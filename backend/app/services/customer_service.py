from sqlalchemy.orm import Session

from app.repositories.customer_repository import CustomerRepository
from app.schemas.customer import CustomerCreate
from app.services.exceptions import ConflictError, NotFoundError


class CustomerService:
    def __init__(self, db: Session) -> None:
        self.repository = CustomerRepository(db)

    def list_customers(self):
        return self.repository.list()

    def get_customer(self, customer_id: int):
        customer = self.repository.get(customer_id)

        if customer is None:
            raise NotFoundError("Customer not found")

        return customer

    def create_customer(self, data: CustomerCreate):
        if self.repository.get_by_email(data.email) is not None:
            raise ConflictError("Customer email already exists")

        return self.repository.create(data)
