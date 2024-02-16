import zmq
from threading import Thread
import sys

class GroupServer:
    def __init__(self, sender, receiver, group_name, ip_port, registered=False):
        self.users = set()
        self.messages = []
        self.sender = sender
        self.receiver = receiver
        self.group_name = group_name
        self.ip_port = ip_port
        self.registered = False

    def register_group(self):
        print('Registering at Message Server on port 4000')
        self.sender.send_json({'action': 'register', 'group_name': self.group_name, 'ip_address': 'tcp://' + grp_ip + ':' + str(self.ip_port)})
        response = self.sender.recv_string()
        if 'SUCCESS' in response:
            self.registered = True
        print(response)

    def join_group(self, user_uuid):
        print(f'\nGROUP JOIN REQUEST FROM {user_uuid}')
        self.users.add(user_uuid)
        self.receiver.send_string('Group joining: SUCCESS')

    def leave_group(self, user_uuid):
        if user_uuid in self.users:
            self.users.remove(user_uuid)
            print(f'\nGROUP LEAVE REQUEST FROM {user_uuid}')
            self.receiver.send_string('Leave request: SUCCESS')
        else:
            self.receiver.send_string('Leave request: FAILED')
    
    def get_message(self, user_uuid, time):
        if time != '':
            filtered_messages = [msg['message'] for msg in self.messages if msg['time'] >= time]
        else:
            filtered_messages = [msg['message'] for msg in self.messages]
        if user_uuid in self.users:
            print(f'\nMESSAGE REQUEST FROM {user_uuid}')
            message_str = '\n'.join(filtered_messages)
            self.receiver.send_string(message_str)
        else:
            self.receiver.send_string('Could not get messages')

    def send_message(self, message, user_uuid, time):
        self.messages.append({'user_uuid': user_uuid, 'message': message, 'time': time})
        if user_uuid in self.users:
            print(f'\nMESSAGE SENT FROM {user_uuid} at date_time {time}\n{message}')
            self.receiver.send_string('Message sending: SUCCESS')
        else:
            self.receiver.send_string('Message sending: FAILED')


def find_available_port(starting_port):
    current_port = starting_port
    while True:
        try:
            context = zmq.Context()
            temp_socket = context.socket(zmq.SUB)
            temp_socket.bind("tcp://*:{}".format(current_port + 1))
            temp_socket.close()
            return current_port
        except zmq.error.ZMQError:
            current_port += 2

def group_server(port):
    context = zmq.Context()
    receiver = context.socket(zmq.REP)
    receiver.bind('tcp://*:{}'.format(port))
    broadcaster = context.socket(zmq.PUB)
    broadcaster.bind('tcp://*:{}'.format(port + 1))
    sender = context.socket(zmq.REQ)
    sender.connect('tcp://{}:4000'.format(msg_ip))

    group_server = GroupServer(sender, receiver, group, port)
    group_server.register_group()
    while group_server.registered != True:
        print('\nRetry? (y/n) ', end='')
        res = input()
        if res == 'y':
            group_server.register_group()
        else:
            break

    while True:
        user_msg = receiver.recv_json()
        if user_msg.get('action') == 'join_group':
            group_server.join_group(user_msg.get('user_uuid'))

        elif user_msg.get('action') == 'leave_group':
            group_server.leave_group(user_msg.get('user_uuid'))

        elif user_msg.get('action') == 'get_message':
            group_server.get_message(user_msg.get('user_uuid'), user_msg.get('time'))

        elif user_msg.get('action') == 'send_message':
            group_server.send_message(user_msg.get('message'), user_msg.get('user_uuid'), user_msg.get('time'))

group = sys.argv[1]

grp_ip = '10.190.0.3'
msg_ip = '10.190.0.2'
# grp_ip = '127.0.0.1'
# msg_ip = '127.0.0.1'

starting_port = 5678
ports = [starting_port + i for i in range(0, 3)]
port = find_available_port(starting_port)

thread = Thread(target=group_server, args=(port,))
thread.start()
