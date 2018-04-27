from coglib.core import BaseProvider

class NetstatProvider(BaseProvider):
    platforms = BaseProvider.PLATFORMS_UNIX
    data = {
        #'net.open': 'get_open_ports',
    }

    def get_open_ports(self, key):
        if self.cli.platform == self.PLATFORM_MACOS:
            command = ['netstat', '-p', 'TCP', '-lant']
        else:
            command = ['netstat', '-plant']
        output = self._exec(command)
        return output
        return [float(avg) for avg in averages]
