from datetime import datetime
from uuid import UUID, uuid4

from beanie import before_event, Insert, Replace, Document
from pydantic import Field


class CameraFeedModel(Document):
    camera_feed_id: UUID = Field(default_factory=uuid4, unique=True)
    media_url: str
    user_id: UUID

    soft_delete: bool = Field(default=False)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @before_event([Insert, Replace])
    def update_updated_at(self):
        self.updated_at = datetime.utcnow()

    class Settings:
        name = "camera_feed"

