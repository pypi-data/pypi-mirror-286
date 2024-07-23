# Orbie

Orbie is a checker to control and restrict the web of interdependencies within a
Python project. It can raise warnings when unwanted interdependencies pop up in
a project.

Orbie is named after the orb-weaver spider known for the complex webs it can
create.

## Why?

Orbie is intended be a tool to set rules and guidance on how the different parts
of a Python project can interdepend on each other. Why might this be interesting
to someone? Well, sometimes in projects where cohesion and complexity is not
kept in mind for the architecture, people will glue random parts together like
making the birthday calculator function interdependent on the number of pets
string formatter. And what starts out as a quick five minute adventure to fix
the dog counter displayed after coming back from a holiday turns into a 6 week
tour through the code base untangling it. So this kind of checker can be used
to stop the tangling up of the code base.

By minimising the interdependencies (or strictly controlling it), it can
decrease the system complexity and open up options to do things like optimise
the ci-cd to test only the affected parts of a project without fear of missing
re-testing unrelated but affected components.

## Example

One example usage might be where you have a single Python project with several
subprojects being shipped as part of it but you want to have some level of
isolation between the different modules.

```
src
└── example
    ├── example_a
    │   ├── children
    │   │   ├── child.py
    │   │   └── grandchildren
    │   │       └── grandchild.py
    │   ├── example_a.py
    │   └── sibling.py
    ├── example_b
    │   └── example_b.py
    ├── example_c
    │   ├── children
    │   │   └── child.py
    │   ├── example_c.py
    │   └── sibling.py
    ├── example_d
    │   └── example_d.py
    └── example_shared
        └── shared.py
```

We may not want `example_a` referencing anything from `example_b`, `example_c`
or `example_d`. And vice-versa for `example_b` and `example_c` and `example_d`.

This can be enforced with some simple code review but that may fail if the
reviewer does not have enough coffee. We need a more complicated solution for
the sake of being programmers building tools for programmers.

We can configure Orbie to not allow imports from subprojects to its cousins
or ancestors and only allow imports within their project spaces.

## How It Works

Orbie is really just a wrapper script around [importlab][importlab] which can
statically parse the imports dependency tree. Orbie can then filter the project
dependencies to find dependencies that are not permitted. If the number of these
exceed zero, the script will exit with error code `1`.

[importlab]: https://github.com/google/importlab)

## Installation

Orbie can be installed from pypi.

Example:

```
pip install orbie
```

## Usage

```
$ orbie --help
usage: orbie [-h]
             [--project-root PROJECT_ROOT]
             [--exception EXCEPTIONS]
             [--except-ancestors]
             [--except-descendents]
             [--except-siblings]
             [--except-cousins]
             [--no-except-venv]
             [--debug]
             [-V PYTHON_VERSION]
             [-P PYTHONPATH]
             input

positional arguments:
  input                 Input file or directory

options:
  -h, --help            show this help message and exit
  --project-root PROJECT_ROOT
                        Base project path to find tangled files within
                        (default: ./)
  --exception EXCEPTIONS
                        Adds an exception for an specific tangled file path or
                        entire directory path
  --except-ancestors    Ignore tangled files coming from parent directories of
                        the importer
  --except-descendents  Ignore tangled files coming from subdirectories below
                        the importer
  --except-siblings     Ignore tangled files coming from the same directory as
                        the importer
  --except-cousins      Ignore tangled files coming from directories and
                        subdirectories under the grandparent's directory
  --no-except-venv      Set to not ignore tangled files found in .venv
  --debug               Set to show debug trace logs
  -V PYTHON_VERSION, --python_version PYTHON_VERSION
                        Python version of target code, e.g. '3.12'
  -P PYTHONPATH, --pythonpath PYTHONPATH
                        Directories for reading dependencies - a list of paths
                        separated by ':'
```

Note that Orbie is assumed to be called from the project root. The current
working directory is used to filter internal and external dependencies. Imports
coming from a virtual environment in the current working directory (i.e. in a
`.venv` subdirectory) are marked as external dependencies.

### Usage: Explicit Exceptions

Of course, restricting interdependencies to 0 typically makes no sense. The more
realistic use case of Orbie is to only allow select interdependencies that
meet the architecture of the project. One example might be only allowing modules
in a specific shared space from being imported (thus creating a clear structure
around the interdependencies).

These exceptional import paths can be specified with `--exception`. They can
reference files or directories.

Example:

```
src
└── example
    ├── example_a
    │   └── example_a.py
    └── example_shared
        └── shared.py
```

In this case, if `example_a.py` should freely import modules from
`example_shared`, this can be done with the explicit exception like so.

```
--exception src/example/example_shared
```

### Usage: Ignore Ancestors

Imported modules that sit in the file system hierarchy above the importer module
tree can be excepted with `--except-ancestors`.

Example: if `child.py` imports something from `sibling.py`, this is considered
an ancestor import.

```
src
└── example
    └── example_a
        ├── children
        │   ├── child.py
        ├── example_a.py
        └── sibling.py
```

### Usage: Ignore Descendents

Imported modules that sit in the file system hierarchy below the importer module
tree can be excepted with `--except-descendents`.

Example: if `example_a.py` imports something from `child.py`, this is considered
a descendent import.

```
src
└── example
    └── example_a
        ├── children
        │   ├── child.py
        └── example_a.py
```

### Usage: Ignore Siblings

Imported modules that sit in the file system hierarchy parallel to the importer module
tree can be excepted with `--except-siblings`.

Example: if `example_a.py` imports something from `sibling.py`, this is
considered a sibling import.

```
src
└── example
    └── example_a
        ├── example_a.py
        └── sibling.py
```
### Usage: Ignore Cousins

Imported modules that sit in the file system tree parallel to the importer
module's parent directory tree can be excepted with `--except-cousins`.

Example: if `example_a.py` imports something from `example_b.py`, this is
considered a cousin import.

```
src
└── example
    ├── example_a
    │   └── example_a.py
    └── example_b
        └── example_b.py
```

## Example Project

You can try run Orbie on the subdir example.

Example:

```
git clone https://github.com/michael131468/orbie.git
cd orbie
cd example
pdm install
pdm run orbie src/example/example_a
pdm run orbie src/example/example_b
pdm run orbie src/example/example_c
pdm run orbie src/example/example_d
```

### Example Project: Example A

In this example, `example_a.py` should show some sibling imports, descendent
imports, and an import from the `example_shared space` (a cousin import).

```
$ pdm run orbie src/example/example_a/example_a.py
INFO:orbie.orbie:Accepting imports from .venv (i.e. external dependencies)
INFO:orbie.orbie:Source tree:
+ src/example/example_a/example_a.py
    :: example/example_a/sibling.py
    :: example/example_a/children/child.py
    :: example/example_a/children/grandchildren/grandchild.py
    :: example/example_shared/shared.py
INFO:orbie.orbie:Checking tangleation of src/example/example_a/example_a.py
against other modules in
/Users/michael/git/github.com/michael131468/orbie/example
INFO:orbie.orbie:4 tangled module/s found:
INFO:orbie.orbie:src/example/example_a/children/child.py (descendent)
INFO:orbie.orbie:src/example/example_a/children/grandchildren/grandchild.py
(descendent)
INFO:orbie.orbie:src/example/example_a/sibling.py (sibling)
INFO:orbie.orbie:src/example/example_shared/shared.py (cousin)
INFO:orbie.orbie:Failing check due to the following file/s:
src/example/example_a/example_a.py
```

These imports could be excepted to get a passing result like so:

```
$ pdm run orbie src/example/example_a/example_a.py \
    --exception src/example/example_shared \
    --except-siblings \
    --except-descendents
INFO:orbie.orbie:Accepting imports from .venv (i.e. external dependencies)
INFO:orbie.orbie:Accepting imports from descendents
INFO:orbie.orbie:Accepting imports from siblings
INFO:orbie.orbie:Accepting the following paths exceptions:
src/example/example_shared
INFO:orbie.orbie:Source tree:
+ src/example/example_a/example_a.py
    :: example/example_a/sibling.py
    :: example/example_a/children/child.py
    :: example/example_a/children/grandchildren/grandchild.py
    :: example/example_shared/shared.py
INFO:orbie.orbie:Checking tangleation of src/example/example_a/example_a.py
against other modules in
/Users/michael/git/github.com/michael131468/orbie/example
INFO:orbie.orbie:0 tangled modules found!
```

### Example Project: Example B

In this example, `example_b.py` should show a cousin import from `example_a.py`.

```
pdm run orbie src/example/example_b/example_b.py
INFO:orbie.orbie:Accepting imports from .venv (i.e. external dependencies)
INFO:orbie.orbie:Source tree:
+ src/example/example_b/example_b.py
    :: example/example_a/__init__.py
INFO:orbie.orbie:Checking tangleation of src/example/example_b/example_b.py
against other modules in
/Users/michael/git/github.com/michael131468/orbie/example
INFO:orbie.orbie:1 tangled module/s found:
INFO:orbie.orbie:src/example/example_a/__init__.py (cousin)
INFO:orbie.orbie:Failing check due to the following file/s:
src/example/example_b/example_b.py
```

This import could be excepted to get a passing result like so:

```
$ pdm run orbie src/example/example_b/example_b.py \
    --exception src/example/example_a/
INFO:orbie.orbie:Accepting imports from .venv (i.e. external dependencies)
INFO:orbie.orbie:Accepting the following paths exceptions:
src/example/example_a/
INFO:orbie.orbie:Source tree:
+ src/example/example_b/example_b.py
    :: example/example_a/__init__.py
INFO:orbie.orbie:Checking tangleation of src/example/example_b/example_b.py
against other modules in
/Users/michael/git/github.com/michael131468/orbie/example
INFO:orbie.orbie:0 tangled modules found!
```

### Example Project: Example C

In this example, `example_c.py` should show a descendent import from the child
`child.py`.

```
$ pdm run orbie src/example/example_c/example_c.py
INFO:orbie.orbie:Accepting imports from .venv (i.e. external dependencies)
INFO:orbie.orbie:Source tree:
+ src/example/example_c/example_c.py
    :: example/example_c/children/child.py
INFO:orbie.orbie:Checking tangleation of src/example/example_c/example_c.py against other modules in /Users/michael/git/github.com/michael131468/orbie/example
INFO:orbie.orbie:1 tangled module/s found:
INFO:orbie.orbie:src/example/example_c/children/child.py (descendent)
INFO:orbie.orbie:Failing check due to the following file/s:
src/example/example_c/example_c.py
```

This import could be excepted to get a passing result like so:

```
$ pdm run orbie src/example/example_c/example_c.py --except-descendents
INFO:orbie.orbie:Accepting imports from .venv (i.e. external dependencies)
INFO:orbie.orbie:Accepting imports from descendents
INFO:orbie.orbie:Source tree:
+ src/example/example_c/example_c.py
    :: example/example_c/children/child.py
INFO:orbie.orbie:Checking tangleation of src/example/example_c/example_c.py
against other modules in
/Users/michael/git/github.com/michael131468/orbie/example
INFO:orbie.orbie:0 tangled modules found!
```

### Example Project: Example D

In this example, `example_d.py` should show no imports (and thus no tangling to
resolve).

```
$ pdm run orbie src/example/example_d/example_d.py
INFO:orbie.orbie:Accepting imports from .venv (i.e. external dependencies)
INFO:orbie.orbie:Source tree:
+ src/example/example_d/example_d.py
INFO:orbie.orbie:Checking tangleation of src/example/example_d/example_d.py against other modules in /Users/michael/git/github.com/michael131468/orbie/example
INFO:orbie.orbie:0 tangled modules found!
```
