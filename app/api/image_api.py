import base64

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import uuid4
from app import models, schemas
from app.db.connection import db
from app.depends.validate_api_key import validate_api_key
from app.schemas.image_schemas import UploadImageREQ
from app.utils.image_utils import get_image_size, resize_image, get_image_extension, get_squared_thumbnail, get_image_file_size

image = APIRouter()


@image.post("/upload")
def upload_image(
    body: schemas.UploadImageREQ,
    image_group_id: int,
    session: Session = Depends(db.session),
    # valid_key: bool = Depends(validate_api_key),
):
    """
    :param body:
    :param session:
    :param valid_key:
    :return:
    """
    image_convert_size = [512, 1024, 1980]
    image_size = get_image_size(body.image)    # returns (120, 150)
    image_extension = get_image_extension(body.image)
    print(f"original - image_size : {image_size}")
    print(f"original - file_size : {len(base64.b64decode(body.image))}")
    print(f"original - image_extension : {image_extension}")
    uuid = str(uuid4())
    thumbnail, file_size = get_squared_thumbnail(body.image)
    images = {}
    total_size = file_size
    print(f"thumbnail - image_size : {get_image_size(thumbnail)}")
    print(f"thumbnail - file_size : {file_size}")
    print(f"total_size : {total_size}")

    for size in image_convert_size:
        if image_size[0] > size:
            resized_image, file_size = resize_image(body.image, size)
            total_size += file_size
            images[size] = resized_image
            image_extension = get_image_extension(resized_image)
            print(f"resized_image - image_size : {get_image_size(resized_image)}")
            print(f"resized_image - file_size : {file_size}")
            print(f"resized_image - image_extension : {image_extension}")
            print(f"total_size : {total_size}")


@image.get("/{image_id}")
def get_image(request: Request, image_id: int, session: Session = Depends(db.session)):
    if request.state.user:
        return {"message": "success"}
    return {"message": "failed"}