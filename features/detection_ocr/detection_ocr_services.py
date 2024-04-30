from uuid import UUID
from datetime import datetime

import bson
from bson import ObjectId
from fastapi import HTTPException, status

from features.detection_ocr.detection_ocr_model import DetectionOCRModel
import bson


def convert_uuid_to_string(uuid_bytes):
    if isinstance(uuid_bytes, bson.binary.Binary):
        # Try different subtypes for wider compatibility
        if uuid_bytes.subtype in (bson.binary.STANDARD, bson.binary.UUID):
            return uuid_bytes.to_string()
    return uuid_bytes


class DetectionOCRServices:
    """
    Store data in database
    """

    @staticmethod
    async def get_list(id: UUID, page: int = 1, limit: int = 10):
        # try:
        pipeline = [
            {
                "$lookup": {
                    "from": "vehicle_details",
                    "localField": "reg_no",
                    "foreignField": "reg_no",
                    "as": "vehicle_info"
                }
            },
            {
                "$unwind": "$vehicle_info"
            },
            {
                "$project": {
                    "_id": "$_id",
                    "detection_ocr_id": "$detection_ocr_id",
                    "reg_no": "$reg_no",
                    "img_url": "$img_url",
                    "cord": "$cord",
                    "xyxy": "$xyxy",
                    "conf": "$conf",
                    "user_id": "$user_id",
                    "camera_feed_id": "$camera_feed_id",
                    "created_at": "$created_at",
                    "updated_at": "$updated_at",
                    "insurance_details": "$vehicle_info.insurance_details",
                    "puc_details": "$vehicle_info.puc_details",
                    "email_id": "$vehicle_info.email_id",
                    "owner_name": "$vehicle_info.owner_name"
                }
            }
        ]
        detection_details_list = await (DetectionOCRModel.find(DetectionOCRModel.camera_feed_id == id,
                                                               DetectionOCRModel.soft_delete == False
                                                               ).aggregate(pipeline)
                                        # .skip(page).limit(limit)
                                        .to_list())
        print(f"---------> {detection_details_list}")
        return detection_details_list
        # except Exception as e:
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Somthing went wrong in returning detection details list get_list."
        #     )

    @staticmethod
    async def get_one(id: UUID):
        try:
            detection_details = await DetectionOCRModel.find_one(DetectionOCRModel.detection_ocr_id == id)
            return detection_details
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning detection details get_one."
            )

    @staticmethod
    async def update(id: UUID, data):
        detection_details = await DetectionOCRModel.find_one(DetectionOCRModel.detection_ocr_id == id)

        await detection_details.update({"$set": data})
        await detection_details.save()
        return detection_details

    @staticmethod
    async def delete(id: UUID):
        detection_details = await DetectionOCRModel.find_one(DetectionOCRModel.detection_ocr_id == id)
        if detection_details:
            # await detection_details.delete()
            await detection_details.update({"$set": {"soft_delete": True}})
            return {"Msg": "Project deleted successful."}
        else:
            return {"Msg": "Project not available."}
