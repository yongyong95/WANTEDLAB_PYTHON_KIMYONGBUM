# REPOSITORY_NAME
...

# SETUP
```
brew install poetry
pyenv virtualenv {virtual-environment-name}
pyenv local {virutal-environment-name}
poetry install
```

# RECOMMENDED
```
python 3.11 이상 권장 (pyenv 통해서 가상환경 생성)
```

# LOCAL RUN
```
uvicorn --host 0.0.0.0 --port 8000 --workers=4 --reload main:app
```