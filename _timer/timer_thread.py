from threading import Thread
from time import sleep
from json import load


class TimerThread(Thread):
    t_list: list

    def __init__(self, callback):
        super().__init__()
        self._read_config()
        self.callback = callback

    def run(self) -> None:
        while True:
            sleep(60)
            for i in self.t_list:
                if 'interval' not in i:
                    continue
                if 'name' not in i:
                    continue
                if 'count' not in i:
                    i['count'] = 0
                i['count'] += 1
                if i['count'] >= i['interval']:
                    i['count'] = 0
                    print("Task:", i['name'], "time triggered")
                    self.callback(i['name'])

    def _read_config(self):
        try:
            with open("timer_list.json", 'r') as file:
                self.t_list = load(file)
                self.t_list: list
                file.close()
                print(self.t_list)
        except Exception as e:
            print(e)
