"""SQLAlchemy models for shipments and related entities."""

from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Table,
    JSON,
)
from sqlalchemy.orm import relationship

from ..auth.models import Base, User
from ..carriers.models import Carrier


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    shipments = relationship("Shipment", secondary="shipment_tags", back_populates="tags")


class ShipmentTag(Base):
    __tablename__ = "shipment_tags"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)


class Follower(Base):
    __tablename__ = "followers"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)
    email = Column(String(255), nullable=False)
    added_by_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="followers")
    added_by = relationship(User)


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    reference = Column(String(64), unique=True, nullable=False)
    container_number = Column(String(64), index=True, nullable=False)
    booking_number = Column(String(64), nullable=True)
    carrier_id = Column(Integer, ForeignKey("carriers.id"), nullable=True)
    external_shipment_id = Column(String(64), nullable=True)
    status = Column(String(32), default="created")
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    carrier = relationship(Carrier, back_populates="shipments")
    created_by = relationship(User)
    tags = relationship("Tag", secondary="shipment_tags", back_populates="shipments")
    followers = relationship("Follower", back_populates="shipment")
    routes = relationship("Route", back_populates="shipment")
    tracking_events = relationship("TrackingHistory", back_populates="shipment")


class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)
    geojson = Column(JSON, nullable=True)
    received_at = Column(DateTime, default=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="routes")


class TrackingHistory(Base):
    __tablename__ = "tracking_history"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("shipments.id", ondelete="CASCADE"), nullable=False)
    event_time = Column(DateTime, nullable=False)
    event_type = Column(String(64), nullable=False)
    location = Column(String(255), nullable=True)
    details = Column(String(255), nullable=True)
    raw_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    shipment = relationship("Shipment", back_populates="tracking_events")