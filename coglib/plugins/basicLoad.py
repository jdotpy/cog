import subprocess
from pprint import pprint
import re

def slugify(key):
    return key.strip().replace(' ', '_').lower()

def whitespace_delimited_parse(text):
    return re.split('\s+', text)

def darwin_top():
    command_output = subprocess.run(["top", "-l", "1"], stdout=subprocess.PIPE)
    output = command_output.stdout.decode('utf-8')

    stats, processes_string = output.split('\n\n')

    result = {}
    for line in stats.splitlines():
        key, attributes = line.split(':', maxsplit=1)
        result[slugify(key)] = attributes

    processes = []
    process_table = processes_string.splitlines()
    columns = whitespace_delimited_parse(process_table[0])
    for row in process_table[1:]:
        row_data = whitespace_delimited_parse(row)
        processes.append(dict(zip(columns, row_data)))

    result['processes'] = processes
    return result

def darwin_cpu_count():
    command_output = subprocess.run(['sysctl', '-n', 'hw.ncpu'], stdout=subprocess.PIPE)
    return int(command_output.stdout.decode('utf-8').strip())

def darwin_load_average():
    command_output = subprocess.run(['sysctl', '-n', 'vm.loadavg'], stdout=subprocess.PIPE)
    averages = command_output.stdout.decode('utf-8').strip().strip('{}').strip().split(' ')
    return list(map(float, averages))

def progress_bar(value, ceiling, markers=None, row_count=50):
    percent_filled = value / ceiling
    used_rows = int((percent_filled) * row_count)
    blank_rows = row_count - used_rows

    bar = '{}{}'.format('=' * used_rows, ' ' * blank_rows)
    if markers:
        for marker in markers:
            location = int((marker / ceiling) * row_count)
            bar = bar[:location] + '|' + bar[location + 1:]
    return '[{}]'.format(bar)

class BasicLoadPlugin():
    commands = [
        {
            'command': 'top',
            'func': 'example_command',
            'args': {
                '--foo': { 'action': 'store_true', 'help': 'Foobar help!' },
             },
        }
    ]

    def __init__(self, cli):
        self.cli = cli

    def example_command(self, args):
        cpu_count = darwin_cpu_count()
        averages = darwin_load_average()
        average = averages[0]
        ceiling = max(average, 2 * cpu_count)
        if average > cpu_count:
            # Overloaded
            print(average, progress_bar(average, average, markers=[cpu_count]))
        else:
            # Overloaded
            print(average, progress_bar(average, cpu_count))
