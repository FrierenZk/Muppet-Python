from multiprocessing import Process, Value
from os import chdir, remove, listdir, killpg, getpgid
from os.path import isfile, isdir, join, getsize
from shutil import rmtree
from subprocess import run, Popen, PIPE

from _task import _source_dir, _image_dir, _server_dir, config


class TaskProcess(Process):
    task: str
    shell_process = None

    def __init__(self, task: Value):
        super().__init__()
        self.task = task.value

    def run(self) -> None:
        try:
            if config.get_update(self.task) is not False:
                self._svn_update()
            else:
                print("Svn up skipped")
            self._image_clean()
            ret: bool = self._image_build()
            if ret & config.get_upload(self.task) is True:
                self._image_upload()
            else:
                print("Task", self.task, "finished with no uploaded")
        except Exception as err:
            print(err)

    def terminate(self) -> None:
        if self.shell_process is not None:
            killpg(getpgid(self.shell_process.pid), 9)
        super().terminate()

    def _svn_update(self):
        chdir(_source_dir(self.task))
        if config.get_cleanup(self.task):
            cmd = "svn cleanup "
            if config.get_cleanupSudo(self.task):
                cmd = "sudo " + cmd
            ret = run(cmd + config.get_cleanupPath(self.task), shell=True)
            print("Task=" + self.task, "svn cleanup", ret)
        ret = run("svn up", shell=True)
        print("Task=" + self.task, "svn up", ret)

    def _image_clean(self):
        image_dir = _image_dir(self.task)
        print("Image cleaning at ", image_dir)
        try:
            files = listdir(image_dir)
            for file in files:
                target = join(image_dir, file)
                print("Delete ", target)
                if isfile(target):
                    remove(join(image_dir, file))
                elif isdir(target):
                    rmtree(target)
        except Exception as err:
            print(err)

    def _image_build(self):
        chdir(_source_dir(self.task))
        cmd = "./mkfw.sh " + config.get_profile(self.task)
        cmd = cmd + " clean && " + cmd
        print("Making compilation...")
        self.shell_process = Popen(cmd, shell=True, bufsize=30, stdout=PIPE,
                                   stderr=PIPE)
        out, err = self.shell_process.communicate()
        self.shell_process.wait()
        if self.shell_process.returncode == 0:
            print("Task", cmd, "success")
            return True
        else:
            print("Task=" + self.task, "cmd=" + cmd, "cmd failed")
            print(out)
            print(err)
            return False

    def _image_upload(self):
        image_dir = _image_dir(self.task)
        file_path = ""
        files = listdir(image_dir)
        for file in files:
            if file.find(".tar.gz") == -1:
                continue
            file_path = image_dir + file
            break
        if file_path != "":
            if getsize(file_path) < (1024 * 1024):
                print("Task", self.task, file_path, "size is not right, upload canceled")
                return
            ret = run(
                "sudo sshpass -p 654321 scp " + file_path + " buildmanager@" + _server_dir(self.task), shell=True)
            if ret.returncode == 0:
                print("Task=" + self.task, "upload success")
            else:
                print("Task=" + self.task, "upload fail", ret)
        else:
            print("Image not exist")
