from logger import get_logger
from bigquery import read
from mailchimp.mailchimp import build_list_automated_emails_operation, start_batch_operation

logger = get_logger(__name__)

def get_workflow_ids():
    logger.debug('Getting Workflow IDs')
    sql = 'select id from mailchimp_data_amc.automations qualify row_number() over (partition by id order by _sdc_batched_at desc) = 1'
    workflows = read(sql)
    logger.debug(f"Got {len(workflows)} workflows")
    return [i["id"] for i in workflows]

def create_batch_operation():
    logger.info("Creating Batch Operation")
    workflow_ids = get_workflow_ids()
    operations =[build_list_automated_emails_operation(w) for w in workflow_ids]
    batch_operation = start_batch_operation(operations)
    logger.info(f"Created Batch Operation ID {batch_operation['id']}", {"batch_operation": batch_operation})
