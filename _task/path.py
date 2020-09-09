from os.path import expanduser
from _task.config import config

server_dir = {
    "trunk": "maintrunk",
    "branches": "branches_version",
    "tags": "tags_version"
}

category_dir = {
    "trunk": "maintrunk"
}


def _upload_dir(task: str):
    type_path: str
    category = config.get_category(task)
    if category is None:
        return None
    if category in server_dir.keys():
        category = server_dir[category]
    uploadPath = config.get_uploadPath(task)
    if uploadPath is None:
        name = config.get_projectName(task)
    else:
        name = uploadPath
    if name is None:
        return None
    return ("172.18.36.250:/volume1/version/" + category + "/" + name + "/").strip()


def _work_dir(task: str):
    category = config.get_category(task)
    if category is None:
        return None
    if category in category_dir.keys():
        category = category_dir[category]
    name = config.get_projectName(task)
    if name is None:
        return None
    basePath = config.get_basePath(task)
    if basePath is None:
        basePath = "catv"
    return expanduser('~') + "/" + basePath + "/" + category + "/" + name + "/"


def _image_dir(task: str):
    return _source_dir(task) + "Project/images/"


def _source_dir(task: str):
    category = config.get_category(task)
    if category is None:
        return None
    if category in category_dir.keys():
        category = category_dir[category]
    name = config.get_projectName(task)
    if name is None:
        return None
    sources = config.get_sourcesPath(task)
    if sources is None:
        sources = "catv-hgu-sfu-allinone"
    basePath = config.get_basePath(task)
    if basePath is None:
        basePath = "catv"
    return expanduser('~') + "/" + basePath + "/" + category + "/" + name + "/" + sources + "/"
