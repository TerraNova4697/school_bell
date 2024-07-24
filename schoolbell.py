import logging
import json

from tb_device_mqtt import TBDeviceMqttClient
from pydantic import ValidationError

from rpc import UpdateScheduleRPC
import rpc


logger = logging.getLogger("scheduler_logger")


class SchoolBell(TBDeviceMqttClient):

    def __init__(self, url, token, cron_manager, config_path: str = "config.json"):
        self.url = url
        self.token = token
        self.cron_manager = cron_manager
        self._config_path = config_path
        super().__init__(self.url, username=self.token)

    def listen_rpc(self):
        self.set_server_side_rpc_request_handler(self.handle_server_side_rpc_reqeusts)

    def unsubscribe_from_all_attributes(self):
        self.unsubscribe_from_attribute(self._sub_attr_schedule)

    def listen_attributes(self):
        self._sub_attr_schedule = self.subscribe_to_attribute(
            "schedule", self.handle_schedule_attribute
        )
        self._sub_attr_off_till = self.subscribe_to_attribute(
            "offTill", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "alarm", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "alarmPath", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "ambulance", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "ambulancePath", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "days", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "endLessonPath", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "fire", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "firePath", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "isOff", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "shift1LessonsNum", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "shift2LessonsNum", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "startLessonPath", self.handle_updated_attribute
        )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "testPath", self.handle_updated_attribute
        )

    def sliceindex(self, x):
        i = 0
        for c in x:
            if c.isalpha():
                i = i + 1
                return i
            i = i + 1

    def upperfirst(self, x):
        i = self.sliceindex(x)
        return x[:i].upper() + x[i:]

    def update_config(self, key: str, value) -> None:
        config = None
        with open(self._config_path, "r") as config_file:
            config = json.load(config_file)
            config[key] = value

        with open(self._config_path, "w") as config_file:
            json.dump(config, config_file, indent=2)

    def handle_updated_attribute(self, body, *args):
        try:
            attribute, value = list(body.items())[0]
            class_name = self.upperfirst(attribute)
        except AttributeError as e:
            logger.exception(e)

        try:
            attr_class = getattr(rpc, class_name)
            attr_class(**body)
        except ValidationError as e:
            logger.exception(str(e))
            return

        try:
            self.update_config(attribute, value)
        except Exception as e:
            logger.exception(e)

    def handle_schedule_attribute(self, body, *args):
        try:
            UpdateScheduleRPC(**body)
        except ValidationError as e:
            logger.exception(str(e))
            return

        try:
            self.cron_manager.set_tasks(body["schedule"])
            self.cron_manager.rewrite_schedule()
        except Exception as e:
            logger.exception(e)
