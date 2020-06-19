import os
import shutil
import threading
from multiprocessing import cpu_count
from typing import Dict, Deque
from time import sleep

from _task.task_entity import TaskEntity


class Muppet:
    task_list_waiting: Deque[TaskEntity] = []
    task_list: Dict[str, TaskEntity] = []

    class TaskCheck(threading.Thread):
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
                file = open("tasks.txt", 'r')
                line = file.readline()
                i = line.find("execute ")
                if i > 0:
                    task = line[i + len("execute ") + 1:].strip().replace('\n', '').replace('\r', '')
                else:
                    return
                t = open("tasks.txt.tmp", 'w')
                t.writelines(file.readlines())
                file.close()
                t.close()
                shutil.move("tasks.txt.tmp", "tasks.txt")
                tasks.append(TaskEntity(task))
            except IOError:
                os.remove("tasks.txt.tmp")
            except LookupError:
                return

    task_check: TaskCheck

    def __init__(self):
        self.task_check.start()
        self.task_check = self.TaskCheck(self)

    def run(self):
        while True:
            while len(self.task_list) < (cpu_count() / 2 - 1 if cpu_count() / 2 - 1 > 0 else 1):
                if len(self.task_list_waiting) > 0:
                    i = self.task_list_waiting.popleft()
                    self.task_list[i.task] = i
                    self.task_list[i.task].run()
                else:
                    break
            sleep(10)

    def __del__(self):
        self.task_check.status = False
        self.task_check.join()
