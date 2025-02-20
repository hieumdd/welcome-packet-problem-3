from typing import TypedDict

import httpx

from logger import get_logger
from config import MAILCHIMP_API_KEY

logger = get_logger(__name__)

client = httpx.Client(
    base_url="https://us20.api.mailchimp.com/3.0",
    headers={"Authorization": f"Bearer {MAILCHIMP_API_KEY}"},
)


class Operation(TypedDict):
    method: str
    path: str
    operation_id: str


class BatchOperation(TypedDict):
    id: str
    status: str
    total_operations: int
    finished_operations: int
    errored_operations: int
    submitted_at: str
    completed_at: str
    response_body_url: str


def build_list_automated_emails_operation(workflow_id: str) -> Operation:
    return Operation(
        method="GET",
        path=f"/automations/${workflow_id}/emails",
        operation_id=workflow_id,
    )


def start_batch_operation(operations: list[Operation]):
    logger.debug(f"Creating ${len(operations)}")
    response = client.request(
        method="POST",
        url="/batches",
        json={"operations": operations},
    )
    response_data: BatchOperation = response.json()
    total_operations = response_data["total_operations"]
    logger.debug(f"Created {total_operations} / ${len(operations)} Operations")
    return response_data


def get_batch_operation(operation_id: str):
    response = client.request(method="GET", url=f"/batches/{operation_id}")
    response_data: BatchOperation = response.json()
    return response_data
