"""main.py"""

from google.cloud import run_v2

PROJECT_ID = "daifuku-development"
LOCATION = "asia-northeast1"
JOBS = "jobs-sample"


def main() -> None:
    client = run_v2.JobsClient()

    request = run_v2.RunJobRequest(
        name=f"projects/{PROJECT_ID}/locations/{LOCATION}/jobs/{JOBS}",
        overrides={
            "container_overrides": [
                {
                    "args":
                        [
                            "--store_list=[111, 122]",
                            '--category_list=["333", "444"]',
                        ],
                },
            ],
        }
    )
    operation = client.run_job(request=request)
    print("Waiting for operation to complete...")

    response = operation.result()
    print(response)


if __name__ == "__main__":
    main()
