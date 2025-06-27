from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base 

class SlotUser(Base):
    __tablename__ = 'slot_users'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    slot_id = Column(Integer, ForeignKey('slots.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)

    user = relationship("User", back_populates="slot_users")
    service = relationship("Service", back_populates="slot_users")
    slot = relationship("Slot", back_populates="slot_users")
