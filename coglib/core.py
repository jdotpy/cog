import os
import sys
import subprocess

class DataNotProvided(ValueError):
    pass

class PlatformUnsupported(ValueError):
    pass

class BaseProvider():
    PLATFORM_MACOS = object()
    PLATFORM_LINUX = object()
    PLATFORM_FREEBSD = object()
    PLATFORM_WINDOWS = object()
    PLATFORM_ALL = object()
    PLATFORMS_UNIX = {
        PLATFORM_LINUX,
        PLATFORM_MACOS,
        PLATFORM_FREEBSD,
    }
    PLATFORMS_ALL = {
        PLATFORM_WINDOWS,
        PLATFORM_LINUX,
        PLATFORM_MACOS,
    }
    platforms = set()
    data = {}

    def __init__(self, cli):
        self.cli = cli

    @classmethod
    def detect_platform(cls):
        if sys.platform.startswith('freebsd'):
            return cls.PLATFORM_FREEBSD
        elif sys.platform.startswith('linux'):
            return cls.PLATFORM_LINUX
        elif sys.platform.startswith('win32'):
            return cls.PLATFORM_WINDOWS
        elif sys.platform.startswith('darwin'):
            return cls.PLATFORM_MACOS
        else:
            raise PlatformUnsupported()

    def is_supported(self, platform):
        return platform in self.platforms

    def _exec(self, command):
        command_result = subprocess.run(command, stdout=subprocess.PIPE)
        return command_result.decode('utf-8')

    def _cat_file(self, location, encoding='utf-8'):
        with open(location, 'r', encoding=encoding) as f:
            data = f.read()
        return data

    def get_data(self, key):
        if key not in self.data:
            raise DataNotProvided()
        func = self.data[key]
        return getattr(self, func)(key)


class BasePlugin():
    def __init__(self, cli):
        self.cli = cli

    def get_data(self, key):
        return self.cli.get_data(key)
