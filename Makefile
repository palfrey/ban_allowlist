venv:
	./uv venv

requirements.test: uv requirements.test.in requirements.constraints
	./uv pip compile requirements.test.in -c requirements.constraints -o requirements.test

sync: requirements.test
	./uv pip sync requirements.test

watch-tests: sync
	PYTHONPATH=. ptw . --now -vvv -s

.PHONY: sync venv watch-tests