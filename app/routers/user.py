from fastapi import APIRouter


router = APIRouter()


@router.get("/profile")
def profile():
    return {"message": "Profile"}


@router.post("/updatePassword")
def updatePassword():
    return {"message": "Update Password"}


@router.post("/updateProfile")
def updateProfile():
    return {"message": "Update Profile"}


@router.post("/deleteAccount")
def deleteAccount():
    return {"message": "Delete Account"}
