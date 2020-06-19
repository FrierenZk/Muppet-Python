import os
import subprocess
import threading
from . import _server_dir, _source_dir, config


class TaskEntity:
    class TaskThread(threading.Thread):
        shell_process: subprocess.Popen

        def run(self) -> None:
            os.chdir(_source_dir(self.task))
            subprocess.run("svn up")
            cmd = "./mkfw.sh " + self.profile
            cmd = cmd + " clean && " + cmd
            self.shell_process = subprocess.Popen(cmd, bufsize=30, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        def __init__(self, task: str, profile: str):
            threading.Thread.__init__(self)
            self.task = task
            self.profile = profile

    task: str
    _profile: str
    valid = False
    _task: TaskThread = None

    def __init__(self, task: str):
        self.image_dir = None
        self.task = task
        self._profile = config.get_profile(task)
        if (task is not None) & (self._profile is not None):
            self.valid = True

    def run(self):
        subprocess.run("svn up " + _source_dir(self.task))
        mkfw = "." + _source_dir(self.task) + "mkfw.sh"
        cmd = mkfw + " " + self._profile + " clean && " + mkfw + " " + self._profile
        if self.valid:
            self._task = self.TaskThread(cmd)
            self._task.start()
        else:
            print("task invalid: ", cmd)
        return

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

    def _upload_image(self):
        file_path = ""
        files = os.listdir(self.image_dir)
        for file in files:
            if file.find(".tar.gz") == -1:
                continue
            file_path = self.image_dir + file
            break

        if file_path is not None:
            ret = subprocess.run("sudo sshpass -p 654321 scp " + file_path + " buildmanager@" + _server_dir(self.task))
            if ret.returncode == 0:
                print("upload success")
            else:
                print("upload fail", ret)
