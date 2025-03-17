from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    middle_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    nin = Column(String, nullable=False)
    is_identical = Column(Boolean, nullable=False)
    photo_image = Column(String, nullable=False)
    government_id = Column(String, nullable=False)
    thumb_photo = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
