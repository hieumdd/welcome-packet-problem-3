from typing import TypeVar

from google.cloud import bigquery

client = bigquery.Client()

T = TypeVar("T")


def read(sql: str) -> list[T]:
    rows = client.query(sql).result()
    return [i for i in rows]


def load(dataset_id: str, table_id: str, rows: list[dict]):
    table = client.get_dataset(dataset_id).table(table_id)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
    )
    job = client.load_table_from_json(rows, table, job_config=job_config)
    job.result()
