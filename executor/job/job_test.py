from job.job import get_workflow_ids, create_batch_operation

def test_get_workflow_ids():
    workflow_ids = get_workflow_ids()
    assert workflow_ids

def test_create_batch_operation():
    batch_operation = create_batch_operation()
    assert batch_operation
