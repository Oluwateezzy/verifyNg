from fastapi import APIRouter


router = APIRouter()


@router.post("/register")
def register():
    return {"message": "Register"}


@router.post("/login")
def login():
    return {"message": "Login"}
