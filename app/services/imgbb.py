import base64
import requests
from fastapi import File, HTTPException, UploadFile


IMGBB_API_KEY = "7ca1bb5acc2466cf7f45094db12c32c7"
IMGBB_UPLOAD_URL = "https://api.imgbb.com/1/upload"


async def upload_file_imgbb(file: UploadFile = File(...)):
    try:
        file_data = await file.read()
        encoded_image = base64.b64encode(file_data).decode("utf-8")
        response = requests.post(
            IMGBB_UPLOAD_URL,
            params={"key": IMGBB_API_KEY},
            data={"image": encoded_image},
        )

        print(response.json())

        if response.status_code != 200:
            raise HTTPException(
                status_code=500, detail="Failed to upload image to Imgbb"
            )

        response_data = response.json()
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to upload image to Imgbb")
