from threading import Thread
from sys import stdin
from _task import config_reload


class InputThread(Thread):
    status: bool = True

    def __init__(self, m):
        super().__init__()
        self.m = m

    def run(self) -> None:
        from muppet import Muppet
        self.m: Muppet
        for line in stdin:
            if not self.status:
                break
            if len(line.strip('\n').strip('\r').strip()) < 6:
                continue
            ret, task = self.m.add_task_to_waiting(line)
            if ret:
                print("add task", task, "success")
            elif line.find("task check") >= 0:
                if line.find("on") >= 0:
                    self.m.init_task_check()
                elif line.find("off") >= 0:
                    self.m.terminate_task_check()
                else:
                    print("error task check command")
            elif line.lower().find("exit()") >= 0:
                self.m.exit()
            elif line.lower().find("config reload") >= 0:
                config_reload()
            elif line.find("terminate ") >= 0:
                i = line.find("terminate ") + len("terminate ")
                self.m.terminate_task(line[i:].strip('\n').strip('\r').strip())
            else:
                print("error command")
