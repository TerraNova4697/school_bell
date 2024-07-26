import logging
import json
from threading import Thread

from crontab import CronTab

logger = logging.getLogger("scheduler_logger")


class CronManager:
    dow = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

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

        shift1_lesson_num = 1
        shift2_lesson_num = 1
        new_dow = ",".join(self.dow[: config["days"]])
        for lesson in self._tasks:
            if lesson["shift"] == 1:
                lesson_num = shift1_lesson_num
            else:
                lesson_num = shift2_lesson_num
            job = self._cron.new(
                command=f"{self._exec_service} {self._exec_file} --type start --shift {lesson['shift']} --lesson {lesson_num} >> /home/nikita/Work/school_scheduler/cronjobs.log 2>&1",  # noqa
                comment="schedule",
            )
            job.setall(f'{lesson["start_minute"]} {lesson["start_hour"]} * * {new_dow}')

            job = self._cron.new(
                command=f"{self._exec_service} {self._exec_file} --type end --shift {lesson['shift']} --lesson {lesson_num} >> /home/nikita/Work/school_scheduler/cronjobs.log 2>&1",  # noqa
                comment="schedule",
            )
            job.setall(f'{lesson["end_minute"]} {lesson["end_hour"]} * * {new_dow}')

            if lesson["shift"] == 1:
                shift1_lesson_num += 1
            else:
                shift2_lesson_num += 1

        self._cron.write(user=True)

    def run_now(self, attribute):

        self._cron.remove_all(comment="alarm")

        try:
            job = self._cron.new(
                command=f"{self._exec_service} /home/nikita/Work/school_scheduler/alarm.py --alarm {attribute} >> /home/nikita/Work/school_scheduler/cronjobs.log 2>&1",  # noqa
                comment="alarm",
            )
            thread = Thread(target=job.run)
            thread.start()
            logger.info("task runs")
        finally:
            self._cron.remove_all(comment="alarm")

    def update_schedule(self, num_of_days):
        jobs = self._cron.find_comment("schedule")
        for job in jobs:
            logger.info(f"BEFORE {job}")
            job.dow.on(*self.dow[:num_of_days])
            self._cron.write()
            logger.info(f"AFTER {job}")
