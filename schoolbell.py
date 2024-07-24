import logging

from tb_device_mqtt import TBDeviceMqttClient
from pydantic import ValidationError

from rpc import UpdateScheduleRPC


logger = logging.getLogger("scheduler_logger")


class SchoolBell(TBDeviceMqttClient):

    def __init__(self, url, token, cron_manager):
        self.url = url
        self.token = token
        self.cron_manager = cron_manager
        super().__init__(self.url, username=self.token)

    def listen_rpc(self):
        self.set_server_side_rpc_request_handler(self.handle_server_side_rpc_reqeusts)

    def listen_attributes(self):
        self.subscribe_to_all_attributes(self.update_attributes)

    def handle_server_side_rpc_reqeusts(self, request_id, body):
        method = body["method"]
        params = body["params"]

        if method == "updateSchedule":
            try:
                UpdateScheduleRPC(**params)
            except ValidationError as e:
                logger.exception(str(e))
                self.send_rpc_reply(
                    request_id, e.json(include_context=True, include_input=True)
                )
                return

            # TODO: manage cron logic
            try:
                self.cron_manager.set_tasks(params["schedule"])
                self.cron_manager.rewrite_schedule()
            except Exception:
                pass

            self.send_rpc_reply(request_id, "true")

        else:
            logger.warning(f"Unknown method for {self.__class__.__name__}: {method}")
            self.send_rpc_reply(request_id, "false")

    def update_attributes(self, result, *args):
        logger.info(result)
