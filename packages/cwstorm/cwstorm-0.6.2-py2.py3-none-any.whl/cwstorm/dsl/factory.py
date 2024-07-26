
from cwstorm.dsl.task import Task
from cwstorm.dsl.upload import Upload
from cwstorm.dsl.job import Job
from cwstorm.dsl.slack import Slack
from cwstorm.dsl.shotgrid import Shotgrid
from cwstorm.dsl.email import Email

CLASSES = {
    "job": Job,
    "task": Task,
    "upload": Upload,
    "slack": Slack,
    "shotgrid": Shotgrid,
    "email": Email
}

def get(data):
    datatype = data.get("type")
    klass = CLASSES.get(datatype)
    if klass is None:
        raise ValueError(f"Class {datatype} not found")
    return klass(**data)
