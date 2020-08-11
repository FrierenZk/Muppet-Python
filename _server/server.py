from json import dumps
from multiprocessing import Queue
from threading import Thread
from engineio.async_drivers import gevent

import socketio
from eliot import to_file, start_action
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

from _task import config

to_file(open("server.log", "w"))


class Server(Thread):
    sio = socketio.Server(async_mode='gevent')
    app = socketio.WSGIApp(sio)
    queue = Queue()
    status = True

    def run(self) -> None:
        @self.sio.event
        def connect(sid, environ=None):
            with start_action(action_type='connect', sid=sid, environ=environ):
                if environ is not None:
                    print(sid, environ, 'Now connected')
                else:
                    print(sid, 'Now connected')

        @self.sio.event
        def disconnect(sid, environ=None):
            with start_action(action_type='disconnect', sid=sid, environ=environ):
                if environ is not None:
                    print(sid, environ, 'Now disconnected')
                else:
                    print(sid, 'Now disconnected')

        @self.sio.event
        def get_task_list(sid, data=None):
            with start_action(action_type='get_task_list', sid=sid, data=data):
                print(sid, 'Calling get_task_list')
                Thread(target=self.get_task_list, args=(sid,)).start()

        @self.sio.event
        def get_list(sid, data=None):
            with start_action(action_type='get_list', sid=sid, data=data):
                print(sid, 'Calling get_list')
                Thread(target=self.get_list, args=(sid,), daemon=True).start()

        @self.sio.event
        def get_waiting_count(sid, data=None):
            with start_action(action_type='get_waiting_count', sid=sid, data=data):
                print(sid, 'Calling get_waiting_count')
                Thread(target=self.get_waiting_count, args=(sid,), daemon=True).start()

        @self.sio.event
        def add_task(sid, data):
            with start_action(action_type='add_task', sid=sid, data=data):
                print(sid, 'Calling add_task', data)
                Thread(target=self.add_task, args=(sid, data,), daemon=True).start()

        @self.sio.event
        def stop_task(sid, data):
            with start_action(action_type='stop_task', sid=sid, data=data):
                print(sid, 'Calling stop_task', data)
                Thread(target=self.stop_task, args=(sid, data), daemon=True).start()

        print("Listen on port 21518")
        WSGIServer(('0.0.0.0', 21518), self.app, handler_class=WebSocketHandler).serve_forever()

    def __init__(self, callback_get_waiting_count, callback_get_task_list, callback_add_task, callback_stop_task):
        super(Server, self).__init__()
        self._callback_get_waiting_count = callback_get_waiting_count
        self._callback_get_task_list = callback_get_task_list
        self._callback_add_task = callback_add_task
        self._callback_stop_task = callback_stop_task

    def terminate(self):
        self.status = False
        self.queue.put('server terminate', block=True)

    def __del__(self):
        self.terminate()

    def get_waiting_count(self, sid):
        data = self._callback_get_waiting_count()
        self.sio.emit(event='waiting_count', room=sid, data=data)

    def get_task_list(self, sid):
        data = self._callback_get_task_list()
        data = dumps(data)
        self.sio.emit(event='task_list', room=sid, data=data)

    def add_task(self, sid, data):
        self._callback_add_task(line='execute ' + data)
        self.sio.emit(event='add', room=sid, data='Add ' + data + ' done')

    def stop_task(self, sid, data):
        self._callback_stop_task(task=data, flag=False)
        self.sio.emit(event='stop', room=sid, data='Stop ' + data + ' done')

    def get_list(self, sid):
        data = {}
        tasks = config.get_tasks()
        for i in tasks:
            data[i] = config.get_category(i)
        data = dumps(data)
        self.sio.emit(event='list', room=sid, data=data)
