PYTHON := .venv/bin/python

.NOTPARALLEL:

.PHONY: setup collect build reason validate test serve manual all
setup:
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt -r requirements_reasoner.txt
collect:
	$(PYTHON) src/collect.py
build:
	$(PYTHON) src/build.py
reason:
	$(PYTHON) src/reason.py $(if $(JAVA),--java "$(JAVA)",)
validate:
	$(PYTHON) src/validate.py
	$(PYTHON) src/prepare_web.py
test:
	$(PYTHON) -m pytest -q
serve:
	$(PYTHON) src/server.py
manual:
	$(PYTHON) src/make_docs.py
all: collect build reason validate test
