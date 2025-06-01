run:
	uvicorn main:app --reload

run-hypercorn:
	hypercorn main:app --reload

test:
	PYTHONPATH=. pytest tests/test_find_word.py

build:
	pip install -r requirements.txt

run2:
	uvicorn main2:app --reload