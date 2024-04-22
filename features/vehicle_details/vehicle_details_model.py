from datetime import datetime
from uuid import UUID

from beanie import before_event, Insert, Replace, Document, Indexed
from pydantic import Field


# class VehicleInsuranceDetails():
#     insurance_from: datetime
#     insurance_upto: datetime
#     insurance_company_code: int
#     insurance_company_name: str
#     opdt: datetime
#     policy_no: str
#     vahan_verify: str
#
#
# class VehiclePUCDetails():
#     puc_from: datetime
#     puc_upto: datetime
#     puc_centreno: str
#     puc_no: str
#     op_dt: datetime


class VehicleDetailsModel(Document):
    state_code: str
    state: str
    office_code: int
    office_name: str
    reg_no: Indexed(str, unique=True)
    reg_date: datetime
    purchase_date: datetime
    owner_count: int
    owner_name: str
    owner_father_name: str
    current_address_line1: str
    current_address_line2: str
    current_address_line3: str
    current_district_name: str
    current_state: str
    current_state_name: str
    current_pincode: int
    permanent_address_line1: str
    permanent_address_line2: str
    permanent_address_line3: str
    permanent_district_name: str
    permanent_state: str
    permanent_state_name: str
    permanent_pincode: int
    owner_code_descr: str
    reg_type_descr: str
    vehicle_class_desc: str
    chassis_no: str
    engine_no: str
    vehicle_manufacturer_name: str
    model_code: str
    model: str
    body_type: str
    cylinders_no: int
    vehicle_hp: float
    vehicle_seat_capacity: int
    vehicle_standing_capacity: int
    vehicle_sleeper_capacity: int
    unladen_weight: int
    vehicle_gross_weight: int
    vehicle_gross_comb_weight: int
    fuel_descr: str
    color: str
    manufacturing_mon: int
    manufacturing_yr: int
    norms_descr: str
    wheelbase: int
    cubic_cap: int
    floor_area: int
    ac_fitted: str
    audio_fitted: str
    video_fitted: str
    vehicle_purchase_as: str
    vehicle_catg: str
    dealer_code: str
    dealer_name: str
    dealer_address_line1: str
    dealer_address_line2: str
    dealer_address_line3: str
    dealer_district: str
    dealer_pincode: str
    sale_amount: int
    laser_code: str
    garage_add: str
    length: int
    width: int
    height: int
    reg_upto: datetime
    fit_upto: datetime
    annual_income: int
    op_dt: datetime
    imported_vehicle: str
    other_criteria: str
    status: str
    vehicle_type: str
    tax_mode: str
    mobile_no: str
    email_id: str
    pan_no: str
    aadhar_no: str
    passport_no: str
    ration_card_no: str
    voter_id: str
    dl_no: str
    verified_on: datetime
    dl_validation_required: bool
    condition_status: bool
    insurance_details: dict
    puc_details: dict

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    soft_delete: bool = Field(default=False)

    @before_event([Insert, Replace])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "vehicle_details"
