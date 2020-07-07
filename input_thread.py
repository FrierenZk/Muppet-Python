from sys import stdin
from threading import Thread


class InputThread(Thread):
    status: bool = True

    def __init__(self, callback_task_finish, callback_add_task, callback_exit):
        super().__init__()
        self._callback_task_finish = callback_task_finish
        self._callback_add_task = callback_add_task
        self._callback_exit = callback_exit

    def run(self) -> None:
        from muppet import Muppet
        self._callback_task_finish: Muppet.callback_task_finish
        self._callback_exit: Muppet.callback_exit
        for line in stdin:
            if not self.status:
                break
            if len(line.strip('\n').strip('\r').strip()) < 6:
                continue
            ret, task = self._callback_add_task(line=line)
            if ret:
                print("add task", task, "success")
            elif line.lower().find("exit()") >= 0:
                self._callback_exit()
            elif line.find("terminate ") >= 0:
                i = line.find("terminate ") + len("terminate ")
                self._callback_task_finish(task=line[i:].strip('\n').strip('\r').strip(), flag=False)
            else:
                print("error command")
