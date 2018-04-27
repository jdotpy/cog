from coglib.core import BasePlugin
from coglib import utils

class NetPlugin(BasePlugin):
    commands = [
        {
            'command': 'net:open',
            'func': 'listening_ports',
            'args': {},
        }
    ]

    def listening_ports(self, args):
        net_query = self.get_data('net.open')
        listening = [entry for entry in net_query if 'LISTEN' in entry['NAME']]
        for entry in listening:
            binding = entry['NAME'].split(' ')[0]
            entry['binding'] = binding
            entry['port'] = binding[binding.rfind(':') + 1:]
        
        cols = ['PID', 'COMMAND', 'binding', 'port']
        print('\t'.join(cols))
        for entry in listening:
            row_data = [entry.get(col) for col in cols]
            print('{}\t{}\t{}\t{}'.format(*row_data))
