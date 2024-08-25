# REPOSITORY_NAME
...

# PYTHON VERSION
```
python 3.11.2
```

# SETUP
```
brew install poetry
brew install sqlite3
pyenv virtualenv {virtual-environment-name}
pyenv local {virutal-environment-name}
poetry install
```

# REFERENCE
```
pytest 이용시, pytest.ini 설정 필요
[pytest]
pythonpath = app

sqlite3 이용시, 편의를 위해 DB Browser for SQLite 설치 
```

# LOCAL RUN
```
[Shell]

uvicorn --host 0.0.0.0 --port 8000 --workers=4 --reload main:app
```
```
[Docker]


```