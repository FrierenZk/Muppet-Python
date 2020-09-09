from json import dumps, load
from shutil import move
from os import remove
from typing import Dict


class Config:
    build_list: Dict[str, Dict[str, str]] = {}
    _list_file = "build_list.json"

    def __init__(self):
        try:
            with open(self._list_file, 'r') as file:
                if len(file.readline()) < 1:
                    return
                else:
                    file.seek(0, 0)
                data = load(file)
                data: Dict
                file.close()
            for k, v in data.items():
                v: Dict
                for i, j in v.items():
                    i: str
                    j: Dict
                    self.build_list[i] = {**{'category': k}, **j}
            print(self.build_list)
        except Exception as e:
            print(e)

    def get_tasks(self) -> list:
        taskList = []
        for i in self.build_list.keys():
            taskList.append(i)
        return taskList

    def get_category(self, task: str):
        if task in self.build_list:
            if 'category' in self.build_list[task]:
                return self.build_list[task]['category']
        return None

    def get_profile(self, task: str):
        if task in self.build_list:
            if 'profile' in self.build_list[task]:
                return self.build_list[task]['profile']
        return None

    def get_projectName(self, task: str):
        if task in self.build_list:
            if 'projectName' in self.build_list[task]:
                return self.build_list[task]['projectName']
        return None

    def get(self, task: str, value: str):
        if task in self.build_list:
            if value in self.build_list[task]:
                return self.build_list[task][value]
        return None

    def get_svnNoUpdate(self, task: str) -> bool:
        if task in self.build_list:
            if 'svnNoUpdate' in self.build_list[task]:
                return bool(self.build_list[task]['svnNoUpdate'])
        return False

    def get_sourcesPath(self, task: str):
        if task in self.build_list:
            if 'sourcesPath' in self.build_list[task]:
                return self.build_list[task]['sourcesPath']
        return None

    def get_upload(self, task: str) -> bool:
        if task in self.build_list:
            if 'upload' in self.build_list[task]:
                return bool(self.build_list[task]['upload'])
        return True

    def get_uploadPath(self, task: str):
        if task in self.build_list:
            if 'uploadPath' in self.build_list[task]:
                return self.build_list[task]['uploadPath']
        return None

    def get_basePath(self, task: str):
        if task in self.build_list:
            if 'basePath' in self.build_list[task]:
                return self.build_list[task]['basePath']
        return None


config = Config()
