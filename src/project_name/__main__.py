import argparse
import logging
import os
import pwd
from sys import argv

from aiohttp.web import run_app
from aiomisc import bind_socket
from aiomisc.log import LogFormat, basic_config
from configargparse import ArgumentParser
from setproctitle import setproctitle
from yarl import URL

from analyzer.api.app import create_app
from analyzer.utils.argparse import clear_environ, positive_int
from analyzer.utils.pg import DEFAULT_PG_URL

from project_name.project_name_commands import ProjectnameCommand

commands = (
    ProjectnameCommand,
)


def main():
    args = parser.parse_args()

    clear_environ(lambda i: i.startswith(ENV_VAR_PREFIX))

    # Чтобы логи не блокировали основной поток (и event loop) во время операций
    # записи в stderr или файл - логи можно буфферизовать и обрабатывать в
    # отдельном потоке (aiomisc.basic_config настроит буфферизацию
    # автоматически).
    basic_config(args.log_level, args.log_format, buffered=True)

    # Аллоцируем сокет из под привиллегированного пользователя отдельным шагом,
    # чтобы была возможность перед запуском приложения сменить пользователя ОС.
    sock = bind_socket(
        address=args.api_address,
        port=args.api_port,
        proto_name='http',
    )

    # После того как приложение аллоцировало сокет и ему больше не нужны
    # привиллегии - хорошим решением будет сменить пользователя (например,
    # на nobody, у которого нет никаких специальных привиллегий) - это также
    # усложнит жизнь злоумышленникам.
    if args.user is not None:
        logging.info('Changing user to %r', args.user.pw_name)
        os.setgid(args.user.pw_gid)
        os.setuid(args.user.pw_uid)

    # В списке процессов намного удобнее видеть название текущего приложения
    setproctitle(os.path.basename(argv[0]))

    app = create_app(args)
    run_app(app, sock=sock)


if __name__ == '__main__':
    main()
