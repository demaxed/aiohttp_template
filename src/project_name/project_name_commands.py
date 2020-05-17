import argparse
import pwd

from configargparse import ArgumentParser
from aiomisc.log import LogFormat, basic_config

class ProjectnameCommand:

    def a(self):
        parser = ArgumentParser(
            auto_env_var_prefix=ENV_VAR_PREFIX, allow_abbrev=False,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument('--user', required=False, type=pwd.getpwnam,
                            help='Change process UID')

        group = parser.add_argument_group('API Options')
        group.add_argument('--api-address', default='0.0.0.0',
                           help='IPv4/IPv6 address API server would listen on')
        group.add_argument('--api-port', type=int, default=8081,
                           help='TCP port API server would listen on')

        group = parser.add_argument_group('Logging options')
        group.add_argument('--log-level', default='info',
                           choices=('debug', 'info', 'warning', 'error', 'fatal'))
        group.add_argument('--log-format', choices=LogFormat.choices(),
                           default='color')

    def handler(self):
        pass
