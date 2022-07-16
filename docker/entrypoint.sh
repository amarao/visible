#!/usr/bin/env bash
set -eEo pipefail

function error {
    echo "Error; $1"
}

if [[ -z $ORG ]]; then
    echo ORG should point to GH organization name
fi

if [[ -z APP_TOKEN ]]; then
    echo $TOKEN should contain application access token or PAT

OPTIONS="${RUNNER_OPTIONS:-""}"
# If the user has provided any runner labels add them to the config options
if [[ -n ${RUNNER_LABELS} ]]; then
    OPTIONS="${OPTIONS} --labels ${RUNNER_LABELS}"
fi

# The runner group that the self-hosted runner will be registered withV
GROUP=${RUNNER_GROUP:-"default"}

REG_TOKEN = $(curl -s -X POST -H "Accept: application/vnd.github+json" -H "Authorization: token ${TOKEN}" https://api.github.com/orgs/${ORG}/actions/runners/registration-token|jq -r .token)

echo "Configuring GitHub Actions Runner and registering"
./config.sh \
    --unattended \
    --url https://github.com/${ORG} \
    --token "${REG_TOKEN}" \
    --name "${RUNNER_NAME}" \
    --work ${RUNNER_WORK_DIRECTORY} \
    --runnergroup ${GROUP} \
    $OPTIONS

echo "Starting GitHub Actions Runner"
env -i ./runsvc.sh

# Deregister
echo Cleaning up runner registration...
./config.sh remove --token "${REG_TOKEN}"
