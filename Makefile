server:
	uvicorn main:app --port 8080 --reload
test:
	python3 -m unittest

.PHONY: server test