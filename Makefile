venv:
	./uv venv

requirements.test: uv requirements.test.in requirements.constraints
	./uv pip compile requirements.test.in -c requirements.constraints -o requirements.test

sync: requirements.test
	./uv pip sync requirements.test

watch-tests: sync
	PYTHONPATH=. ptw . --now -vvv -s

pre-commit: sync
	pre-commit run -a

mypy: sync
	MYPYPATH=stubs dmypy run .

watch-mypy:
	 watchmedo auto-restart --directory=./ --pattern="*.py;*.pyi" --no-restart-on-command-exit --recursive -- ${MAKE} mypy

.PHONY: sync venv watch-tests
