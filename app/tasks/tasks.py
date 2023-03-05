import json
import traceback

from google.cloud.tasks_v2 import CloudTasksClient, Task
from google.cloud.tasks_v2.services.cloud_tasks.transports \
    import CloudTasksGrpcTransport
import grpc

from app.logger.interface import Logger


class TasksClient:
    def __init__(
        self,
        project: str,
        region: str,
        function_url: str,
        emulator_url: str | None,
        queue_name: str,
        oidc_token_service_account: str | None,
        logger: Logger
    ):
        if emulator_url is None:
            self.tasks_client = CloudTasksClient()
        else:
            logger.debug("use cloud tasks emulator")
            transport = CloudTasksGrpcTransport(
                channel=grpc.insecure_channel(emulator_url)
            )
            self.tasks_client = CloudTasksClient(
                transport=transport)

        self.__function_url = function_url
        self.__service_account_email = oidc_token_service_account
        self.__logger = logger
        self.__queue_name = self.tasks_client.queue_path(
            project,
            region,
            queue_name
        )

    def dispatch(
        self,
        method: str = "POST",
        payload: dict | None = None,
    ) -> Task | None:
        task = {
            "http_request": {
                "http_method": method,
                "url": self.__function_url,
                "headers": {
                    "Content-Type": "application/json"
                }
            }
        }
        if self.__service_account_email is not None:
            task["http_request"]["oidc_token"] = {
                "service_account_email": self.__service_account_email,
                "audience": self.__function_url,
            }
        if payload is not None:
            task["http_request"]["body"] = json.dumps(payload).encode()

        try:
            return self.tasks_client.create_task(
                request={"parent": self.__queue_name, "task": task})
        except Exception:
            self.__logger.error(
                f"Unable to process request: ${traceback.format_exc()}")
            return None
