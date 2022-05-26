terraform {
  required_providers {
    newrelic = {
      source  = "newrelic/newrelic"
      version = "~> 2.25"
    }
  }
  backend "s3" {}
  required_version = ">= 1.0"
}
