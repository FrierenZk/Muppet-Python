from ctypes import c_wchar_p, c_bool
from multiprocessing import Process, Value
from threading import Thread


class TaskEntity(Thread):
    task: str

    def __init__(self, task: str, callback):
        super().__init__()
        self.task = task
        self._callback = callback
        self.unregistered = Value(c_bool, False)
        self.process = Process()

    def run(self) -> None:
        from _task.task_process import TaskProcess
        self.process = TaskProcess(Value(c_wchar_p,self.task))
        self.process.daemon = True
        self.process.run()
        self.unregister()
        print("Task", self.task, "thread terminated")

    def terminate(self):
        self.unregister()
        if self.process.is_alive():
            self.process.terminate()
        return

    def unregister(self):
        self.unregistered.acquire()
        if self.unregistered.value is False:
            self._callback(task=self.task, flag=True)
            self.unregistered.value = True
        self.unregistered.release()
