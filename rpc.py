from pydantic import BaseModel


class Lecture(BaseModel):
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int


class UpdateScheduleRPC(BaseModel):
    schedule: list[Lecture]
