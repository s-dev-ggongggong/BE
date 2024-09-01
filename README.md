# run back server

flask run

# db migrate(update)

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
