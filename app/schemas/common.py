from datetime import datetime
from typing import List, Optional

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class RoomBase(BaseModel):
    name: str
    capacity: int = 0
    night_period: Optional[str] = None
    initial_count: int = 0
    remark: Optional[str] = None


class RoomCreate(RoomBase):
    pass


class RoomRead(RoomBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True


class PersonBase(BaseModel):
    name: str
    photo_path: Optional[str] = None
    remark: Optional[str] = None
    room_id: Optional[str] = None


class PersonCreate(PersonBase):
    pass


class PersonRead(PersonBase):
    id: str
    created_at: datetime

    class Config:
        orm_mode = True
