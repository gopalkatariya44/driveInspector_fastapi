from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class BaseDetectionOCRRequest(BaseModel):
    reg_no: str
    img_url: str
    cord: list
    xyxy: list
    conf: float
    user_id: UUID
    camera_feed_id: UUID


class DetectionOCRResponse(BaseDetectionOCRRequest):
    created_at: datetime
    updated_at: datetime
