from collections import deque
from multiprocessing import cpu_count
from time import sleep
from typing import Dict, Deque
from _task.task_entity import TaskEntity
from input_thread import InputThread
from task_thread import TaskThread
from threading import Thread, Lock
from _task.config import config


class Muppet:
    task_list_waiting: Deque[TaskEntity] = deque()
    task_list_waiting_lock: Lock
    task_list: Dict[str, TaskEntity] = {}
    task_list_lock: Lock
    status = True
    task_check: TaskThread = None
    input: InputThread = None

    def __init__(self):
        self.init_task_check()
        self.init_input()
        self.task_list_lock = Lock()
        self.task_list_waiting_lock = Lock()

    def init_task_check(self):
        if self.task_check is None:
            self.task_check = TaskThread(self)
            self.task_check.daemon = True
            self.task_check.start()
            print("task check thread on")

    def init_input(self):
        if self.input is None:
            self.input = InputThread(self)
            self.input.daemon = True
            self.input.start()
            print("input listener on")

    # noinspection PyTypeChecker
    def terminate_task_check(self):
        self.task_check.status = False
        try:
            self.task_check.join(10)
        except TimeoutError:
            print("can not terminate task check normally")
        finally:
            self.task_check = None
            print("task check terminated")

    # noinspection PyTypeChecker
    def terminate_input(self):
        self.input.status = False
        try:
            if self.input.is_alive():
                self.input.join(1)
        except TimeoutError:
            print("can not terminate input listener normally")
        finally:
            self.input = None
            print("input listener terminated")

    def callback(self, task):
        self.task_list_lock.acquire()
        self.task_list.pop(task)
        self.task_list_lock.release()
        print(task, "finished")

    def run(self):
        while self.status:
            while len(self.task_list) < (cpu_count() / 2 - 1 if cpu_count() / 2 - 1 > 0 else 1):
                if len(self.task_list_waiting) > 0:
                    self.task_list_waiting_lock.acquire()
                    i = self.task_list_waiting.popleft()
                    self.task_list_waiting_lock.release()
                    if i.task not in self.task_list.keys():
                        flag = True
                        for j in self.task_list.keys():
                            if config.get_name(i.task) == config.get_name(j):
                                flag = False
                                break
                        if flag:
                            self.task_list_lock.acquire()
                            self.task_list[i.task] = i
                            self.task_list_lock.release()
                            self.task_list[i.task].run()
                            print(i.task, "running")
                        else:
                            self.task_list_waiting_lock.acquire()
                            self.task_list_waiting.append(i)
                            self.task_list_waiting_lock.release()
                    else:
                        print("duplicated tasks error", i.task)
                else:
                    break
            sleep(10)
        print("muppet closing")
        self.__del__()

    def add_task_to_waiting_line(self, line: str):
        i = line.find("execute ")
        if i >= 0:
            task = line[i + len("execute "):].strip('\n').strip('\r').strip()
            self.add_task_to_waiting(task)
            return True, task
        return False, None

    def add_task_to_waiting(self, task: str):
        self.task_list_waiting_lock.acquire()
        self.task_list_waiting.append(TaskEntity(task, self.callback))
        self.task_list_waiting_lock.release()

    def terminate_task(self, task: str):
        if task in self.task_list.keys():
            print("task", task, "stopping")
            Thread(target=self.task_list[task].terminate).start()
        else:
            print("can't find task", task)

    def exit(self):
        self.status = False
        print("exiting...")

    # noinspection PyTypeChecker
    def __del__(self):
        th1: Thread = None
        th2: Thread = None
        if self.task_check is not None:
            if self.task_check.is_alive():
                th1 = Thread(target=self.terminate_task_check).start()
        if self.input is not None:
            if self.input.is_alive():
                th2 = Thread(target=self.terminate_input).start()
        if th1 is not None:
            th1.join()
        if th2 is not None:
            th2.join()
