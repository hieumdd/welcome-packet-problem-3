select
    id,
    web_id,
    workflow_id,
    create_time,
    start_time,
    status,
    emails_sent,
    send_time,
    report_summary,
    _sys_created_date,
    _sys_created_at,
from {{ source("landing__mailchimp", "emails") }}
qualify row_number() over (partition by id, workflow_id, _sys_created_date order by _sys_created_at desc) = 1
