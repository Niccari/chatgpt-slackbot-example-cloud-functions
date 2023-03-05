from logging import DEBUG, INFO
import os


class Config:
    CLOUD_TASKS_QUEUE_NAME = "chatgpt-dispatcher"

    PROJECT_ID = os.environ["PROJECT_ID"]
    REGION = os.environ["REGION"]
    FUNCTIONS_URL = os.environ["FUNCTIONS_URL"]
    OIDC_TOKEN_SERVICE_ACCOUNT = os.environ.get("OIDC_TOKEN_SERVICE_ACCOUNT")

    if "K_SERVICE" in os.environ:
        IS_CLOUD = True
        LOG_LEVEL = INFO

        CLOUD_TASKS_EMULATOR_HOST = None
    else:
        IS_CLOUD = False
        LOG_LEVEL = DEBUG

        CLOUD_TASKS_EMULATOR_HOST = \
            os.environ.get("CLOUD_TASKS_EMULATOR_HOST", "127.0.0.1:9091")
