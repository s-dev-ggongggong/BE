# run back server

- flask run --port 8000
- python run.py

# debug back server

flask dev --port 8000

# requirements

pypreqs '../BE'

# db migrate(update)

# KEY

AWS_ACCESS_KEY_ID = aws access key id
AWS_SECRET_ACCESS_KEY =aws secret access key
PRIVATE_EC2_SSH_KEy = ssh_key
BASTION_SSH_PRIVATE_KEY = bst_rsa
KNOWN_HOSTS

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
