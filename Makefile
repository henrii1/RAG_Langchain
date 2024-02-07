install:
	pip install -r requirements.txt &&\
			pip install --upgrade flask python-dotenv-vault

test:
	python -m pytest -vv tests/test_*.py

format:
	black *.py

lint:
	pylint --disable=R,C,E1120 *.py

all: install lint test