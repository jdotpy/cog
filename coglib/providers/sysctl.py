from coglib.core import BaseProvider


class SysctlProvider(BaseProvider):
    platforms = {BaseProvider.PLATFORM_MACOS}
    data = {
        'cpu.loadAvg': 'cpu_load_average',
    }
    
    def _get_attribute(self, name):
        self._exec(['sysctl', '-n', name])


    def cpu_load_average(self):
        average_data = self._get_attribute('vm.loadavg')
        averages = average_data.strip().strip('{}').strip().split(' ')
        return [float(avg) for avg in averages]

    def cpu_count(self):
        result = self._get_attribute('hw.ncpu')
        return int(result.strip())
