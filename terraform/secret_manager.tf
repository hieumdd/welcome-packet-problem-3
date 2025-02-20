resource "google_secret_manager_secret" "mailchimp_api_key" {
  secret_id = "MAILCHIMP_API_KEY"
  replication {
    auto {}
  }
}
