from uuid import UUID

from bson import ObjectId
from fastapi import HTTPException, status

from features.vehicle_details.vehicle_details_model import VehicleDetailsModel


class VehicleDetailsServices:
    """
    Store data in database
    """

    @staticmethod
    async def get_list(user_id: UUID, page: int = 1, limit: int = 10):
        try:
            vehicle_details_list = await (VehicleDetailsModel.find(
                VehicleDetailsModel.user_id == user_id,
                VehicleDetailsModel.soft_delete == False
            )
                                          # .skip(page).limit(limit)
                                          .to_list())
            return vehicle_details_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning vehicle details list."
            )

    @staticmethod
    async def get_one(id: ObjectId):
        try:
            vehicle_details = await VehicleDetailsModel.find_one(VehicleDetailsModel.id == id)
            return vehicle_details
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning vehicle details."
            )

    @staticmethod
    async def update(id: UUID, data):
        vehicle_details = await VehicleDetailsModel.find_one(VehicleDetailsModel.id == id)

        await vehicle_details.update({"$set": data})
        await vehicle_details.save()
        return vehicle_details

    @staticmethod
    async def delete(id: ObjectId):
        vehicle_details = await VehicleDetailsServices.get_one(id)
        if vehicle_details:
            # await vehicle_details.delete()
            await vehicle_details.update({"$set": {"soft_delete": True}})
            return {"Msg": "Project deleted successful."}
        else:
            return {"Msg": "Project not available."}
