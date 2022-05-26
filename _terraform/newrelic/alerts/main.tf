module "newrelic" {
  source = "https://terraform-modules-master-2749785-0-live-base-eu-west-1.s3-eu-west-1.amazonaws.com/bnw-newrelic-container-2.zip"

  # Standard BNW variables
  app_name    = var.app_name
  region      = var.region
  branch      = var.branch_name
  environment = var.environment
  ou          = var.ou

  # Configuration for CPU threshold alerts
  cpu_threshold_operator           = "above"
  cpu_threshold_critical_threshold = 40
  cpu_threshold_warning_threshold  = 30
  cpu_threshold_critical_duration  = 900
  cpu_threshold_warning_duration   = 1800

  # Configuration for CPU anomaly alerts
  cpu_anomaly_baseline_direction = "upper_and_lower"
  cpu_anomaly_operator           = "above"
  cpu_anomaly_critical_threshold = 50
  cpu_anomaly_warning_threshold  = 50
  cpu_anomaly_critical_duration  = 900
  cpu_anomaly_warning_duration   = 1800

  # Configuration for RAM threshold alerts
  memory_threshold_operator           = "above"
  memory_threshold_critical_threshold = 75
  memory_threshold_warning_threshold  = 65
  memory_threshold_critical_duration  = 900
  memory_threshold_warning_duration   = 1800

  # Configuration for RAM anomaly alerts
  memory_anomaly_baseline_direction = "upper_and_lower"
  memory_anomaly_operator           = "above"
  memory_anomaly_critical_threshold = 50
  memory_anomaly_warning_threshold  = 50
  memory_anomaly_critical_duration  = 900
  memory_anomaly_warning_duration   = 1800

  # Configuration for minimum running containers alert
  # APP_HA_L7_CONTAINER_NODES_DESIRED: '3' desired min is 3
  minimum_running_containers_operator           = "below"
  minimum_running_containers_critical_threshold = 3
  minimum_running_containers_warning_threshold  = 3
  minimum_running_containers_critical_duration  = 600
  minimum_running_containers_warning_duration   = 1200

  # Configuration for maximum running containers alert
  # APP_HA_L7_CONTAINER_NODES_MAX: '6' max can go upto 6
  maximum_running_containers_operator           = "above"
  maximum_running_containers_critical_threshold = 6
  maximum_running_containers_warning_threshold  = 6
  maximum_running_containers_critical_duration  = 600
  maximum_running_containers_warning_duration   = 1200

  # Configuration for notifications
  slack_channel_name    = var.slack_channel_name
  slack_channel_webhook = var.slack_channel_webhook
}

resource "newrelic_alert_policy_channel" "example_alert_slack" {
  policy_id = module.newrelic.alert_policy_id
  # If you also configured email alerts here, you need to add that to this array, e.g:
  # channel_ids = [module.newrelic_instance_alerts.alerts_slack_channel.0.id,channel_ids = [module.newrelic_instancr_alerts.alerts_email.0.id]]
  channel_ids = [module.newrelic.alerts_slack_channel.0.id]
}
