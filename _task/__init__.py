from _task.config import Config
from _task.task_entity import TaskEntity

config = Config()

type_dir = {
    "trunk": "maintrunk",
    "branches": "branches_version"
}


def _server_dir(task: str):
    type_path: str
    t = config.get_type(task)
    if t is None:
        return None
    if t in type_dir.keys():
        type_path = type_dir[t]
    else:
        type_path = t
    return ("172.18.36.250:/volume1/version/" + type_path + "/" + task + "/").strip()


def _source_dir(task: str):
    t = config.get_type(task)
    if t is None:
        return None
    name = config.get_name(task)
    if name is None:
        return None
    return "~/catv/" + t + "/" + name + "/"
