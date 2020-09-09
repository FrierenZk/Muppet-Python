import socketio
from time import sleep

if __name__ == "__main__":
    print(1)
    sio = socketio.Client()
    sio.connect('http://localhost:21518')


    @sio.event
    def available_list(data):
        print(data)


    @sio.event
    def processing_list(data):
        print(data)


    @sio.event
    def waiting_list(data):
        print(data)


    @sio.event
    def add_task(data):
        print(data)


    @sio.event
    def stop_task(data):
        print(data)

    @sio.event
    def broadcast_logs(data):
        print(data)


    sio.emit('connect')
    sio.emit('get_available_list')
    sio.emit('get_processing_list')
    sio.emit('get_waiting_list')
    sio.emit('set_add_task', 'wifi6')
    sio.emit('set_stop_task', 'wifi6')
    sleep(10)
    sio.disconnect()
