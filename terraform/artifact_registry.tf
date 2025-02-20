resource "google_artifact_registry_repository" "docker_1" {
  location               = "us-central1"
  repository_id          = "docker-1"
  format                 = "DOCKER"
  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "delete-untagged"
    action = "DELETE"
    condition {
      tag_state = "UNTAGGED"
    }
  }
}
