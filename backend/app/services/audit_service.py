import logging
from datetime import UTC, datetime

from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.core.config import settings
from app.schemas.ticket import TicketStatus

logger = logging.getLogger(__name__)


class AuditService:
    def __init__(self) -> None:
        self.enabled = settings.mongo_audit_enabled

    def record_ticket_status_change(
        self,
        *,
        ticket_id: int,
        customer_id: int,
        previous_status: TicketStatus,
        new_status: TicketStatus,
        user: str = "system",
    ) -> None:
        if not self.enabled:
            return

        event = {
            "ticket_id": ticket_id,
            "customer_id": customer_id,
            "action": "ticket.status_changed",
            "previous_status": previous_status.value,
            "new_status": new_status.value,
            "user": user,
            "occurred_at": datetime.now(UTC),
        }

        client: MongoClient | None = None

        try:
            client = MongoClient(
                settings.mongo_url,
                serverSelectionTimeoutMS=1000,
                connectTimeoutMS=1000,
            )
            collection = client[settings.mongo_database][settings.mongo_audit_collection]
            collection.insert_one(event)
        except PyMongoError:
            logger.warning("Could not write ticket audit event", exc_info=True)
        finally:
            if client is not None:
                client.close()
