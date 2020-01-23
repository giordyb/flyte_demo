#!/usr/bin/env bash
set -e

GIT_SHA=$(git rev-parse HEAD)
IMAGE_TAG_WITH_SHA="${IMAGE_NAME}:${GIT_SHA}"
echo $IMAGE_TAG_WITH_SHA
docker run --network host -e FLYTE_PLATFORM_URL='127.0.0.1:30081' $IMAGE_TAG_WITH_SHA pyflyte -p flytedemo -d development -c tasks_and_workflow.config register workflows
docker run --network host -e FLYTE_PLATFORM_URL='127.0.0.1:30081' $IMAGE_TAG_WITH_SHA pyflyte -p flytedemo -d development -c workflow.config register workflows