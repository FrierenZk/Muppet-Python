import socketio
from time import sleep

if __name__ == "__main__":
    print(1)
    sio = socketio.Client()
    sio.connect('http://localhost:21518')


    @sio.event
    def task_list(data):
        print(data)


    @sio.event
    def list(data):
        print(data)


    @sio.event
    def waiting_count(data):
        print(data)


    @sio.event
    def add(data):
        print(data)


    @sio.event
    def stop(data):
        print(data)


    sio.emit('connect')
    sio.emit('get_task_list')
    sio.emit('get_list')
    sio.emit('get_waiting_count')
    sio.emit('add_task', 'wifi6')
    sio.emit('stop_task', 'wifi6')
    sleep(1)
    sio.disconnect()
