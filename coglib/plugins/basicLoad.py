from coglib.core import BasePlugin

from pprint import pprint
import re

def slugify(key):
    return key.strip().replace(' ', '_').lower()

def whitespace_delimited_parse(text):
    return re.split('\s+', text)

def find_all(text, snippet):
    indexes = []
    index = None
    while index != -1:
        if index is not None:
            start = index + 1
        else:
            start = 0
        index = text.find(snippet, start)
        if index != -1:
            indexes.append(index)
    return indexes

def split_at_indexes(text, source_bps):
    # Ensure breakpoints is a sorted list
    breakpoints = list(source_bps)
    breakpoints.sort()
    chunks = []
    for index, breakpoint in enumerate(breakpoints):
        if index == 0:
            start = 0
        else:
            start = breakpoints[index - 1]
        chunks.append(text[start:breakpoint])
    if breakpoints[-1] < len(text) - 1:
        chunks.append(text[breakpoints[-1]:])
    return chunks

def parse_whitespace_table(text):
    lines = text.splitlines()
    header = lines[0]
    initial = True

    # Start with a baseline of the spaces in headers
    breakpoints = set()
    breakpoints.update(find_all(header, ' '))

    # Remove breakpoints used in body
    invalid_used = set()
    for line in lines[1:]:
        for breakpoint in breakpoints:
            if line[breakpoint] != ' ':
                invalid_used.add(breakpoint)
    breakpoints = breakpoints - invalid_used

    # Remove "redundant" breakpoints that are sequential keeping the earliest one
    redundant = set()
    for breakpoint in breakpoints:
        if (breakpoint - 1) in breakpoints:
            redundant.add(breakpoint)
    breakpoints = breakpoints - redundant

    columns = [col.strip() for col in split_at_indexes(lines[0], breakpoints)]
    rows = []
    for line in lines[1:]:
        row_data = [col.strip() for col in split_at_indexes(line, breakpoints)]
        rows.append(dict(zip(columns, row_data)))
    return rows

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

def darwin_listening_ports():
    command_result = subprocess.run(['lsof', '+c0', '-nP', '-i'], stdout=subprocess.PIPE)
    raw_output = command_result.stdout.decode('utf-8')
    data = parse_whitespace_table(raw_output)
    just_listening = [entry for entry in data if 'LISTEN' in entry.get('NAME', '')]
    for entry in just_listening:
        binding = entry['NAME'].split(' ')[0]
        entry['binding'] = binding
        entry['port'] = binding[binding.rfind(':') + 1:]

    return just_listening

def progress_bar(value, ceiling, markers=None, row_count=50):
    percent_filled = value / ceiling
    used_rows = int((percent_filled) * row_count)
    blank_rows = row_count - used_rows

    bar = '{}{}'.format('#' * used_rows, '-' * blank_rows)
    if markers:
        for marker in markers:
            location = int((marker / ceiling) * row_count)
            bar = bar[:location] + '|' + bar[location + 1:]
    return '[{}]'.format(bar)

class BasicLoadPlugin(BasePlugin):
    commands = [
        {
            'command': 'load',
            'func': 'cpu_load',
            'args': {},
        },
        #{
        #    'command': 'net:open',
        #    'func': 'listening_ports',
        #    'args': {
        #        '--foo': { 'action': 'store_true', 'help': 'Foobar help!' },
        #     },
        #}
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
