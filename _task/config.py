import json
import os
import shutil
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
            data = json.load(file)
            data: Dict
            file.close()
        for k, v in data.items():
            v: Dict
            for i, j in v.items():
                i: str
                j: Dict
                self.build_list[i] = {**{"type": k}, **j}
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
                string = json.dumps(data, indent=4, sort_keys=True)
                file.write(string)
                file.close()
                shutil.move(self._list_file + ".tmp", self._list_file)
        except IOError as err:
            print("config", err)
            os.remove(self._list_file + ".tmp")
        except LookupError as err:
            print("config", err)
        finally:
            return

    def get_type(self, task: str):
        if task in self.build_list:
            if 'type' in self.build_list[task]:
                return self.build_list[task]['type']
        return None

    def get_profile(self, task: str):
        if task in self.build_list:
            if 'profile' in self.build_list[task]:
                return self.build_list[task]['profile']
        return None

    def get_name(self, task: str):
        if task in self.build_list:
            if 'name' in self.build_list[task]:
                return self.build_list[task]['name']
        return None

    def get(self, task: str, value: str):
        if task in self.build_list:
            if value in self.build_list[task]:
                return self.build_list[task][value]
        return None


config = Config()
