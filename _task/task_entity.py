import os
import subprocess
import threading
from _task.path import _server_dir, _source_dir
from _task.config import config


class TaskEntity:
    class TaskThread(threading.Thread):
        shell_process: subprocess.Popen

        def run(self) -> None:
            os.chdir(_source_dir(self.task))
            ret = subprocess.run("svn up")
            print("task=" + self.task, "svn up", ret)
            cmd = "./mkfw.sh " + self.profile
            cmd = cmd + " clean && " + cmd
            self.shell_process = subprocess.Popen(cmd, bufsize=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.shell_process.wait()
            out, err = self.shell_process.communicate()
            if self.shell_process.returncode == 0:
                print(cmd, "success")
                self._upload_image()
            else:
                print("task=" + self.task, "cmd failed")
                print(out)
                print(err)

        def __init__(self, task: str, profile: str):
            super().__init__()
            self.task = task
            self.profile = profile
            self.image_dir = _source_dir(task)

        def _upload_image(self):
            file_path = ""
            files = os.listdir(self.image_dir)
            for file in files:
                if file.find(".tar.gz") == -1:
                    continue
                file_path = self.image_dir + file
                break

            if file_path is not None:
                ret = subprocess.run(
                    "sudo sshpass -p 654321 scp " + file_path + " buildmanager@" + _server_dir(self.task))
                if ret.returncode == 0:
                    print("task=" + self.task, "upload success")
                else:
                    print("task=" + self.task, "upload fail", ret)

    task: str
    _profile: str
    valid = False
    _task: TaskThread = None

    def __init__(self, task: str):
        self.task = task
        self._profile = config.get_profile(task)
        if (task is not None) & (self._profile is not None):
            self.valid = True

    def run(self):
        if self.valid:
            self._task = self.TaskThread(self.task, self._profile)
            self._task.start()
        else:
            print("task invalid", "task=" + self.task, "profile=" + self._profile)

    def terminate(self):
        if self._task is None:
            return
        if self._task.shell_process.poll() is None:
            self._task.shell_process.terminate()
        return

    def __del__(self):
        if self._task is None:
            return
        self._task.shell_process.kill()
