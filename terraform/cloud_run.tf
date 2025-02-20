resource "google_cloud_run_v2_job" "mailchimp_ingestion" {
  depends_on = [
    google_bigquery_dataset.landing__mailchimp,
    google_service_account.welcome_packet_3,
    google_project_iam_member.welcome_packet_3,
    google_secret_manager_secret.mailchimp_api_key,
    google_artifact_registry_repository.docker_1,
  ]
  deletion_protection = false

  name     = "mailchimp--ingestion"
  location = "us-central1"
  template {
    template {
      execution_environment = "EXECUTION_ENVIRONMENT_GEN2"
      timeout               = "900s"
      max_retries           = 0
      service_account       = google_service_account.welcome_packet_3.email
      containers {
        image = "${google_artifact_registry_repository.docker_1.location}-docker.pkg.dev/${data.google_project.project.project_id}/${google_artifact_registry_repository.docker_1.name}/mailchimp--ingestion:latest"
        resources {
          limits = {
            "cpu"    = "1"
            "memory" = "1024Mi"
          }
        }
        args = ["job.py"]
        env {
          name = "MAILCHIMP_API_KEY"
          value_source {
            secret_key_ref {
              secret  = google_secret_manager_secret.mailchimp_api_key.secret_id
              version = "latest"
            }
          }
        }
      }
    }
  }
}
