#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

docker build -t ${JOB_NAME}:latest -f Dockerfile . --platform linux/amd64
IMAGE_NAME=${IMAGE_URL}

# push image to Artifact Registory
docker tag ${JOB_NAME}:latest ${IMAGE_NAME}:${IMAGE_TAG}
docker push ${IMAGE_NAME}:${IMAGE_TAG}