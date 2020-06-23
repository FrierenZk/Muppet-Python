from threading import Thread
from collections import deque
from multiprocessing import cpu_count
from time import sleep
from typing import Dict, Deque
from sys import stdin

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
            try:
                file = open("tasks.txt", 'r')
                file.close()
            except IOError:
                file = open("tasks.txt", 'w')
                file.close()
            while self.status:
                self._check_file()
                sleep(60)

        def _check_file(self):
            tasks: Deque[TaskEntity] = self.m.task_list_waiting
            if len(tasks) > 2:
                return
            try:
                flag = False
                file = open("tasks.txt", 'r')
                lines = file.readlines()
                file.close()
                for line in lines:
                    t, _ = self.m.add_task_to_waiting(line)
                    flag |= t
                if flag:
                    file = open("tasks.txt", 'w')
                    file.close()
            except IOError as err:
                print("muppet", err)
            except LookupError as err:
                print("muppet", err)
            finally:
                return

    class InputThread(Thread):
        def __init__(self, m):
            super().__init__()
            self.m = m

        def run(self) -> None:
            for line in stdin:
                if len(line.strip('\n').strip('\r').strip()) < 8:
                    continue
                ret, task = self.m.add_task_to_waiting(line)
                if ret:
                    print("add task", task, "success")
                elif line.find("task check"):
                    if line.find("on"):
                        self.m.init_task_check()
                    elif line.find("off"):
                        self.m.terminate_task_check()
                    else:
                        print("error task check command")
                else:
                    print("error command")

    task_check: TaskCheck = None
    input: InputThread

    def __init__(self):
        self.init_task_check()
        self.init_input()

    def init_task_check(self):
        if self.task_check is None:
            self.task_check = self.TaskCheck(self)
            self.task_check.start()

    def init_input(self):
        self.input = self.InputThread(self)
        self.input.start()

    def terminate_task_check(self):
        self.task_check.status = False
        try:
            self.task_check.join(60)
        except TimeoutError:
            print("can not terminate task check normally")
        finally:
            self.task_check = None

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

    def add_task_to_waiting(self, line: str):
        i = line.find("execute ")
        if i >= 0:
            task = line[i + len("execute "):].strip().replace('\n', '').replace('\r', '')
            self.task_list_waiting.append(TaskEntity(task, self.callback))
            return True, task
        return False, None

    def __del__(self):
        self.task_check.status = False
        self.task_check.join()
