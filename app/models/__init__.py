from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .service import Service
from .slot import Slot
from .slot_user import SlotUser