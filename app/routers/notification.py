from fastapi import APIRouter


router = APIRouter()


@router.post("/sendNotification")
def sendNotification():
    return {"message": "Send Notification"}


@router.get("/getNotifications")
def getNotifications():
    return {"message": "Get Notifications"}


@router.post("/markAsRead")
def markAsRead():
    return {"message": "Mark As Read"}


@router.post("/deleteNotification")
def deleteNotification():
    return {"message": "Delete Notification"}
