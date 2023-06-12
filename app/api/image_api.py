import base64

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from uuid import uuid4
from app import models, schemas
from app.db.connection import db
from app.depends.validate_api_key import validate_api_key
from app.schemas.image_schemas import UploadImageREQ
from app.utils.image_utils import get_image_size, resize_image, get_image_extension, get_squared_thumbnail, get_image_file_size, s3_upload

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
    image_convert_size = [512, 1024, 1920]
    image_size = get_image_size(body.image_base64)    # returns (120, 150)
    image_extension = get_image_extension(body.image_base64)
    print(f"type(body.image_base64) : {type(body.image_base64)}")
    print(f"original - image_size : {image_size}")
    print(f"original - file_size : {len(base64.b64decode(body.image_base64))}")
    print(f"original - image_extension : {image_extension}")
    uuid = str(uuid4())
    thumbnail, file_size = get_squared_thumbnail(body.image_base64)
    print(f"thumbnail : {thumbnail}")
    print(f"type(thumbnail) : {type(thumbnail)}")
    images = {"thumbnail": thumbnail}
    total_size = file_size
    print(f"thumbnail - image_size : {thumbnail.size}")
    print(f"thumbnail - file_size : {file_size}")
    print(f"total_size : {total_size}")

    for size in image_convert_size:
        if image_size[0] > size:
            resized_image, file_size = resize_image(body.image_base64, size)
            total_size += file_size
            images[size] = resized_image
            print(f"resized_image - image_size : {resized_image.size}")
            print(f"resized_image - file_size : {file_size}")
            print(f"resized_image - image_extension : {resized_image.format}")
            print(f"total_size : {total_size}")
            print(f"type(resized_image): {type(resized_image)}")

    print(f"images: {images}")

    image_detail = {}
    for k, v in images.items():
        image_detail[k] = s3_upload(v, f"{uuid}_{k}.webp")

    print(image_detail)


"""
    있음 user_id = Column(ForeignKey("users.id"), nullable=False)
    있음 image_group_id = Column(ForeignKey("image_groups.id"), nullable=False)
    있음 uuid = Column(String(64), nullable=False, default=uuid.uuid4)
    필요없는 모델 s3_key = Column(String(256), nullable=False)
    있음 file_name = Column(String(128), nullable=False)
    필요없는 모델 file_mime = Column(String(64), nullable=False)
    있음 file_extension = Column(String(16), nullable=False)
    필요없는 모델 file_size = Column(Integer, nullable=False)
    있음 total_file_size = Column(Integer, nullable=False)
    있음 image_url_data = Column(JSON, nullable=False)
    image_group = relationship("ImageGroups", back_populates="images", uselist=False)
"""


@image.get("/{image_id}")
def get_image(request: Request, image_id: int, session: Session = Depends(db.session)):
    if request.state.user:
        return {"message": "success"}
    return {"message": "failed"}