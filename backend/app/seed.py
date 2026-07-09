from app.core.database import SessionLocal, init_db
from app.models.customer import Customer
from app.models.ticket import Ticket
from app.schemas.ticket import TicketStatus


def run_seed() -> None:
    init_db()

    with SessionLocal() as db:
        db.query(Ticket).delete()
        db.query(Customer).delete()
        db.commit()

        customers = [
            Customer(
                name="Ana Gomez",
                email="ana.gomez@example.com",
                company="Imagine",
            ),
            Customer(
                name="Carlos Perez",
                email="carlos.perez@example.com",
                company="Finanz",
            ),
            Customer(
                name="Laura Martinez",
                email="laura.martinez@example.com",
                company="Acme Support",
            ),
        ]

        db.add_all(customers)
        db.commit()

        for customer in customers:
            db.refresh(customer)

        tickets = [
            Ticket(
                customer_id=customers[0].id,
                title="No puedo iniciar sesion",
                description="El cliente reporta error al ingresar a la plataforma.",
                status=TicketStatus.PENDING.value,
            ),
            Ticket(
                customer_id=customers[1].id,
                title="Actualizar datos de empresa",
                description="Solicita cambiar la razon social registrada.",
                status=TicketStatus.IN_PROGRESS.value,
            ),
        ]

        db.add_all(tickets)
        db.commit()


if __name__ == "__main__":
    run_seed()
    print("Seed data loaded.")
