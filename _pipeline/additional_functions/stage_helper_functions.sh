#!/bin/bash

function create_newrelic_alerts {
  echo "Running New Relic alerts"
  local tf_cmd="${1}"
  local tf_dir="${2}"
  local tf_statefile_name="${3}"

  export NEW_RELIC_API_KEY=$(config_get_bnw_secret '.newrelic.api_key' 'secrets-jenkins')
  export NEW_RELIC_REGION=US
  export NEW_RELIC_ACCOUNT_ID=135555
  export SLACK_CHANNEL_WEBHOOK=$(config_get_bnw_secret '.it_crowd.url' 'secrets-slack-webhooks')
  export SLACK_CHANNEL_NAME="#pest-alerts"

cat << EOF > "$tf_dir/terraform.tfvars"
slack_channel_webhook="$SLACK_CHANNEL_WEBHOOK"
slack_channel_name="$SLACK_CHANNEL_NAME"
EOF

  run_terraform_in_bnw "$tf_cmd" "$tf_dir" "$tf_statefile_name"
  rm -f "$tf_dir/terraform.tfvars"
  unset NEW_RELIC_API_KEY NEW_RELIC_REGION NEW_RELIC_ACCOUNT_ID SLACK_CHANNEL_WEBHOOK SLACK_CHANNEL_NAME
  echo "Finished applying New Relic alerts"
}
