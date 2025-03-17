from fastapi import APIRouter


router = APIRouter()


@router.post("/register")
def register():
    return {"message": "Register"}


@router.post("/login")
def login():
    return {"message": "Login"}


@router.post("/validateDocs")
def validateDocs():
    return {"message": "Validate Docs"}


@router.post("/sendOTP")
def sendOTP():
    return {"message": "Send OTP"}
