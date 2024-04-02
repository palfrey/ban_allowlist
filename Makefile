venv:
	./uv venv

requirements.test: uv requirements.test.in requirements.constraints
	./uv pip compile requirements.test.in -c requirements.constraints -o requirements.test

sync: requirements.test
	./uv pip sync requirements.test

watch-tests: sync
	PYTHONPATH=. ptw . --now -vvv

pre-commit: sync
	pre-commit run -a

mypy: sync
	MYPYPATH=stubs dmypy run .

watch-mypy:
	 watchmedo auto-restart --directory=./ --pattern="*.py;*.pyi" --no-restart-on-command-exit --recursive -- ${MAKE} mypy

integration-tests: sync
	cd integration_tests && python test_banning_works.py

watch-integration-tests:
	 watchmedo auto-restart --directory=./ --pattern="*.py;*.pyi;*.yaml.j2" --ignore-patterns "config/custom_components/ban_allowlist/*.py" --no-restart-on-command-exit --recursive -- ${MAKE} integration-tests

.PHONY: sync venv watch-tests mypy watch-mypy integration-tests watch-integration-tests
