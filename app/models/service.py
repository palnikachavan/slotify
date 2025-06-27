from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from app.models import Base  # shared Base

class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    
    slot_users = relationship("SlotUser", back_populates="service")

    
    def __repr__(self):
        return f"<Service(id={self.id}, name={self.name})>"
