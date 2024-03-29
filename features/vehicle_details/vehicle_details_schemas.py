from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class BaseVehicleDetailsRequest(BaseModel):
    reg_no: str
    img_url: str
    cord: list
    conf: float
    puc: bool
    insurance: bool


class VehicleDetailsResponse(BaseVehicleDetailsRequest):
    created_at: datetime
    updated_at: datetime
