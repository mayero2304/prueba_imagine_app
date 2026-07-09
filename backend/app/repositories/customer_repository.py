from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


class CustomerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Customer]:
        statement = select(Customer).order_by(Customer.id)
        return list(self.db.scalars(statement).all())

    def get(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        statement = select(Customer).where(Customer.email == email)
        return self.db.scalars(statement).first()

    def create(self, data: CustomerCreate) -> Customer:
        customer = Customer(**data.model_dump())
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
