from typing import Optional
from mongey.models.storable_model import StorableModel
from mongey.models.fields import StringField, ReferenceField, DatetimeField
from ashtree.util import uuid4_string, now
from .user import User


class Session(StorableModel):

    COLLECTION = "sessions"
    KEY_FIELD = "key"

    key = StringField(default=uuid4_string, required=True, rejected=True, restricted=True)
    user_id: ReferenceField[User] = ReferenceField(reference_model=User, index=True)
    created_at = DatetimeField(default=now, required=True)

    async def user(self) -> Optional["User"]:
        if self.user_id is None:
            return None
        return await User.cache_get(self.user_id)
