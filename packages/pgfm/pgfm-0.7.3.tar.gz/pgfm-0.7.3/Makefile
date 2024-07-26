.PHONY: help

help:
	@printf "build\n\
	  Build Python distributables.\n"
	@printf "docs\n\
	  Build documentation.\n"
	@printf "publish\n\
	  Publish the package to PyPI.\n"
	@printf "reqs\n\
	  Install Python requirements.\n"
	@printf "run\n\
	  Open Python shell with imported 'pgfm'.\n"
	@printf "test [path]\n\
	  Run tests. Use 'path=TestXyz.…' for a specific test.\n"
	@printf "ve39\n\
	  Set up Python virtual environment.\n"

# Private Makefile. Not a part of a project. Included conditionally; no error
# if it does not exist. The reason is to have a convenient way to run private
# commands using Make.

-include Makefile.private

# ----------------------------------------------------------------------------
# Virtual environment.

ve39:
	python -m venv ve39

python  := ve39/bin/python
pip     := ve39/bin/pip

# ----------------------------------------------------------------------------
# Python requirements.

.PHONY: reqs

reqs: ve39
	$(pip) install -r requirements.txt 

# ----------------------------------------------------------------------------
# Open Python shell with imported 'pgfm'.

.PHONY: run

run:
	$(python) -B -i -c "import pgfm; from importlib import reload"

# ----------------------------------------------------------------------------
# Run tests

.PHONY: test

ifdef path
    TESTPATH := .$(path)
endif

test:
	$(python) -B -m unittest test$(TESTPATH)

run test : export PYTHONPATH := src:tests

# ----------------------------------------------------------------------------
# Build the distributables.

.PHONY: build

build:
	flit build --no-use-vcs

# ----------------------------------------------------------------------------
# Publish the distributables.

.PHONY: publish

publish:
	flit publish

# ----------------------------------------------------------------------------
# Short command reference
#
# flit
#   --no-use-vcs
#     Do not use version control system.
#
# pip
#   -r <file>
#     Install modules from the file.
#
# python
#   -B
#      Do not write bytecode.
#   -c <cmd>
#      Execute the specified command.
#   -i
#      Do not exit after execution, but stay in the Python shell.
#   -m <module> 
#      Execute the specified module.
