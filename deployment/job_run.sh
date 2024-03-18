#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

gcloud beta run jobs execute ${JOB_NAME} \
    --project ${PROJECT_ID} \
    --region ${REGION} \
    --args='^:^--store_list=[269,270]:--category_list=["136_1", "90_1"]'