resource "google_cloud_scheduler_job" "mailchimp_ingestion" {
  depends_on = [
    google_cloud_run_v2_job.mailchimp_ingestion,
  ]

  name             = "mailchimp--ingestion"
  paused           = false
  schedule         = "0 */4 * * *"
  attempt_deadline = "15s"
  region           = "us-central1"
  http_target {
    http_method = "POST"
    uri         = "https://${google_cloud_run_v2_job.mailchimp_ingestion.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${data.google_project.project.number}/jobs/${google_cloud_run_v2_job.mailchimp_ingestion.name}:run"
    oauth_token {
      service_account_email = google_service_account.welcome_packet_3.email
    }
  }
}
