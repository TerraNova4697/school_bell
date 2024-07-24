import logging
import json

from crontab import CronTab

logger = logging.getLogger("scheduler_logger")


class CronManager:

    def __init__(
        self,
        user: str,
        exec_service: str,
        exec_file: str,
        config_path: str = "config.json",
    ):
        self._user = user
        self._cron = CronTab(
            user=True, log="/home/nikita/Work/school_scheduler/cronjobs.log"
        )
        self._exec_service = exec_service
        self._exec_file = exec_file
        self._tasks = None
        self._config_path = config_path

    def set_tasks(self, tasks):
        self._tasks = tasks

    def rewrite_schedule(self):
        self._cron.remove_all(comment="schedule")
        configs = {}
        with open(self._config_path, "r") as config_file:
            config = json.load(config_file)
            configs["days"] = config["days"]

        for lesson in self._tasks:
            job = self._cron.new(
                command=f"{self._exec_service} {self._exec_file} --type start >> /home/nikita/Work/school_scheduler/cronjobs.log 2>&1",  # noqa
                comment="schedule",
            )
            job.setall(
                f'{lesson["start_minute"]} {lesson["start_hour"]} * * 1-{configs["days"]}'
            )

            job = self._cron.new(
                command=f"{self._exec_service} {self._exec_file} --type end >> /home/nikita/Work/school_scheduler/cronjobs.log 2>&1",  # noqa
                comment="schedule",
            )
            job.setall(
                f'{lesson["end_minute"]} {lesson["end_hour"]} * * 1-{configs["days"]}'
            )

        self._cron.write()
