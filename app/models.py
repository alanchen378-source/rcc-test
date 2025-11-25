import datetime as dt
import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.db.session import Base


def default_uuid():
    return str(uuid.uuid4())


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False, unique=True)
    capacity = Column(Integer, default=0)
    night_period = Column(String, nullable=True)
    initial_count = Column(Integer, default=0)
    remark = Column(Text, nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    residents = relationship("Person", back_populates="room")
    rois = relationship("ROI", back_populates="room")


class Person(Base):
    __tablename__ = "people"

    id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False)
    photo_path = Column(String, nullable=True)
    remark = Column(Text, nullable=True)
    room_id = Column(String, ForeignKey("rooms.id"), nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    room = relationship("Room", back_populates="residents")
    faces = relationship("FaceFeature", back_populates="person")


class Visitor(Base):
    __tablename__ = "visitors"

    id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False)
    photo_path = Column(String, nullable=True)
    remark = Column(Text, nullable=True)
    valid_from = Column(DateTime, nullable=False)
    valid_to = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class Passerby(Base):
    __tablename__ = "passerbys"

    id = Column(String, primary_key=True, default=default_uuid)
    first_seen = Column(DateTime, default=dt.datetime.utcnow)
    last_seen = Column(DateTime, default=dt.datetime.utcnow)
    seen_count = Column(Integer, default=1)
    camera_id = Column(String, nullable=True)
    remark = Column(Text, nullable=True)


class FaceFeature(Base):
    __tablename__ = "face_features"

    id = Column(String, primary_key=True, default=default_uuid)
    person_id = Column(String, ForeignKey("people.id"), nullable=True)
    visitor_id = Column(String, ForeignKey("visitors.id"), nullable=True)
    passerby_id = Column(String, ForeignKey("passerbys.id"), nullable=True)
    vector = Column(JSONB, nullable=False)
    snapshot_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    person = relationship("Person", back_populates="faces")


class RTSPStream(Base):
    __tablename__ = "rtsp_streams"

    id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    remark = Column(Text, nullable=True)
    location = Column(String, nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    rois = relationship("ROI", back_populates="stream")


class ROI(Base):
    __tablename__ = "rois"

    id = Column(String, primary_key=True, default=default_uuid)
    stream_id = Column(String, ForeignKey("rtsp_streams.id"), nullable=False)
    room_id = Column(String, ForeignKey("rooms.id"), nullable=False)
    polygon = Column(JSONB, nullable=False)
    arrow = Column(JSONB, nullable=False)

    stream = relationship("RTSPStream", back_populates="rois")
    room = relationship("Room", back_populates="rois")


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=default_uuid)
    room_id = Column(String, ForeignKey("rooms.id"))
    type = Column(String, nullable=False)
    payload = Column(JSONB, nullable=True)
    snapshot_path = Column(String, nullable=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)


class Track(Base):
    __tablename__ = "tracks"

    id = Column(String, primary_key=True, default=default_uuid)
    stream_id = Column(String, ForeignKey("rtsp_streams.id"))
    reid = Column(String, nullable=False)
    start_time = Column(DateTime, default=dt.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    person_id = Column(String, ForeignKey("people.id"), nullable=True)
    visitor_id = Column(String, ForeignKey("visitors.id"), nullable=True)
    passerby_id = Column(String, ForeignKey("passerbys.id"), nullable=True)
    remark = Column(Text, nullable=True)

    __table_args__ = {"sqlite_autoincrement": True}
