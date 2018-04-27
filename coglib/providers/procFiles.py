from coglib.core import BaseProvider


class ProcFileProvider(BaseProvider):
    platforms = {BaseProvider.PLATFORM_LINUX}
    data = {
        'cpu.loadAvg': 'cpu_load_average',
    }
    
    def cpu_load_average(self, key):
        average_data = self._cat_file('/proc/loadavg')
        averages = average_data.split(' ')[:3]
        return [float(avg) for avg in averages]
