from ctypes import c_wchar_p, c_bool
from multiprocessing import Value
from threading import Thread
from time import sleep


class TaskEntity(Thread):
    task: str
    process = None

    def __init__(self, task: str, callback):
        super().__init__()
        self.task = task
        self._callback = callback
        self.unregistered = Value(c_bool, False)

    def run(self) -> None:
        from _task.task_process import TaskProcess
        self.process = TaskProcess(Value(c_wchar_p, self.task))
        self.process.daemon = True
        self.process.run()
        self.unregister()
        print("Task", self.task, "thread terminated")

    def terminate(self):
        from _task.task_process import TaskProcess
        print(0)
        if self.process is not None:
            print(1)
            self.process: TaskProcess
            self.process.terminate()
            print(6)
            sleep(0)
        return

    def unregister(self):
        with self.unregistered.get_lock():
            print(8)
            if self.unregistered.value is False:
                self._callback(task=self.task, flag=True)
                self.unregistered.value = True
                print(9)
