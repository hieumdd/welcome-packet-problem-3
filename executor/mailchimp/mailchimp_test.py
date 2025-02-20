from mailchimp.mailchimp import (
    build_list_automated_emails_operation,
    start_batch_operation,
)


def test_start_batch_operation():
    workflow_ids = [
        "0f1a9a57f2",
        "cc5472e84a",
        "53e8f0f9cf",
        "689f1ea255",
        "d283b7c949",
    ]
    operations = list(map(build_list_automated_emails_operation, workflow_ids))
    try:
        batch_operation = start_batch_operation(operations)
        assert batch_operation["id"]
    except Exception as e:
        raise e
