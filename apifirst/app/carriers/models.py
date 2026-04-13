"""SQLAlchemy model for carriers."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from ..auth.models import Base


class Carrier(Base):
    __tablename__ = "carriers"
    __table_args__ = (UniqueConstraint("code", name="uq_carrier_code"),)

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(16), nullable=False, unique=True, index=True)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    shipments = relationship("Shipment", back_populates="carrier")