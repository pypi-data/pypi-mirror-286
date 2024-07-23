import logging
import os
import struct
import sys
from typing import ClassVar

import yaml


class ExtAuthHandler:
    """Base class for extauth handlers"""

    name: ClassVar[str]

    def __init__(self, config: dict, logger: logging.RootLogger):
        self._config = self._parse_config(config)
        self._logger = logger
        self._logger.debug("Handler initialized")

    def _parse_config(config: dict) -> dict:
        return config

    def auth(user: str, server: str, password: str) -> bool:
        raise NotImplementedError

    def is_user(user: str, server: str) -> bool:
        raise NotImplementedError

    def set_pass(user: str, server: str, password: str) -> bool:
        raise NotImplementedError

    def try_register(user: str, server: str, password: str) -> bool:
        raise NotImplementedError

    def remove_user(user: str, server: str, password: str | None = None) -> bool:
        raise NotImplementedError


class ExtAuth:
    def __init__(self, handler: type[ExtAuthHandler]):
        if os.path.isfile(f"/etc/ejabberd/extauth/{handler.name}.yml"):
            with open(f"/etc/ejabberd/extauth/{handler.name}.yml", "r"):
                self._config = yaml.load()
        else:
            self._config = {}

        if level_name := self._config.get("log_level", None):
            logging.basicConfig(level=logging.getLevelName(level_name))
        self._logger = logging.getLogger(__name__)
        self._handler = handler(self._config.get("handler", {}), self._logger)

    def _read_and_handle():
        # Read two bytes to get the length
        length_bytes = sys.stdin.buffer.read(2)
        length = struct.unpack("!h", length_bytes)
        self._logger.debug("Receiving command of length %d", length)

        # Read as many bytes as announced
        command_bytes = sys.stdin.buffer.read(length)
        command_raw = command_bytes.decode()
        self._logger.debug("Received command: %s", command_raw)

        # The packet contains the command and its arguments, split by colon
        command, *args = command_raw.split(":")

        try:
            if command == "auth" and len(args) == 3:
                res = self._handler.auth(*args)
            elif command == "isuser" and len(args) == 2:
                res = self._handler.is_user(*args)
            elif command == "setpass" and len(args) == 3:
                res = self._handler.set_pass(*args)
            elif command == "tryregister" and len(args) == 3:
                res = self._handler.try_register(*args)
            elif command == "removeuser" and len(args) == 2:
                res = self._handler.remove_user(*args)
            elif command == "removeuser3" and len(args) == 3:
                res = self._handler.remove_user(*args)
            else:
                self._logger.error("Command or signature is invalid")
                res = False
        except NotImplementedError:
            self._logger.warning("Command is not implemented in handler; returning failure")
            res = False

        res_bytes = struct.pack("!h", int(res))
        res_bytes = struct.pack("!h", len(res_bytes))

        sys.stdout.buffer.write(res_bytes)
        sys.stdout.buffer.flush()

    def run(self):
        self._logger.info("Starting handling commands from stdin")
        while True:
            self._read_and_handle()
