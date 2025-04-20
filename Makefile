run:
	uvicorn main:app --reload

test:
	PYTHONPATH=. pytest tests/test_find_word.py

build:
	pip install -r requirements.txt