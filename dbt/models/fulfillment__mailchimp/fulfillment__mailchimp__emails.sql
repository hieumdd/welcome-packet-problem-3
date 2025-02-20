with
external__mailchimp__automations as (
  select
    id,
    settings.from_name,
    settings.title,
  from {{ source("external__mailchimp", "automations") }}
  qualify row_number() over (partition by id order by _sdc_batched_at desc) = 1
),
staging__mailchimp__emails as (
  select * from {{ ref("staging__mailchimp__emails") }}
),
calendar as (
  select date
  from unnest(GENERATE_DATE_ARRAY(
    (select min(_sys_created_date) from staging__mailchimp__emails),
    (select max(_sys_created_date) from staging__mailchimp__emails)
  )) date
),
dimensions as (
  select
    calendar.date,
    external__mailchimp__automations.id as workflow_id,
    external__mailchimp__automations.from_name as workflow_from_name,
    external__mailchimp__automations.title as workflow_title,
  from calendar
  cross join external__mailchimp__automations
),
fct_emails_cumulative as (
  select
    dimensions.date,
    dimensions.workflow_from_name,
    dimensions.workflow_title,
    staging__mailchimp__emails.workflow_id,
    staging__mailchimp__emails.id,
    staging__mailchimp__emails.emails_sent,
    staging__mailchimp__emails.report_summary.opens as emails_opens,
    lag(staging__mailchimp__emails.report_summary.opens) over (last_1d) as emails_opens_last_1d,
    staging__mailchimp__emails.report_summary.unique_opens as emails_unique_opens,
    lag(staging__mailchimp__emails.report_summary.unique_opens) over (last_1d) as emails_unique_opens_last_1d,
    staging__mailchimp__emails.report_summary.clicks as emails_clicks,
    lag(staging__mailchimp__emails.report_summary.clicks) over (last_1d) as emails_clicks_last_1d,
    staging__mailchimp__emails.report_summary.subscriber_clicks as emails_subscriber_clicks,
    lag(staging__mailchimp__emails.report_summary.subscriber_clicks) over (last_1d) as emails_subscriber_clicks_last_1d,
  from dimensions
  left join staging__mailchimp__emails
    on dimensions.date = staging__mailchimp__emails._sys_created_date
    and dimensions.workflow_id = staging__mailchimp__emails.workflow_id
  window last_1d as (partition by staging__mailchimp__emails.workflow_id, staging__mailchimp__emails.id order by dimensions.date)
)
select
  date,
  workflow_from_name,
  workflow_title,
  workflow_id,
  id,
  emails_sent,
  emails_opens - emails_opens_last_1d as emails_opens,
  emails_opens as total_emails_opens,
  emails_unique_opens - emails_unique_opens_last_1d as emails_unique_opens,
  emails_unique_opens as total_emails_unique_opens,
  emails_clicks - emails_clicks_last_1d as emails_clicks,
  emails_clicks as total_emails_clicks,
  emails_subscriber_clicks - emails_subscriber_clicks_last_1d as emails_subscriber_clicks,
  emails_subscriber_clicks as total_emails_subscriber_clicks,
from fct_emails_cumulative
where
  1 = 1
  and emails_opens_last_1d is not null
  and emails_unique_opens_last_1d is not null
  and emails_clicks_last_1d is not null
  and emails_subscriber_clicks_last_1d is not null
