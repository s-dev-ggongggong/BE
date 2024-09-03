from fastapi import FastAPI
from me import router as me_router
from fastapi.openapi.utils import get_openapi
import yaml

app = FastAPI()

app.include_router(me_router)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    with open("D:/STUDY/code_study/project/S_dev/BE-1/fastapi-swagger-example/proofhub13-test-api-1.0.0-resolved.yaml", "r") as file:
        openapi_schema = yaml.safe_load(file)
    app.openapi_schema = get_openapi(
        title=openapi_schema['info']['title'],
        version=openapi_schema['info']['version'],
        description=openapi_schema['info']['description'],
        routes=app.routes
    )
    return app.openapi_schema

app.openapi = custom_openapi
