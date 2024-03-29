from datetime import datetime

from beanie import before_event, Insert, Replace, Document
from pydantic import Field


class VehicleDetailsModel(Document):
    # user_id: UUID = Field(default_factory=uuid4, unique=True)
    reg_no: str
    img_url: str
    cord: list
    xyxy: list
    conf: float
    puc: bool
    insurance: bool

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event([Insert, Replace])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "vehicle_details"
