run:
	uvicorn main:app --reload

run-hypercorn:
	hypercorn main:app --reload

test:
	PYTHONPATH=. pytest tests/test_find_word.py

frezze:
	python -m pip freeze > requirements.txt

build:
	pip install -r requirements.txt

run2:
	uvicorn main2:app --reload