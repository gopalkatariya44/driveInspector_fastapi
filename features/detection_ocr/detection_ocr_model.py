from datetime import datetime
from uuid import UUID

from beanie import before_event, Insert, Replace, Document
from pydantic import Field


class DetectionOCRModel(Document):
    reg_no: str
    img_url: str
    cord: list
    xyxy: list
    conf: float
    user_id: UUID

    soft_delete: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event([Insert, Replace])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "detection_ocr_details"



