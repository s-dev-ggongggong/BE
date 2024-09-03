from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def read_me():
    return "Hello"
