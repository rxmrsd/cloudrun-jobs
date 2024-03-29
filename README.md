# シンプルなCloud Run Jobs

## Jobの実行
```yaml
#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

gcloud beta run jobs execute ${JOB_NAME} \
    --project ${PROJECT_ID} \
    --region ${REGION} \
    --args='^:^--temp_list1=[269, 270]:--temp_list2=["136_1", "90_1"]'
```