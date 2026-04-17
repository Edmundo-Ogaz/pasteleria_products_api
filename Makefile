env:
        python3 -m venv venv

activate:
        source venv/bin/activate

deactivate:
        deactivate

run:
	uvicorn main_serverless:app --reload

run-hypercorn:
	hypercorn main_serverless:app --reload

test:
	PYTHONPATH=. pytest tests/test_find_word.py

frezze:
	python -m pip freeze > requirements.txt

build:
	pip install -r requirements.txt

run2:
	uvicorn main_old:app --reload