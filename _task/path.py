import os

from _task.config import config

server_dir = {
    "trunk": "maintrunk",
    "branches": "branches_version",
    "tags": "tags_version"
}

type_dir = {
    "trunk": "maintrunk"
}


def _server_dir(task: str):
    type_path: str
    t = config.get_type(task)
    if t is None:
        return None
    if t in server_dir.keys():
        t = server_dir[t]
    return ("172.18.36.250:/volume1/version/" + t + "/" + task + "/").strip()


def _image_dir(task: str):
    t = config.get_type(task)
    if t is None:
        return None
    if t in type_dir.keys():
        t = type_dir[t]
    name = config.get_name(task)
    if name is None:
        return None
    return os.path.expanduser('~') + "/catv/" + t + "/" + name + "/"


def _source_dir(task: str):
    return _image_dir(task) + "catv-hgu-sfu-allinone/"
