from coglib.core import BasePlugin
from coglib import utils

class BasicLoadPlugin(BasePlugin):
    commands = [
        {
            'command': 'load',
            'func': 'cpu_load',
            'args': {},
        },
    ]

    def __init__(self, cli):
        self.cli = cli

    def cpu_load(self, args):
        cpu_count = self.get_data('cpu.countLogical')
        averages = self.get_data('cpu.loadAvg')
        average = averages[0]
        ceiling = max(average, 2 * cpu_count)
        if average > cpu_count:
            # Overloaded
            print(average, progress_bar(average, average, markers=[cpu_count]))
        else:
            print(average, progress_bar(average, cpu_count))

    def listening_ports(self, args):
        listening_processes = darwin_listening_ports()
        for entry in listening_processes:
            print('{}\t{}\t{}\t{}'.format(
                entry.get('PID'),
                entry.get('COMMAND'),
                entry.get('binding'),
                entry.get('port'),
            ))
