from uuid import UUID

from bson import ObjectId
from fastapi import HTTPException, status

from .camera_feed_model import CameraFeedModel


class CameraFeedServices:
    """
    Store data in database
    """

    @staticmethod
    async def get_list(user_id: UUID, page: int = 1, limit: int = 10):
        try:
            camera_feed_list = await (CameraFeedModel.find(CameraFeedModel.user_id == user_id,
                                                           CameraFeedModel.soft_delete == False)
                                      # .skip(page).limit(limit)
                                      .to_list())
            return camera_feed_list
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning camera feed list get_list."
            )

    @staticmethod
    async def add(user_id, media_url):
        media_feed = CameraFeedModel(
            user_id=user_id,
            media_url=media_url,
        )
        await media_feed.save()
        return media_feed

    @staticmethod
    async def get_one(id: ObjectId):
        try:
            camera_feed = await CameraFeedModel.find_one(CameraFeedModel.id == id)
            return camera_feed
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Somthing went wrong in returning detection camera feed get_one."
            )

    @staticmethod
    async def update(id, data):
        camera_feed = await CameraFeedModel.find_one(CameraFeedModel.id == id)

        await camera_feed.update({"$set": data})
        await camera_feed.save()
        return camera_feed

    @staticmethod
    async def delete(id: ObjectId):
        detection_details = await CameraFeedServices.get_one(id)
        if detection_details:
            # await detection_details.delete()
            await detection_details.update({"$set": {"soft_delete": True}})
            return {"Msg": "Project deleted successful."}
        else:
            return {"Msg": "Project not available."}
