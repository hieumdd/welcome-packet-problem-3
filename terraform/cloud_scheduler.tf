resource "google_cloud_scheduler_job" "ingestion_mailchimp" {
  depends_on = [
    google_cloud_run_v2_job.ingestion_mailchimp,
  ]

  name             = "ingestion--mailchimp"
  paused           = false
  schedule         = "0 */4 * * *"
  attempt_deadline = "15s"
  region           = "us-central1"
  http_target {
    http_method = "POST"
    uri         = "https://${google_cloud_run_v2_job.ingestion_mailchimp.location}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${data.google_project.project.number}/jobs/${google_cloud_run_v2_job.ingestion_mailchimp.name}:run"
    oauth_token {
      service_account_email = google_service_account.welcome_packet_3.email
    }
  }
}
