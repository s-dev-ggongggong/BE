# run back server

- flask run --port 8000 (only)

# 서버 정상작동 확인용

python app.py dev --port 8000

## 가끔 경로 못찾거나 할때

### GITBASH, LINUX /MAC

- export FLASK_APP=app.py

### WINDOWS

- set FLASK_APP=app.py

# requirements

pip install pipreqs

pipreqs . --ignore flask --force

# requirements 버전 dependency 관리

pip install -r requirements.txt

# db migrate

[DBBROWSER등 db_client 서버 끄고 진행]
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# db 초기화

rm -rf migrations
rm -rf migrations/\*

# db migration error

- migrations/versions 내 생기는 config 파일 프롬프트 수정

# script 이용한 json 업로드

python -m scripts.load_emails

# 서버 에러 터질때

1. find . -name "**pycache**" -exec rm -rf {} +
2. find . -name ".pyc" -delete
3. export FLASK_APP=app.py|| set FLASK_APP =app.py

# KEY

AWS_ACCESS_KEY_ID = aws access key id
AWS_SECRET_ACCESS_KEY =aws secret access key
PRIVATE_EC2_SSH_KEy = ssh_key
BASTION_SSH_PRIVATE_KEY = bst_rsa

# JSON_FORMAT

```
[post] : /traning/create

request body:
{
    traningName: STRING,
    traningDesc : STRING,
    traningStart : YYYY-MM-DD,
    traningEnd : YYYY-MM-DD,
    resourceUser : INTIGER,
    maxPhisingMail : INTIGER
}

response body:
{
    status: |200|400|500|
    message : "훈련이 생성되었습니다." | "에러 발생"
}

/traing/upload
{
    file:BLOB
}
response body:
{
    status: |200|400|500|
    message : "업로드 성공" | "에러 발생"
}

```
