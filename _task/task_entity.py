from ctypes import c_wchar_p, c_bool
from multiprocessing import Process, Value


class TaskEntity(Process):
    task: str

    def __init__(self, task: str, callback):
        super().__init__()
        self.task = task
        self._callback = callback
        self.unregistered = Value(c_bool, False)
        from _task.task_process import TaskProcess
        self.process = TaskProcess(Value(c_wchar_p, self.task))
        self.process.daemon = True

    def run(self) -> None:
        try:
            self.process.start()
            while self.process.is_alive():
                self.process.join(10)
        except Exception as err:
            print(err)
        finally:
            self.unregister()
            print("task", self.task, "thread terminated")

    def terminate(self):
        self.unregister()
        super(TaskEntity, self).terminate()
        return

    def unregister(self):
        self.unregistered.acquire()
        if self.unregistered.value is False:
            self._callback(task=self.task, flag=True)
            self.unregistered.value = True
        self.unregistered.release()
