resource "google_service_account" "welcome_packet_3" {
  account_id = "welcome-packet-3"
}

resource "google_project_iam_member" "welcome_packet_3" {
  for_each = toset([
    "roles/artifactregistry.writer",
    "roles/bigquery.dataEditor",
    "roles/bigquery.jobUser",
    "roles/bigquery.user",
    "roles/iam.serviceAccountUser",
    "roles/run.admin",
    "roles/secretmanager.secretAccessor",
  ])

  project = data.google_project.project.id
  role    = each.key
  member  = google_service_account.welcome_packet_3.member
}

