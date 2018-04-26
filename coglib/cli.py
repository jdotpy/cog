import argparse
import sys

from .plugins.basicLoad import BasicLoadPlugin

class CLI():
    name = 'cog'
    PLUGIN_CLASSES = [
        BasicLoadPlugin,
    ]

    def __init__(self):
        self._parser = argparse.ArgumentParser(prog=self.name)
        self._subparsers = self._parser.add_subparsers(dest='cmd')
        self._initialize_plugins();


    def _initialize_plugins(self):
        self.plugins = []

        for Plugin in self.PLUGIN_CLASSES:
            self.plugins.append(Plugin(cli))

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

