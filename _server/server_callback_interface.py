from abc import ABCMeta, abstractmethod


class ServerCallBackInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_waiting_list(self) -> list:
        pass

    @abstractmethod
    def get_processing_list(self) -> list:
        pass

    @abstractmethod
    def add_task(self, line: str) -> (bool, str):
        pass

    @abstractmethod
    def stop_task(self, task: str, flag: bool) -> None:
        pass
