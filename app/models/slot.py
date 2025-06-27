from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base 

class Slot(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_booked = Column(Boolean, default=False)

    service = relationship("Service", backref="slots")
    slot_users = relationship("SlotUser", back_populates="slot")

    def __repr__(self):
        return f"<Slot(id={self.id}, start={self.start_time}, booked={self.is_booked})>"
