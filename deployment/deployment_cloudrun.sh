#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

gcloud beta run jobs create ${JOB_NAME} \
    --image=${IMAGE_URL}:${IMAGE_TAG} \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --max-retries=0 \
    --args=store_list,category_list \
    