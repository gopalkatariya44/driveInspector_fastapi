from uuid import UUID
from datetime import datetime

from bson import ObjectId
from fastapi import HTTPException, status

from features.detection_ocr.detection_ocr_model import DetectionOCRModel


class DetectionOCRServices:
    """
    Store data in database
    """

    @staticmethod
    async def get_list(id: UUID, page: int = 1, limit: int = 10):
        try:
            detection_details_list = await (DetectionOCRModel.find(DetectionOCRModel.camera_feed_id == id,
                                                                   DetectionOCRModel.soft_delete == False
                                                                   )
                                            # .skip(page).limit(limit)
                                            .to_list())
            return detection_details_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning detection details list get_list."
            )

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
