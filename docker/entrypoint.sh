#!/usr/bin/env bash
set -eEo pipefail

function error {
    echo "Error; $1"
}


OPTIONS="${RUNNER_OPTIONS:-""}"
# If the user has provided any runner labels add them to the config options
if [[ -n ${RUNNER_LABELS} ]]; then
    OPTIONS="${OPTIONS} --labels ${RUNNER_LABELS}"
fi

# The runner group that the self-hosted runner will be registered with
GROUP=${RUNNER_GROUP:-"default"}

echo "Configuring GitHub Actions Runner and registering"
./config.sh \
    --unattended \
    --url "${RUNNER_URL}" \
    --token "${TOKEN}" \
    --name "${RUNNER_NAME}" \
    --work ${RUNNER_WORK_DIRECTORY} \
    --runnergroup ${GROUP} \
    $OPTIONS

echo "Starting GitHub Actions Runner"
env -i ./runsvc.sh

# Deregister
echo Cleaning up runner registration...
./config.sh remove --token "${TOKEN}"
