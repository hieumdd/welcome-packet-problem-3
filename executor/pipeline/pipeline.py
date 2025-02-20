from io import BytesIO
from typing import TypedDict
import gzip
import json
import tarfile

from pydantic import BaseModel, Field
import httpx
import pendulum

from config import DATASET_ID, TABLE_ID
from logger import get_logger
from bigquery import load

logger = get_logger(__name__)


class BatchOperationResponse(TypedDict):
    operation_id: str
    response: str
    status_code: int


def create_batch_operation_response(fo: BytesIO):
    responses = []
    with gzip.GzipFile(fileobj=fo, mode="rb") as gunzipped:
        with tarfile.open(fileobj=gunzipped, mode="r|*") as tar:
            for file_ in tar:
                if not file_.name.endswith(".json"):
                    continue
                file_content = tar.extractfile(file_)
                content = file_content.read().decode("utf-8")
                rows: list[BatchOperationResponse] = json.loads(content)
                success_rows = [row for row in rows if row.get("status_code") == 200]
                for row in success_rows:
                    responses.append(json.loads(row["response"]))
                logger.debug(
                    f"Got {len(success_rows)} / {len(rows)} rows for file {file_.name}"
                )
    logger.debug("Finished parsing .tar.gz file")
    return responses


def parse_response(responses: list[dict]):
    return [email for response in responses for email in response["emails"]]


def transform(emails: list[dict]):
    class Email(BaseModel):
        class ReportSummary(BaseModel):
            opens: int
            unique_opens: int
            open_rate: float
            clicks: int
            subscriber_clicks: int
            click_rate: float

        id: str
        web_id: int
        workflow_id: str
        create_time: str
        start_time: str | None = Field(default_factory=lambda x: None if x == "" else x)
        status: str
        emails_sent: int
        send_time: str | None = Field(default_factory=lambda x: None if x == "" else x)
        report_summary: ReportSummary | None = Field(None)
        sys_created_date: str = Field(
            default_factory=lambda: pendulum.now("UTC").to_date_string(),
            serialization_alias="_sys_created_date",
        )
        sys_created_at: str = Field(
            default_factory=lambda: pendulum.now("UTC").format("YYYY-MM-DDTHH:mm:ssZ"),
            serialization_alias="_sys_created_at",
        )

    return [Email.model_validate(email).model_dump(by_alias=True) for email in emails]


def handle_batch_operation_webhook(url: str):
    logger.info("Extracting Batch Operation Response", {"url": url})

    response = httpx.request(method="GET", url=url)
    response.raise_for_status()
    fo = BytesIO(response.content)

    responses = create_batch_operation_response(fo)
    emails = parse_response(responses)
    rows = transform(emails)
    load(DATASET_ID, TABLE_ID, rows)

    logger.info("ETL Batch Operation Response Completed", {"url": url})
