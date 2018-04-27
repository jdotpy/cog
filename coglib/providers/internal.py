from coglib.core import BaseProvider

import multiprocessing

class InternalPythonProvider(BaseProvider):
    platforms = BaseProvider.PLATFORMS_ALL
    data = {
        'cpu.countLogical': 'cpu_count',
    }

    def cpu_count(self, key):
        return multiprocessing.cpu_count()
