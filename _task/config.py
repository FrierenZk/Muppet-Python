from json import dumps, load
from shutil import move
from os import remove
from typing import Dict


class Config:
    build_list: Dict[str, Dict[str, str]] = {}
    _list_file = "build_list.json"

    def __init__(self):
        try:
            file = open(self._list_file, 'r')
            file.close()
        except IOError:
            file = open(self._list_file, 'w')
            file.close()
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

    def __del__(self):
        if len(self.build_list) < 1:
            return
        try:
            with open(self._list_file + ".tmp", 'w') as file:
                data: Dict[str, Dict[str, Dict]] = {}
                for k, v in self.build_list.items():
                    print(1)
                    v: Dict
                    k: str
                    print(v)
                    if "type" not in v.keys():
                        continue
                    _type = v["type"]
                    if _type not in data:
                        data[_type] = {}
                    v.pop("type")
                    print(v)
                    data[_type][k] = v
                string = dumps(data, indent=4, sort_keys=True)
                file.write(string)
                file.close()
                move(self._list_file + ".tmp", self._list_file)
        except IOError as err:
            print("config", err)
            remove(self._list_file + ".tmp")
        except LookupError as err:
            print("config", err)
        finally:
            return

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

    def get_update(self, task: str):
        if task in self.build_list:
            if 'svn_update' in self.build_list[task]:
                return self.build_list[task]['svn_update']
        return True

    def get_sourcesPath(self, task: str):
        if task in self.build_list:
            if 'sourcesPath' in self.build_list[task]:
                return self.build_list[task]['sourcesPath']
        return None

    def get_upload(self, task: str):
        if task in self.build_list:
            if 'upload' in self.build_list[task]:
                return self.build_list[task]['upload']
        return True

    def get_cleanup(self, task: str):
        if task in self.build_list:
            if 'cleanup' in self.build_list[task]:
                return self.build_list[task]['cleanup']
        return False

    def get_cleanupSudo(self, task: str):
        if task in self.build_list:
            if 'cleanupSudo' in self.build_list[task]:
                return self.build_list[task]['cleanupSudo']
        return False

    def get_cleanupPath(self, task: str):
        if task in self.build_list:
            if 'cleanupPath' in self.build_list[task]:
                return self.build_list[task]['cleanupPath']
        return ''

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
