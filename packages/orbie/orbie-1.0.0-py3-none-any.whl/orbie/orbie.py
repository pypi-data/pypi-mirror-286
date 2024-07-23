#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from collections.abc import Collection
from dataclasses import dataclass, field
from pathlib import Path

from importlab import environment, graph, output  # type: ignore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class IgnoreConfig:
    ancestors: bool = False
    descendents: bool = False
    siblings: bool = False
    cousins: bool = False
    paths: Collection[str] = field(default_factory=lambda: [])
    venv: bool = True


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path("."),
        help="Base project path to find tangled files within (default: ./)",
    )
    parser.add_argument(
        "--exception",
        action="append",
        dest="exceptions",
        help="Adds an exception for an specific tangled file path or entire directory path",
    )
    parser.add_argument(
        "--except-ancestors",
        default=False,
        action="store_true",
        help="Ignore tangled files coming from parent directories of the importer",
    )
    parser.add_argument(
        "--except-descendents",
        default=False,
        action="store_true",
        help="Ignore tangled files coming from subdirectories below the importer",
    )
    parser.add_argument(
        "--except-siblings",
        default=False,
        action="store_true",
        help="Ignore tangled files coming from the same directory as the importer",
    )
    parser.add_argument(
        "--except-cousins",
        default=False,
        action="store_true",
        help="Ignore tangled files coming from directories and subdirectories under the grandparent's directory",
    )
    parser.add_argument(
        "--no-except-venv",
        default=False,
        action="store_false",
        help="Set to not ignore tangled files found in .venv",
    )
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Set to show debug trace logs",
    )
    parser.add_argument("input", type=str, nargs=1, help="Input file or directory")

    # Needed for importlab
    default_python_version = "%d.%d" % sys.version_info[:2]
    parser.add_argument(
        "-V",
        "--python_version",
        type=str,
        action="store",
        dest="python_version",
        default=default_python_version,
        help="Python version of target code, e.g. '3.12'",
    )
    parser.add_argument(
        "-P",
        "--pythonpath",
        type=str,
        action="store",
        dest="pythonpath",
        default="",
        help=f"Directories for reading dependencies - a list of paths separated by '{os.pathsep}'",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.debug:
        global logger
        logger.info("Setting logger to debug mode")
        logger.setLevel(logging.DEBUG)

    ignore_config = IgnoreConfig(
        ancestors=args.except_ancestors,
        descendents=args.except_descendents,
        siblings=args.except_siblings,
        cousins=args.except_cousins,
        paths=args.exceptions or [],
        venv=not args.no_except_venv,
    )

    if ignore_config.venv:
        logger.info("Accepting imports from .venv (i.e. external dependencies)")

    if ignore_config.ancestors:
        logger.info("Accepting imports from ancestors")

    if ignore_config.descendents:
        logger.info("Accepting imports from descendents")

    if ignore_config.siblings:
        logger.info("Accepting imports from siblings")

    if ignore_config.cousins:
        logger.info("Accepting imports from cousins and their descendents")

    if len(ignore_config.paths) > 0:
        logger.info(
            "Accepting the following paths exceptions:\n%s",
            "\n".join(ignore_config.paths),
        )

    input_path = Path(args.input[0])
    if not input_path.exists():
        logger.error("Input path could not be found: %s", input_path)
        sys.exit(1)

    results = {}
    if input_path.is_dir():
        # Scan and check all python files in this directory tree
        for input_file in input_path.rglob("*.py"):
            if not input_file.is_file():
                continue
            import_graph = get_import_graph(args, input_file)
            results[input_file] = check_tangleation(
                import_graph, args.project_root, input_file, ignore_config
            )
    else:
        import_graph = get_import_graph(args, input_path)
        results[input_path] = check_tangleation(
            import_graph, args.project_root, input_path, ignore_config
        )

    if not all(results.values()):
        logger.info(
            "Failing check due to the following file/s:\n%s",
            "\n".join([str(k) for k, v in results.items() if not v]),
        )
        sys.exit(1)


def get_import_graph(args: argparse.Namespace, input_path: Path) -> graph.ImportGraph:
    env = environment.create_from_args(args)
    import_graph = graph.ImportGraph.create(env, [str(input_path)], True)
    logger.info("Source tree:")
    output.print_tree(import_graph)
    return import_graph


def check_tangleation(
    import_graph: graph.ImportGraph,
    project_root: Path,
    input_file: Path,
    ignore_config: IgnoreConfig,
) -> bool:
    logger.info(
        "Checking tangleation of %s against other modules in %s",
        input_file,
        project_root.resolve(),
    )
    tangled_modules = get_tangled_modules(
        import_graph,
        str(input_file),
        project_root,
        ignore_config,
    )

    if len(tangled_modules) > 0:
        logger.info("%d tangled module/s found:", len(tangled_modules))
        for tangled_module, tangle_type in tangled_modules:
            tangled_path = tangled_module.relative_to(project_root.resolve())
            logger.info("%s (%s)", tangled_path, tangle_type)
        return False

    logger.info("0 tangled modules found!")
    return True


def get_tangled_modules(
    import_graph: graph.ImportGraph,
    input_file: str,
    project_root: Path,
    ignore_config: IgnoreConfig,
) -> Collection[tuple[Path, str]]:
    tangled_modules = []
    project_root = project_root.resolve()

    keys = set(x[0] for x in import_graph.graph.edges)
    for key in sorted(keys):
        for _, value in sorted(import_graph.graph.edges([key])):
            importer_path = Path(input_file).resolve()
            imported_path = Path(value)
            logger.debug("Checking %s:%s", importer_path, imported_path)

            # Ignore external imports
            if project_root not in imported_path.parents:
                logger.debug("Ignoring %s as it's not in project root", imported_path)
                continue

            # Ignore exceptions
            tangle_type = classify_tangle(
                importer_path, imported_path, project_root, ignore_config
            )
            if is_excepted(
                importer_path, imported_path, project_root, tangle_type, ignore_config
            ):
                logger.debug(
                    "Ignoring %s as it's marked as an exception", imported_path
                )
                continue

            # Mark import as a tangled import
            tangled_modules.append((imported_path, tangle_type))
    return tangled_modules


def classify_tangle(
    importer_path: Path,
    imported_path: Path,
    project_root: Path,
    ignore_config: IgnoreConfig,
) -> str:
    logger.debug("Classifying imported_path: %s", imported_path)

    relative_path = imported_path.relative_to(project_root)
    logger.debug("Equivalent relative_path: %s", relative_path)

    classification = "unknown"

    # Order is important here as several classifications overlap in attributes
    if importer_path.parent == imported_path.parent:
        classification = "sibling"
    elif importer_path.parent in imported_path.parents:
        classification = "descendent"
    elif imported_path.parent in importer_path.parents:
        classification = "ancestor"
    elif importer_path.parent.parent in imported_path.parents:
        classification = "cousin"

    logger.debug("Tangle type: %s", classification)
    return classification


def is_excepted(
    importer_path: Path,
    imported_path: Path,
    project_root: Path,
    tangle_type: str,
    ignore_config: IgnoreConfig,
) -> bool:
    logger.debug(
        "Checking imported_path for exceptions: %s (%s)", imported_path, tangle_type
    )

    relative_path = imported_path.relative_to(project_root)
    logger.debug("Equivalent relative_path: %s", relative_path)

    # Ignore imports from venv (typically indicator of an external import)
    venv_path = project_root / ".venv"
    if ignore_config.venv and venv_path in imported_path.parents:
        logger.debug("Ignoring %s as it's part of .venv", imported_path)
        return True

    # Ignore imports from parent directories
    if ignore_config.ancestors and tangle_type == "ancestor":
        logger.debug("Ignoring %s as it's an ancestor", imported_path)
        return True

    # Ignore imports from children directories
    if ignore_config.descendents and tangle_type == "descendent":
        logger.debug("Ignoring %s as it's an descendent", imported_path)
        return True

    # Ignore imports within same parent directory
    if ignore_config.siblings and tangle_type == "sibling":
        logger.debug("Ignoring %s as it's a sibling", imported_path)
        return True

    # Ignore imports in directories within the grandparent directory
    if ignore_config.cousins and tangle_type == "cousin":
        logger.debug(
            "Ignoring %s as it's a cousin (or descendent of cousin)", imported_path
        )
        return True

    # Handle exceptions that are marking files
    if str(relative_path) in ignore_config.paths:
        logger.debug("Ignoring %s as it's marked as an exception", imported_path)
        return True

    # Handle exceptions that are marking a directory
    # In case an exception path is a directory, check if relative_path
    # is a subdir of said exception path
    logger.debug("Checking paths exceptions for directory exceptions")
    for exception in ignore_config.paths:
        exception_path = project_root / exception
        logger.debug("Checking %s", exception_path)

        if not exception_path.is_dir():
            logger.debug("Exception path is not a directory")
            continue

        logger.debug("Exception path is a directory")
        if exception_path not in relative_path.resolve().parents:
            logger.debug("Exception path is not a parent of %s", relative_path)
            continue

        logger.debug("Ignoring %s because exception path is a parent", relative_path)
        return True

    return False


if __name__ == "__main__":
    main()
