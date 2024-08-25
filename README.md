# REPOSITORY_NAME
WANTEDLAB_PYTHON_KIMYONGBUM (ASSIGNMENT)

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
* pytest 이용시, pytest.ini 아래 코드 추가 필요 *
[pytest]
pythonpath = app

* sqlite3 이용시, 편의를 위해 DB Browser for SQLite 설치 *
```

# LOCAL RUN
```
[Shell]
DB_URL=sqlite:///wantedlab.db \
uvicorn --host 0.0.0.0 --port 8000 --workers=4 --reload app.main:app
```
```
[Docker]
docker login
docker build --platform linux/arm64 -t wantedlab-company-kimyongbum -f Dockerfile .
docker-compose up

```

# API 명세
### [API 명세 링크](https://everlasting-door-b42.notion.site/Company-API-3988e2c177e449cdaf2296dab247aa6a)
```
(Swagger 문서는 로컬 실행후 `http://localhost:8000/docs` 브라우저 통해 확인 가능)
```