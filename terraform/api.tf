resource "google_project_service" "services" {
  for_each = toset([
    "artifactregistry.googleapis.com",
    "bigquery.googleapis.com",
    "bigquerystorage.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudscheduler.googleapis.com",
    "iam.googleapis.com",
    "logging.googleapis.com",
    "run.googleapis.com",
    "secretmanager.googleapis.com",
  ])

  service = each.key
}
