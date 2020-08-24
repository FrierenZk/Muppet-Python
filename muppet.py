from multiprocessing import cpu_count, Process, Lock, Queue
from typing import Dict

from _server import Server, ServerCallBackInterface
from _task import config, TaskThread
from input_thread import InputThread
from _timer import TimerThread


class Muppet(Process, ServerCallBackInterface):
    waiting_task_list = Queue()
    waiting_task_set = set()
    waiting_task_set_lock: Lock = Lock()
    processing_task_dic: Dict[str, TaskThread] = {}
    processing_task_dic_lock: Lock = Lock()
    _status = True

    def __init__(self):
        super().__init__()
        self.waiting_task_list: Queue[dict]
        self.input = InputThread(callback_task_finish=self.stop_task,
                                 callback_add_task=self.add_task, callback_exit=self.callback_exit)
        self.input.daemon = True
        self.input.start()
        self.server = Server(interface=self)
        self.server.daemon = True
        self.server.start()
        self.timer = TimerThread(self.callback_timer_add_task)
        self.timer.daemon = True
        self.timer.start()

    def run(self) -> None:
        try:
            while self._status:
                if len(self.processing_task_dic) < (cpu_count() / 2 - 1 if cpu_count() / 2 - 1 > 0 else 1):
                    i = self.task_pop()
                    if i['task'] == "":
                        continue
                    if i['task'] not in self.processing_task_dic.keys():
                        flag = True
                        for j in self.processing_task_dic.keys():
                            if config.get_projectName(i['task']) == config.get_projectName(j):
                                flag = False
                                break
                        if flag:
                            self.run_task(i['task'], i['svn_check'])
                        else:
                            self.waiting_task_list.put(i, block=True)
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
        self.waiting_task_list.close()

    def clean_tasks(self):
        self.processing_task_dic_lock.acquire()
        for _, j in self.processing_task_dic.items():
            j.terminate()
        self.processing_task_dic_lock.release()

    def run_task(self, task: str, svn_check):
        print("Task", task, "running")
        self.processing_task_dic_lock.acquire()
        self.processing_task_dic[task] = TaskThread(task, finish=self.stop_task,
                                                    svn_check=svn_check, push=self.server.broadcast_logs)
        self.processing_task_dic[task].daemon = True
        self.processing_task_dic_lock.release()
        self.processing_task_dic[task].start()

    def task_push(self, task: str, svn_check=False):
        self.waiting_task_list.put({'task': task, 'svn_check': svn_check}, block=True)
        self.waiting_task_set_lock.acquire()
        self.waiting_task_set.add(task)
        self.waiting_task_set_lock.release()

    def task_pop(self) -> dict:
        task = self.waiting_task_list.get(block=True)
        self.waiting_task_set_lock.acquire()
        self.waiting_task_set.remove(task['task'])
        self.waiting_task_set_lock.release()
        return task

    def callback_exit(self):
        self._status = False
        self.task_push("")

    def callback_timer_add_task(self, task: str):
        self.task_push(task, True)

    def get_waiting_list(self) -> list:
        data = []
        self.waiting_task_set_lock.acquire()
        for i in self.waiting_task_set:
            data.append(i)
        self.waiting_task_set_lock.release()
        return data

    def get_processing_list(self) -> list:
        data = []
        self.processing_task_dic_lock.acquire()
        for i in self.processing_task_dic.keys():
            data.append(i)
        self.processing_task_dic_lock.release()
        return data

    def add_task(self, line: str) -> (bool, str):
        i = line.find("execute ")
        if i >= 0:
            task = line[i + len("execute "):].strip('\n').strip('\r').strip()
            self.task_push(task)
            return True, task
        return False, None

    def stop_task(self, task: str, flag=True) -> None:
        self.processing_task_dic_lock.acquire()
        if task in self.processing_task_dic.keys():
            if flag is True:
                self.processing_task_dic.pop(task)
                print("Task:", task, "finished")
            else:
                self.processing_task_dic[task].terminate()
                self.processing_task_dic.pop(task)
                print("Task", task, "terminated")
        else:
            print("Task", task, "already removed")
        self.processing_task_dic_lock.release()
