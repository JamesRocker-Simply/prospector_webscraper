variable "app_name" {
  type        = string
  description = "Name of application"
}

variable "region" {
  type = string
}

variable "branch_name" {
  type        = string
  description = "branch name (e.g. `master`)"
}

variable "environment" {
  type        = string
  description = "environment (e.g. `dev`, `live`)"
}

variable "ou" {
  type        = string
  description = "ou (e.g. `prod`, `dev`, `staging`)"
}

variable "slack_channel_name" {
 type = string
}

variable "slack_channel_webhook" {
 type = string
}
