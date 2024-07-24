from pydantic import BaseModel


class Lecture(BaseModel):
    start_hour: int
    start_minute: int
    end_hour: int
    end_minute: int


class UpdateScheduleRPC(BaseModel):
    schedule: list[Lecture]


class OffTill(BaseModel):
    offTill: int


class OnTill(BaseModel):
    onTill: int


class Alarm(BaseModel):
    alarm: bool


class AlarmPath(BaseModel):
    alarmPath: str


class Ambulance(BaseModel):
    ambulance: bool


class AmbulancePath(BaseModel):
    ambulancePath: str


class Days(BaseModel):
    days: int


class EndLessonPath(BaseModel):
    endLessonPath: str


class Fire(BaseModel):
    fire: bool


class FirePath(BaseModel):
    firePath: str


class IsOff(BaseModel):
    isOff: bool


class Shift1LessonsNum(BaseModel):
    shift1LessonsNum: int


class Shift2LessonsNum(BaseModel):
    shift2LessonsNum: int


class StartLessonPath(BaseModel):
    startLessonPath: str


class TestPath(BaseModel):
    testPath: str
