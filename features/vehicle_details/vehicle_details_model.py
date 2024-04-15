from datetime import datetime
from uuid import UUID

from beanie import before_event, Insert, Replace, Document, Link
from pydantic import Field


class VehicleDetailsModel(Document):
    reg_no: str
    img_url: str
    cord: list
    xyxy: list
    conf: float
    insurance_from: datetime
    insurance_upto: datetime
    puc_from: datetime
    puc_upto: datetime
    soft_delete: bool = Field(default=False)

    user_id: UUID

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event([Insert, Replace])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "vehicle_details"
