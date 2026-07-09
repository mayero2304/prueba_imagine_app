from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket import TicketCreate, TicketStatus
from app.services.exceptions import NotFoundError


class TicketService:
    def __init__(self, db: Session) -> None:
        self.customer_repository = CustomerRepository(db)
        self.ticket_repository = TicketRepository(db)

    def list_tickets(self):
        return self.ticket_repository.list()

    def create_ticket(self, data: TicketCreate):
        if self.customer_repository.get(data.customer_id) is None:
            raise NotFoundError("Customer not found")

        return self.ticket_repository.create(data)

    def update_status(self, ticket_id: int, status: TicketStatus):
        ticket = self.ticket_repository.get(ticket_id)

        if ticket is None:
            raise NotFoundError("Ticket not found")

        return self.ticket_repository.update_status(ticket, status)
