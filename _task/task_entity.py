from os import chdir, listdir, remove
from os.path import join, isfile, isdir, getsize
from shutil import rmtree
from subprocess import PIPE, Popen, run
from threading import Thread

from _task.config import config
from _task.path import _server_dir, _source_dir, _image_dir


class TaskEntity:
    class TaskThread(Thread):
        shell_process: Popen = None

        def run(self) -> None:
            try:
                chdir(_source_dir(self.task))
                if config.get_update(self.task) != False:
                    if config.get_cleanup(self.task):
                        cmd = "svn cleanup "
                        if config.get_cleanupSudo():
                            cmd = "Sudo "+cmd
                        ret = run(cmd + config.get_cleanupPath(self.task), shell=True)
                        print("task=" + self.task, "svn cleanup", ret)
                    ret = run("svn up", shell=True)
                    print("task=" + self.task, "svn up", ret)
                else:
                    print("svn up skipped")
                cmd = "./mkfw.sh " + self.profile
                cmd = cmd + " clean && " + cmd
                self._image_clean()
                print("making compilation...")
                self.shell_process = Popen(cmd, shell=True, bufsize=30, stdout=PIPE,
                                           stderr=PIPE)
                out, err = self.shell_process.communicate()
                self.shell_process.wait()
                if self.shell_process.returncode == 0:
                    print(cmd, "success")
                    if config.get_upload(self.task):
                        self._upload_image()
                    else:
                        print(self.task, "finished with no uploaded")
                else:
                    print("task=" + self.task, "cmd=" + cmd, "cmd failed")
                    print(out)
                    print(err)
            except Exception as err:
                print(self.task, err)
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
            if file_path != "":
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
            if self.task is None:
                self.task = "None"
            if self._profile is None:
                self._profile = "None"
            print("task invalid", "task=" + self.task, "profile=" + self._profile)

    def terminate(self):
        if self._task is None:
            return
        if self._task.shell_process.poll() is None:
            self._task.shell_process.terminate()
        print("task", self.task, "terminated")
        return

    def __del__(self):
        if self._task is None:
            return
        if self._task.shell_process is None:
            return
        self._task.shell_process.kill()
