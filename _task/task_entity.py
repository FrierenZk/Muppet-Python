from threading import Thread
from multiprocessing import Value
from ctypes import c_wchar_p


class TaskEntity:
    class TaskThread(Thread):
        process = None

        def run(self) -> None:
            try:
                from _task.task_process import TaskProcess
                self.process = TaskProcess(self.task)
                self.process.daemon = True
                self.process.start()
                while self.process.is_alive():
                    self.process.join(10)
            except Exception as err:
                print(err)
            finally:
                self._callback(self.task)
                print("task", self.task, "thread terminated")

        def __init__(self, task: str, callback):
            super().__init__()
            self.task: Value = Value(c_wchar_p, task)
            self._callback = callback

        def terminate(self):
            if self.process is not None:
                if self.process.is_alive():
                    print("task", self.task, "terminating")
                    self.process.terminate()

    task: str
    _task: TaskThread = None

    def __init__(self, task: str, callback):
        self.task = task
        self._callback = callback

    def run(self):
        self._task = self.TaskThread(self.task, self._callback)
        self._task.start()

    def terminate(self):
        if self._task is None:
            return
        self._task.terminate()
        return
