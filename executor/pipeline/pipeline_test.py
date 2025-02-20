from mailchimp.mailchimp import get_batch_operation
from pipeline.pipeline import (
    create_batch_operation_response,
    handle_batch_operation_webhook,
)


def test_create_batch_operation_response():
    with open("response.tar.gz", "rb") as f:
        data = create_batch_operation_response(f)
    assert data


def test_handle_batch_operation_webhook():
    batch_operation = get_batch_operation("l8gil363ae")
    handle_batch_operation_webhook(batch_operation["response_body_url"])
