from threading import Thread
from os import chdir, remove, listdir, setsid
from os.path import isfile, isdir, join, getsize
from shutil import rmtree
from subprocess import run, Popen, PIPE

from _task.config import config
from _task.path import _image_dir, _source_dir, _upload_dir


class TaskThread(Thread):
    task: str
    shell_process = None
    status = True

    def __init__(self, task: str, callback, svn_check=False):
        super().__init__()
        self.task = task
        self.finish = callback
        self.svn_check = svn_check

    def run(self) -> None:
        try:
            if config.get_svnNoUpdate(task=self.task):
                self.push_with_print("Svn up skipped")
            else:
                self.status &= self._svn_update()
            self._image_clean()
            ret: bool = self._image_build()
            if ret & config.get_upload(self.task) is True:
                self._image_upload()
            else:
                self.push_with_print("Task", self.task, "finished with no uploaded")
        except Exception as err:
            self.push_with_print(err)
        finally:
            self.finish(self.task)

    def terminate(self) -> None:
        self.status = False
        if self.shell_process is None:
            return
        from os import killpg
        from signal import SIGKILL, SIGINT
        killpg(self.shell_process.pid, SIGKILL)
        while self.shell_process.poll() is None:
            self.shell_process.send_signal(SIGINT)

    # Test
    @staticmethod
    def push_logs(task: str, string: str):
        pass

    def push_with_print(self, *args):
        string = ""
        fix = False
        for i in args:
            if fix:
                string += " "
            else:
                fix = True
            string += str(i)
        if string == "":
            return
        print(string)
        self.push_logs(self.task, string)

    def awaitProcess(self) -> int:
        while True:
            outputBytes: bytes = self.shell_process.stdout.readline()
            output: str = str(outputBytes, encoding='utf8').strip()
            if output == '' and self.shell_process.poll() is not None:
                break
            if output:
                self.push_with_print(output)
        return self.shell_process.poll()

    def _svn_update(self) -> bool:
        # preUpdate
        svn = ""
        if self.svn_check:
            svn = self._svn_info()
        # Update
        if not self.status:
            return self.status
        chdir(_source_dir(self.task))
        from os import setsid
        self.shell_process = Popen("svn up", shell=True, stdout=PIPE, stderr=PIPE,
                                   preexec_fn=setsid)
        ret = self.awaitProcess()
        self.push_with_print("Task=" + self.task, "svn up", ret)
        if ret != 0:
            return False
        # postUpdate
        if self.svn_check:
            svn2 = self._svn_info()
            if svn == svn2:
                self.push_with_print("Svn have no change, build skipped")
                return False
        return True

    def _svn_info(self) -> str:
        chdir(_source_dir(self.task))
        cmd = "svn info | grep \"Last Changed Rev\""
        process = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
        out, _ = process.communicate()
        process.wait()
        self.push_with_print(out)
        return str(out)

    def _image_clean(self):
        image_dir = _image_dir(self.task)
        self.push_with_print("Image cleaning at ", image_dir)
        try:
            files = listdir(image_dir)
            for file in files:
                target = join(image_dir, file)
                self.push_with_print("Delete ", target)
                if isfile(target):
                    remove(join(image_dir, file))
                elif isdir(target):
                    rmtree(target)
        except Exception as err:
            self.push_with_print(err)

    def _image_build(self) -> bool:
        if not self.status:
            return self.status
        chdir(_source_dir(self.task))
        cmd = "./mkfw.sh " + config.get_profile(self.task)
        cmd = cmd + " clean && " + cmd
        self.push_with_print("Making compilation...")
        self.shell_process = Popen(cmd, shell=True, bufsize=30, stdout=PIPE,
                                   stderr=PIPE, preexec_fn=setsid)
        ret = self.awaitProcess()
        if ret == 0:
            self.push_with_print("Task", cmd, "success")
            return True
        else:
            self.push_with_print("Task=" + self.task, "cmd=" + cmd, "cmd failed")
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
                self.push_with_print("Task", self.task, file_path, "size is not right, upload canceled")
                return
            ret = run(
                "sudo sshpass -p 654321 scp " + file_path + " buildmanager@" + _upload_dir(self.task), shell=True)
            if ret.returncode == 0:
                self.push_with_print("Task=" + self.task, "upload success")
            else:
                self.push_with_print("Task=" + self.task, "upload fail", ret)
        else:
            self.push_with_print("Image not exist")
