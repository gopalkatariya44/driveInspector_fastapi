from datetime import datetime

from pydantic import BaseModel
from uuid import UUID


class BaseVehicleDetailsRequest(BaseModel):
    reg_no: str
    img_url: str
    cord: list
    conf: float
    insurance_from: datetime
    insurance_upto: datetime
    puc_from: datetime
    puc_upto: datetime


class VehicleDetailsResponse(BaseVehicleDetailsRequest):
    created_at: datetime
    updated_at: datetime
