from coglib.core import BaseProvider
from coglib import utils

class LsofProvider(BaseProvider):
    platforms = BaseProvider.PLATFORMS_UNIX
    data = {
        'net.open': 'get_open_ports',
    }

    def get_open_ports(self, key):
        stdout = self._exec(['lsof', '+c0', '-nPi'])
        return utils.parse_whitespace_table(stdout)
