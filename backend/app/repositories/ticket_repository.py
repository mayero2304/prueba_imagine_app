from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket
from app.schemas.ticket import TicketCreate, TicketStatus


class TicketRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Ticket]:
        statement = select(Ticket).order_by(Ticket.id)
        return list(self.db.scalars(statement).all())

    def get(self, ticket_id: int) -> Ticket | None:
        return self.db.get(Ticket, ticket_id)

    def create(self, data: TicketCreate) -> Ticket:
        payload = data.model_dump()
        payload["status"] = data.status.value
        ticket = Ticket(**payload)
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def update_status(self, ticket: Ticket, status: TicketStatus) -> Ticket:
        ticket.status = status.value
        self.db.commit()
        self.db.refresh(ticket)
        return ticket
