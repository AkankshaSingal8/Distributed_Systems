import zmq

class MessageServer:
    def __init__(self):
        self.groups = {}

    def register_group(self, group_name, ip_address):
        self.groups[group_name] = ip_address

    def get_group_list(self, uuid):
        group_list = '\n'.join([f'{group_name} - {ip_address}' for group_name, ip_address in self.groups.items()])
        print(f'\nGROUP LIST REQUEST FROM {uuid}')
        print(f'Group list sent')
        return group_list

    def extract_port(self):
        ports = []
        for group_name, ip_address in self.groups.items():
            parts = ip_address.split(':')
            port_number = parts[-1]
            ports.append(port_number)
        return ports


context = zmq.Context()
server = MessageServer()
receiver = context.socket(zmq.REP)
receiver.bind('tcp://*:4000')
print('Hello, Admin! Message Server is ON at port 4000')

while True:
    message = receiver.recv_json()
    if message.get('action') == 'register':
        print(f'\nNew Joining Request!\n'
                f'JOIN REQUEST FROM {message.get("ip_address")}\n'
                f'Register group? (y/n)', end=" ")
        res = input()
        if res == 'y':
            server.register_group(message.get('group_name'), message.get('ip_address'))
            receiver.send_string('Group registration: SUCCESS')
            print('Group registered.')
        else:
            receiver.send_string('Group registration: FAILED')

    elif message.get('action') == 'get_group_list':
        group_list = server.get_group_list(message.get('uuid'))
        receiver.send_string(group_list)
    
    elif message.get('action') == 'extract_port':
        port_list = server.extract_port()
        receiver.send_string(str(port_list))
