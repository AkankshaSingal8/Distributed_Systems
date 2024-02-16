import zmq
from threading import Thread
import sys
import uuid
from datetime import datetime

class User:
    def __init__(self, uuid):
        self.uuid = uuid

    def connect_socket(self, ip, port):
        context = zmq.Context()
        socket = context.socket(zmq.REQ)
        socket.connect('tcp://{}:{}'.format(ip, port))
        return socket

    def get_group_list(self):
        socket = self.connect_socket(msg_ip, 4000)
        socket.send_json({'action': 'get_group_list', 'uuid': str(self.uuid)})
        response = socket.recv_string()
        print('\nGroup List')
        print(response)

    def extract_port(self):
        socket = self.connect_socket(msg_ip, 4000)
        socket.send_json({'action': 'extract_port'})
        response = socket.recv_string()
        return response

    def join_group(self, port):
        socket = self.connect_socket(grp_ip, port)
        socket.send_json({'action': 'join_group', 'user_uuid': str(self.uuid)})
        response = socket.recv_string()
        print(response)

    def leave_group(self, port):
        socket = self.connect_socket(grp_ip, port)
        socket.send_json({'action': 'leave_group', 'user_uuid': str(self.uuid)})
        response = socket.recv_string()
        print(response)

    def get_message(self, port, time):
        socket = self.connect_socket(grp_ip, port)
        socket.send_json({'action': 'get_message', 'user_uuid': str(self.uuid), 'time': time})
        response = socket.recv_string()
        print(response)

    def send_message(self, port):
        socket = self.connect_socket(grp_ip, port)
        message = input("[{0}] > ".format(user_name))
        message = "[%s]:  %s" % (user_name, message)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        socket.send_json({'action': 'send_message', 'user_uuid': str(self.uuid), 'message': message, 'time': dt_string})
        response = socket.recv_string()
        print(response)


user_name = sys.argv[1]

grp_ip = '34.131.142.50'
msg_ip = '34.131.129.181'
# grp_ip = '127.0.0.1'
# msg_ip = '127.0.0.1'

user_uuid = uuid.uuid4()
user = User(user_uuid)

while True:
    print(f'\n1. Get group list\n'
          f'2. Join a group\n'
          f'3. Leave a group\n'
          f'4. Get message\n'
          f'5. Send message\n')
    resp = input()
    if resp == '1':
        user.get_group_list()
    else:
        print('Enter port: ', end="")
        port = int(input())
        if str(port) in user.extract_port():
            if resp == '2':
                user.join_group(port)
            elif resp == '3':
                user.leave_group(port)
            elif resp == '4':
                print('Enter timestamp (DD/MM/YYYY HH:MM:SS): ', end="")
                time = input()
                user.get_message(port, time)
            elif resp == '5':
                user.send_message(port)
        else:
            print('No group found at input port')
