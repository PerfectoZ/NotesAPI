server:
	uvicorn main:app --host 0.0.0.0 --port 8080 --reload
test:
	python3 -m unittest

.PHONY: server test