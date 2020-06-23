from threading import Thread
from typing import Deque
from _task.task_entity import TaskEntity
from time import sleep


class TaskThread(Thread):
    status: bool = True

    def __init__(self, m):
        super().__init__()
        self.m = m

    def run(self) -> None:
        from muppet import Muppet
        self.m: Muppet
        try:
            file = open("tasks.txt", 'r')
            file.close()
        except IOError:
            file = open("tasks.txt", 'w')
            file.close()
        while self.status:
            self._check_file()
            sleep(10)

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
