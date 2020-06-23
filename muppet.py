from threading import Thread
from collections import deque
from multiprocessing import cpu_count
from time import sleep
from typing import Dict, Deque

from _task.task_entity import TaskEntity


class Muppet:
    task_list_waiting: Deque[TaskEntity] = deque()
    task_list: Dict[str, TaskEntity] = {}

    class TaskCheck(Thread):
        status: bool = True

        def __init__(self, m):
            super().__init__()
            self.m = m

        def run(self) -> None:
            while self.status:
                self._check_file()
                sleep(5)

        def _check_file(self):
            tasks: Deque[TaskEntity] = self.m.task_list_waiting
            if len(tasks) > 2:
                return
            try:
                file = open("tasks.txt", 'r')
                file.close()
            except IOError:
                file = open("tasks.txt", 'w')
                file.close()
            try:
                flag = False
                file = open("tasks.txt", 'r')
                lines = file.readlines()
                for line in lines:
                    i = line.find("execute ")
                    if i >= 0:
                        task = line[i + len("execute "):].strip().replace('\n', '').replace('\r', '')
                        tasks.append(TaskEntity(task, self.m.callback))
                        flag = True
                    else:
                        continue
                file.close()
                if flag:
                    file = open("tasks.txt", 'w')
                    file.close()
            except IOError as err:
                print("muppet", err)
            except LookupError as err:
                print("muppet", err)
            finally:
                return

    def __init__(self):
        self.task_check = self.TaskCheck(self)
        self.task_check.start()

    def callback(self, task):
        self.task_list.pop(task)
        print(task, "finished")

    def run(self):
        while True:
            while len(self.task_list) < (cpu_count() / 2 - 1 if cpu_count() / 2 - 1 > 0 else 1):
                if len(self.task_list_waiting) > 0:
                    i = self.task_list_waiting.popleft()
                    if i.task not in self.task_list.keys():
                        self.task_list[i.task] = i
                        self.task_list[i.task].run()
                    else:
                        print("duplicated tasks error", i.task)
                else:
                    break
            sleep(10)

    def __del__(self):
        self.task_check.status = False
        self.task_check.join()
