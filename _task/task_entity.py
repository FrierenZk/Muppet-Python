from os import chdir, listdir, remove
from shutil import rmtree
from os.path import join, isfile, isdir, getsize
from threading import Thread
from subprocess import PIPE, Popen, run
from _task.path import _server_dir, _source_dir, _image_dir
from _task.config import config


class TaskEntity:
    class TaskThread(Thread):
        shell_process: Popen = None

        def run(self) -> None:
            try:
                chdir(_source_dir(self.task))
                ret = run("svn up", shell=True)
                print("task=" + self.task, "svn up", ret)
                cmd = "./mkfw.sh " + self.profile
                cmd = cmd + " clean && " + cmd
                self._image_clean()
                self.shell_process = Popen(cmd, shell=True, bufsize=30, stdout=PIPE,
                                           stderr=PIPE)
                out, err = self.shell_process.communicate()
                self.shell_process.wait()
                if self.shell_process.returncode == 0:
                    print(cmd, "success")
                    self._upload_image()
                else:
                    print("task=" + self.task, "cmd=" + cmd, "cmd failed")
                    print(out)
                    print(err)
            finally:
                self._callback(self.task)

        def __init__(self, task: str, profile: str, callback):
            super().__init__()
            self.task = task
            self.profile = profile
            self.image_dir = _image_dir(task)
            self._callback = callback

        def _upload_image(self):
            file_path = ""
            files = listdir(self.image_dir)
            for file in files:
                if file.find(".tar.gz") == -1:
                    continue
                file_path = self.image_dir + file
                break
            if file_path is not "":
                if getsize(file_path) < (1024 * 1024):
                    print(file_path, "size is not right, upload canceled")
                    return
                ret = run(
                    "sudo sshpass -p 654321 scp " + file_path + " buildmanager@" + _server_dir(self.task), shell=True)
                if ret.returncode == 0:
                    print("task=" + self.task, "upload success")
                else:
                    print("task=" + self.task, "upload fail", ret)
            else:
                print("image not exist")

        def _image_clean(self):
            print("image cleaning at ", self.image_dir)
            try:
                files = listdir(self.image_dir)
                for file in files:
                    target = join(self.image_dir, file)
                    print("delete ", target)
                    if isfile(target):
                        remove(join(self.image_dir, file))
                    elif isdir(target):
                        rmtree(target)
            except Exception as err:
                print(err)

    task: str
    _profile: str
    valid = False
    _task: TaskThread = None

    def __init__(self, task: str, callback):
        self.task = task
        self._profile = config.get_profile(task)
        self._callback = callback
        if (task is not None) & (self._profile is not None):
            self.valid = True

    def run(self):
        if self.valid:
            self._task = self.TaskThread(self.task, self._profile, self._callback)
            self._task.start()
        else:
            self._callback(self.task)
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
