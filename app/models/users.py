from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.models import Base 
from werkzeug.security import generate_password_hash, check_password_hash

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(64), default='user')

    slot_users = relationship("SlotUser", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
