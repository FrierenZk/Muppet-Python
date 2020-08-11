from multiprocessing import cpu_count, Process, Lock, Queue
from typing import Dict

from _server import Server
from _task import config, TaskEntity
from input_thread import InputThread
from _timer import TimerThread


class Muppet(Process):
    task_list_waiting = Queue()
    task_list: Dict[str, TaskEntity] = {}
    task_list_lock: Lock
    _status = True

    def __init__(self):
        super().__init__()
        self.task_list_lock = Lock()
        self.task_list_waiting: Queue[str]
        self.input = InputThread(callback_task_finish=self.callback_task_finish,
                                 callback_add_task=self.callback_add_task, callback_exit=self.callback_exit)
        self.input.daemon = True
        self.input.start()
        self.server = Server(callback_add_task=self.callback_add_task, callback_stop_task=self.callback_task_finish,
                             callback_get_task_list=self.callback_get_task_list,
                             callback_get_waiting_count=self.callback_get_waiting_count)
        self.server.daemon = True
        self.server.start()
        self.timer = TimerThread(self.callback_timer_add_task)
        self.timer.daemon = True
        self.timer.start()

    def run(self) -> None:
        try:
            while self._status:
                if len(self.task_list) < (cpu_count() / 2 - 1 if cpu_count() / 2 - 1 > 0 else 1):
                    i = self.task_list_waiting.get(block=True)
                    if i == "":
                        continue
                    if i not in self.task_list.keys():
                        flag = True
                        for j in self.task_list.keys():
                            if config.get_projectName(i) == config.get_projectName(j):
                                flag = False
                                break
                        if flag:
                            print("Task", i, "running")
                            self.task_list_lock.acquire()
                            self.task_list[i] = TaskEntity(i, self.callback_task_finish)
                            self.task_list_lock.release()
                            self.task_list[i].start()
                        else:
                            self.task_list_waiting.put(i, block=True)
                    else:
                        print("Duplicated tasks error", i)
        except EOFError:
            print("Muppet closing")
        finally:
            self.clean_tasks()

    def terminate(self) -> None:
        self.clean_tasks()
        super().terminate()

    def __del__(self):
        self.task_list_waiting.close()

    def clean_tasks(self):
        self.task_list_lock.acquire()
        for _, j in self.task_list.items():
            j.terminate()
        self.task_list_lock.release()

    def callback_exit(self):
        self._status = False
        self.task_list_waiting.put("", block=True)

    def callback_task_finish(self, task, flag=True):
        self.task_list_lock.acquire()
        if task in self.task_list.keys():
            if flag is True:
                self.task_list.pop(task)
                print("Task:", task, "finished")
            else:
                self.task_list[task].terminate()
                self.task_list.pop(task)
                print("Task", task, "terminated")
        else:
            print("Can not find target task:", task)
        self.task_list_lock.release()

    def callback_add_task(self, line: str):
        i = line.find("execute ")
        if i >= 0:
            task = line[i + len("execute "):].strip('\n').strip('\r').strip()
            self.task_list_waiting.put(task)
            return True, task
        return False, None

    def callback_timer_add_task(self, task: str):
        self.task_list_lock.acquire()
        if task not in self.task_list.keys():
            self.task_list[task] = TaskEntity(task, self.callback_task_finish, True)
        self.task_list_lock.release()
        self.task_list[task].start()

    def callback_get_task_list(self):
        data = []
        self.task_list_lock.acquire()
        for i in self.task_list.keys():
            data.append(i)
        self.task_list_lock.release()
        return data

    def callback_get_waiting_count(self):
        return self.task_list_waiting.qsize()
