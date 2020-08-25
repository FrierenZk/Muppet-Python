from multiprocessing import Queue
from threading import Thread
from json import load, dumps

import socketio
from eliot import to_file, start_action
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

# noinspection PyUnresolvedReferences
from engineio.async_drivers import gevent

from _task import config

to_file(open("server.log", "w"))


class Server(Thread):
    sio = socketio.Server(async_mode='gevent')
    app = socketio.WSGIApp(sio)
    queue = Queue()
    status = True
    broadcast = "broadcast_room"

    def run(self) -> None:
        @self.sio.event
        def connect(sid, environ=None):
            with start_action(action_type='connect', sid=sid, environ=environ):
                if environ is not None:
                    print(sid, environ, 'Now connected')
                else:
                    print(sid, 'Now connected')
                self.sio.enter_room(sid, self.broadcast)

        @self.sio.event
        def disconnect(sid, environ=None):
            with start_action(action_type='disconnect', sid=sid, environ=environ):
                if environ is not None:
                    print(sid, environ, 'Now disconnected')
                else:
                    print(sid, 'Now disconnected')
                self.sio.leave_room(sid, self.broadcast)

        @self.sio.event
        def get_processing_list(sid, data=None):
            with start_action(action_type='get_processing_list', sid=sid, data=data):
                print(sid, 'Calling get_processing_list')
                Thread(target=self.get_processing_list, args=(sid,)).start()

        @self.sio.event
        def get_available_list(sid, data=None):
            with start_action(action_type='get_available_list', sid=sid, data=data):
                print(sid, 'Calling get_available_list')
                Thread(target=self.get_available_list, args=(sid,), daemon=True).start()

        @self.sio.event
        def get_waiting_list(sid, data=None):
            with start_action(action_type='get_waiting_list', sid=sid, data=data):
                print(sid, 'Calling get_waiting_list')
                Thread(target=self.get_waiting_list, args=(sid,), daemon=True).start()

        @self.sio.event
        def set_add_task(sid, data):
            with start_action(action_type='add_task', sid=sid, data=data):
                print(sid, 'Calling add_task', data)
                Thread(target=self.set_add_task, args=(sid, data,), daemon=True).start()

        @self.sio.event
        def set_stop_task(sid, data):
            with start_action(action_type='stop_task', sid=sid, data=data):
                print(sid, 'Calling stop_task', data)
                Thread(target=self.set_stop_task, args=(sid, data), daemon=True).start()

        port: int = 0
        try:
            with open("server_settings.json", 'r') as file:
                dic = load(file)
                dic: dict
                if 'port' in dic.keys():
                    port = int(dic['port'])
        except Exception as e:
            print(e)
        finally:
            if port <= 0:
                print("Read server_settings.json error, use default port 21518")
                port = 21518

        print("Listen on port", port)
        WSGIServer(('0.0.0.0', port), self.app, handler_class=WebSocketHandler).serve_forever()

    def __init__(self, interface):
        super(Server, self).__init__()
        from _server.server_callback_interface import ServerCallBackInterface
        self.interface: ServerCallBackInterface = interface

    def terminate(self):
        self.status = False
        self.queue.put('server terminate', block=True)

    def __del__(self):
        self.terminate()

    def get_waiting_list(self, sid):
        data = self.interface.get_waiting_list()
        data = dumps(data)
        self.sio.emit(event='waiting_list', room=sid, data=data)

    def get_processing_list(self, sid):
        data = self.interface.get_processing_list()
        data = dumps(data)
        self.sio.emit(event='processing_list', room=sid, data=data)

    def set_add_task(self, sid, data):
        self.interface.add_task(line='execute ' + data)
        self.sio.emit(event='add_task', room=sid, data='Add ' + data + ' done')

    def set_stop_task(self, sid, data):
        self.interface.stop_task(task=data, flag=False)
        self.sio.emit(event='stop_task', room=sid, data='Stop ' + data + ' done')

    def get_available_list(self, sid):
        data = {}
        tasks = config.get_tasks()
        for i in tasks:
            data[i] = config.get_category(i)
        data = dumps(data)
        self.sio.emit(event='available_list', room=sid, data=data)

    def broadcast_logs(self, task: str, log: str):
        try:
            data = {'task': task, 'broadcast_logs': log}
            self.sio.emit(event='broadcast_logs', room=self.broadcast, data=dumps(data))
        except Exception as e:
            print(e)

    def broadcast_task_status_change(self, task: str, state: str):
        try:
            data = {'task': task, 'state': state}
            self.sio.emit(event='broadcast_task_status_change', room=self.broadcast, data=dumps(data))
        except Exception as e:
            print(e)

    def broadcast_task_finish(self, task: str, msg: str):
        try:
            self.broadcast_task_status_change(task, "stopped")
            data = {'task': task, 'msg': msg}
            self.sio.emit(event='broadcast_task_finish', room=self.broadcast, data=dumps(data))
        except Exception as e:
            print(e)
