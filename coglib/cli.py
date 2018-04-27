import argparse
import sys

from .providers.sysctl import SysctlProvider
from .plugins.basicLoad import BasicLoadPlugin
from .core import BaseProvider

from .utils import import_class

class NoPlatformFoundError(ValueError):
    pass

class CLI():
    name = 'cog'

    PROVIDER_CLASSES = [
        'coglib.providers.internal.InternalPythonProvider',
        'coglib.providers.sysctl.SysctlProvider',
        'coglib.providers.procFiles.ProcFileProvider',
    ]
    PLUGIN_CLASSES = [
        'coglib.plugins.basicLoad.BasicLoadPlugin',
    ]

    def __init__(self):
        self._platform = BaseProvider.detect_platform()
        self._parser = argparse.ArgumentParser(prog=self.name)
        self._subparsers = self._parser.add_subparsers(dest='cmd')
        self._initialize_plugins();

    def get_data(self, key):
        sources = self.data_sources.get(key, [])
        if not sources:
            raise NoPlatformFoundError()

        source = sources[0]
        return source.get_data(key)

    def _initialize_plugins(self):
        self.plugins = []
        self.providers = []
        self.data_sources = {}

        for path in self.PROVIDER_CLASSES:
            ProviderClass = import_class(path)
            provider = ProviderClass(self)
            if not provider.is_supported(self._platform):
                continue

            self.providers.append(provider)
            for key, func_name in provider.data.items():
                if key not in self.data_sources:
                    self.data_sources[key] = [provider]
                else:
                    self.data_sources[key].append(provider)
        for path in self.PLUGIN_CLASSES:
            plugin = import_class(path)(self)
            self.plugins.append(plugin)

        for plugin in self.plugins:
            for command_meta in plugin.commands:
                command_name = command_meta.get('command')
                command_func = getattr(plugin, command_meta.get('func', 'command'))
                command_args = command_meta.get('args', {})

                plugin_parser = self._subparsers.add_parser(command_name)
                plugin_parser.set_defaults(func=command_func)
                for arg_key, arg_options in command_args.items():
                    plugin_parser.add_argument(arg_key, **arg_options)

    def run(self):
        args = self._parser.parse_args()
        if not args.cmd:
            self._parser.print_help()
            sys.exit(1)

        args.func(args)


def cli():
    print('COG the main')


def init():
    cli = CLI()
    cli.run()

