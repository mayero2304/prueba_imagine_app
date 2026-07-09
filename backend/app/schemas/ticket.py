from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class TicketStatus(str, Enum):
    PENDING = "Pendiente"
    IN_PROGRESS = "En progreso"
    FINISHED = "Finalizado"


class TicketBase(BaseModel):
    customer_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=160)
    description: str = Field(min_length=1)
    status: TicketStatus = TicketStatus.PENDING


class TicketCreate(TicketBase):
    pass


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketRead(TicketBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
