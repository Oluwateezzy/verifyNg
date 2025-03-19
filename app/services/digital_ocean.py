from fastapi import File, HTTPException, UploadFile
import boto3
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.do_spaces_endpoint,
    aws_access_key_id=settings.do_spaces_access_key,
    aws_secret_access_key=settings.do_spaces_secret,
)


def upload_file(file: UploadFile = File(...)):
    file_key = f"uploads/{file.filename}"

    s3_file = s3_client.upload_fileobj(
        file.file, settings.do_spaces_bucket, file_key, ExtraArgs={"ACL": "public-read"}
    )

    response = s3_client.head_object(Bucket=settings.do_spaces_bucket, Key=file_key)
    print(response)

    # file_url = f"https://{settings.do_spaces_bucket}.{settings.do_spaces_region}.digitaloceanspaces.com/{file_key}"

    if response.get("ResponseMetadata", {}).get("HTTPStatusCode") == 200:
        file_url = f"https://{settings.do_spaces_bucket}.{settings.do_spaces_region}.digitaloceanspaces.com/{file_key}"
        return {"file_url": file_url}
    else:
        raise HTTPException(status_code=500, detail="File upload failed.")
