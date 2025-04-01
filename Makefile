run:
	uvicorn main:app --reload

test:
	PYTHONPATH=. pytest tests/test_find_word.py