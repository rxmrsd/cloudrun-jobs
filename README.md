# Cloud Run Jobsの引数にリストを与える

## はじめに

最近業務でCloud Run Jobsを使うことがあり，その際引数にリストを与えたいというシーンがありました．その時ほんの少しだけ工夫が必要でしたのでその旨を記載します．

## Cloud Run Jobsとは

Cloud Run JobsはCloud Runの機能の一つで，手動実行や，スケジュール設定による定期実行をすることが可能です．

https://cloud.google.com/run/docs/create-jobs?hl=ja

## お題

下記のPythonコードを実行するJobsを作成します．

```python:main.py
"""main.py"""
import json
import logging

import click

logging.basicConfig(level=logging.INFO)


@click.command()
@click.option(
    "--temp_list1",
    type=str,
    required=True,
)
@click.option(
    "--temp_list2",
    type=str,
    required=True,
)
def main(temp_list1: str, temp_list2: str) -> None:
    logging.info(f"{temp_list1}: type: {type(temp_list1)}")
    logging.info(f"{temp_list2}: type: {type(temp_list2)}")

    _temp_list1 = json.loads(temp_list1)
    for _temp in _temp_list1:
        logging.info(f"{_temp}: type: {type(_temp)}")
    _temp_list2 = json.loads(temp_list2)
    for _temp in _temp_list2:
        logging.info(f"{_temp}: type: {type(_temp)}")


if __name__ == "__main__":
    main()

```

シンプルに，引数に2つのリスト(`temp_list1`, `temp_list2`)を与えてそれを表示するものです．


## デプロイ
こちらの構成で，以下2つのことを行ないます．
- ArtifactRegistryにイメージをデプロイ
```bash:deployment_component.sh
#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

docker build -t ${JOB_NAME}:latest -f Dockerfile . --platform linux/amd64

# push image to Artifact Registory
docker tag ${JOB_NAME}:latest ${IMAGE_URL}:${IMAGE_TAG}
docker push ${IMAGE_URL}:${IMAGE_TAG}
```

- Cloud Run Jobsを作成
Jobsの引数に`temp_list1`と`temp_list2`を与えるようにします．

```bash:deployment_cloudrun.sh
#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

gcloud beta run jobs create ${JOB_NAME} \
    --image=${IMAGE_URL}:${IMAGE_TAG} \
    --project=${PROJECT_ID} \
    --region=${REGION} \
    --max-retries=0 \
    --args=temp_list1,temp_list2 \
```

## 実行
以下コマンドにてJobsを実行します．
```bash:job_run.sh
#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

gcloud beta run jobs execute ${JOB_NAME} \
    --project ${PROJECT_ID} \
    --region ${REGION} \
    --args='^:^--temp_list1=[269, 270]:--temp_list2=["136_1", "90_1"]'
```

ポイントは引数の部分です．
```bash
--args='^:^--temp_list1=[269, 270]:--temp_list2=["136_1", "90_1"]'
```


### カンマをエスケープする
以下のように記述して実行するとエラーとなります．
```bash
#!/usr/bin/env bash
export $(cat ./deployment/.env | xargs)

gcloud beta run jobs execute ${JOB_NAME} \
    --project ${PROJECT_ID} \
    --region ${REGION} \
    --args='--temp_list1=[269, 270],--temp_list2=["136_1", "90_1"]'
```
理由はカンマにあります．Jobsを実行する際，`temp_list1=[269, 270]`のように，リスト内にカンマが含まれます．このカンマと引数と引数の間にあるカンマが混在しているため，コマンド側が識別できないようです．
そこで，引数間を区切るカンマを別の文字に置き換えます．上記では`:`に置き換えており，そのことを明示するため冒頭に`^:^`をおまじないとして記載します．これでカンマを識別できるようになり，リスト形式の引数を与えることができます．

無事ログに値が表示されています．↓

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3618319/0f348616-c301-7f33-a973-72a87420b5ec.png)


## スケジュールには引数が設定できない？
私が調べた限り(2024/03/30時点)ですが，Cloud Run Jobsのスケジューラ トリガーに引数を与えることができませんでした．Dockerイメージは共通で外部からの引数でJobを切り分け，それらを定期実行する想定をしていたのですが，このサービスを使うことができませんでした．

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/3618319/6158a8e3-7d09-64d4-d6b5-d4dbe50f0127.png)

代替案として考えたのは，以下です．
- 引数はConfigファイルとしてStorageに格納し，それを読み込むようにする
- Cloud FunctionsとCloud Schedulerを組み合わせ，clientライブラリで実行する(こんな感じ↓)
```python
def main() -> None:
    client = run_v2.JobsClient()

    request = run_v2.RunJobRequest(
        name=f"projects/{PROJECT_ID}/locations/{LOCATION}/jobs/{JOBS}",
        overrides={
            "container_overrides": [
                {
                    "args":
                        [
                            "--temp_list1=[111, 122]",
                            '--temp_list2=["333", "444"]',
                        ],
                },
            ],
        }
    )
    operation = client.run_job(request=request)
```


## まとめ

本記事では，Cloud Run Jobsの引数にリストを与えるときに行なった対応を記載しました．  
全体のファイルは[こちら](https://github.com/rxmrsd/cloudrun-jobs)に公開しております．




## 参考
- [Cloud Run jobs を徹底解説！](https://blog.g-gen.co.jp/entry/cloud-run-jobs-explained)
- [カンマをエスケープする](https://cloud.google.com/sdk/gcloud/reference/topic/escaping)