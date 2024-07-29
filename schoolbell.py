import logging
import json
import base64
import os
import datetime

from tb_device_mqtt import TBDeviceMqttClient
from pydantic import ValidationError

from rpc import UpdateScheduleRPC
import rpc
from bell import stop_priority


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
        # self._sub_attr_off_till = self.subscribe_to_attribute(
        #     "offTill", self.handle_updated_attribute
        # )
        # self._sub_attr_on_till = self.subscribe_to_attribute(
        #     "onTill", self.handle_updated_attribute
        # )
        self._sub_attr_alarm = self.subscribe_to_attribute(
            "alarm", self.handle_updated_attribute_and_run_alarm
        )
        self._sub_attr_alarm_path = self.subscribe_to_attribute(
            "alarmPath", self.handle_updated_attribute
        )
        self._sub_attr_ambulance = self.subscribe_to_attribute(
            "ambulance", self.handle_updated_attribute
        )
        self._sub_attr_ambulance_path = self.subscribe_to_attribute(
            "ambulancePath", self.handle_updated_attribute
        )
        self._sub_attr_days = self.subscribe_to_attribute(
            "days", self.handle_updated_attribute_and_update_cron
        )
        self._sub_attr_end_lesson_path = self.subscribe_to_attribute(
            "endLessonPath", self.handle_updated_attribute
        )
        self._sub_attr_fire = self.subscribe_to_attribute(
            "fire", self.handle_updated_attribute_and_run_alarm
        )
        self._sub_attr_test = self.subscribe_to_attribute(
            "test", self.handle_updated_attribute_and_run_alarm
        )
        self._sub_attr_fire_path = self.subscribe_to_attribute(
            "firePath", self.handle_updated_attribute
        )
        self._sub_attr_is_off = self.subscribe_to_attribute(
            "isOff", self.handle_updated_attribute
        )
        self._sub_attr_shift1_lessons_num = self.subscribe_to_attribute(
            "shift1LessonsNum", self.handle_updated_attribute
        )
        self._sub_attr_shift2_lessons_num = self.subscribe_to_attribute(
            "shift2LessonsNum", self.handle_updated_attribute
        )
        self._sub_attr_start_lessons_path = self.subscribe_to_attribute(
            "startLessonPath", self.handle_updated_attribute
        )
        self._sub_attr_test_path = self.subscribe_to_attribute(
            "testPath", self.handle_updated_attribute
        )
        self._sub_attr_start_lesson_audio = self.subscribe_to_attribute(
            "startLessonAudio", self.handle_updated_attribute_and_save_audio
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

    def get_day_midnight(self, days: int | None = None):
        """Returns a datetime object for the start of the next day (00:00)."""
        today = datetime.date.today()
        target_day = today + datetime.timedelta(days=1)
        if days:
            target_day = target_day + datetime.timedelta(days=days)
        return datetime.datetime(target_day.year, target_day.month, target_day.day)

    def get_readable_dt(self, dt: datetime.datetime) -> str:
        return dt.strftime("%d.%m.%Y %H:%M")

    def handle_server_side_rpc_reqeusts(self, request_id, body):
        method = body["method"]
        params = body["params"]

        logger.warning(body)

        if method == "updateSchedule":
            try:
                UpdateScheduleRPC(**params)
            except ValidationError as e:
                logger.exception(str(e))
                self.send_rpc_reply(
                    request_id, e.json(include_context=True, include_input=True)
                )
                return

            try:
                self.cron_manager.set_tasks(params["schedule"])
                self.cron_manager.rewrite_schedule()
            except Exception:
                pass

            self.send_rpc_reply(request_id, "true")

        elif method == "turnOffFor":
            days = params["days"]

            start_midnight = self.get_day_midnight()
            end_midnight = self.get_day_midnight(days)

            self.update_config(
                "offFor",
                [
                    int(1000 * start_midnight.timestamp()),
                    int(1000 * end_midnight.timestamp()),
                ],
            )

            response_text = f"Отключен с {self.get_readable_dt(start_midnight)} по {self.get_readable_dt(end_midnight)}"
            logger.info(response_text)
            self.send_rpc_reply(request_id, json.dumps({"message": response_text}))

        elif method == "turnOnFor":
            days = params["days"]

            start_midnight = self.get_day_midnight()
            end_midnight = self.get_day_midnight(days)

            self.update_config(
                "onFor",
                [
                    int(1000 * start_midnight.timestamp()),
                    int(1000 * end_midnight.timestamp()),
                ],
            )

            response_text = f"Включен с {self.get_readable_dt(start_midnight)} по {self.get_readable_dt(end_midnight)}"
            logger.info(response_text)
            self.send_rpc_reply(request_id, json.dumps({"message": response_text}))

        else:
            logger.warning(f"Unknown method for {self.__class__.__name__}: {method}")
            self.send_rpc_reply(request_id, "false")

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

    def handle_updated_attribute_and_run_alarm(self, body, *args):
        self.handle_updated_attribute(body, args)
        attribute, value = list(body.items())[0]
        logger.info(f"current value of alarm is {value}")
        if value:
            self.cron_manager.run_now(attribute)
        else:
            stop_priority()

    def handle_updated_attribute_and_save_audio(self, body, *args):
        attribute, value = list(body.items())[0]
        b64format_audio = body[attribute]

        try:
            audio_format = body[attribute].split(";")[0].split("/")[1]
        except IndexError as e:
            logger.exception(e)

        logger.info(b64format_audio.split(",")[-1])

        try:
            file_name = f"{attribute}.{audio_format}"
            fh = open(file_name, "wb")
            fh.write(base64.b64decode(b64format_audio.split(",")[-1]))
            fh.close()
        except Exception as e:
            logger.exception(e)

        try:
            new_path_key = attribute.removesuffix("Audio") + "Path"
            file_path = (
                str(os.path.dirname(os.path.abspath(__file__)))
                + f"/{attribute}.{audio_format}"
            )
            self.update_config(new_path_key, file_path)
        except Exception as e:
            logger.exception(e)

    def handle_updated_attribute_and_update_cron(self, body, *args):
        self.handle_updated_attribute(body, args)
        attribute, value = list(body.items())[0]
        try:
            self.cron_manager.update_schedule(value)
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
