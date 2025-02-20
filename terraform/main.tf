terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.14.1"
    }
  }
  backend "gcs" {
    credentials = "./service-account.json"
    bucket      = "305314978193-terraform"
  }
}

provider "google" {
  credentials = file("./service-account.json")
  project     = "satori-test-10-451404"
}

data "google_project" "project" {
}
