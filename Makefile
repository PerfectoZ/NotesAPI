server:
	uvicorn main:app --port 8080 --reload
.PHONY: server