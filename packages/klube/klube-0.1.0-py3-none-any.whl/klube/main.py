#!/usr/bin/env python3
import subprocess
import sys
import importlib
import config
from commands.base import BaseHandler


def import_handler(command: str, args: list[str]) -> BaseHandler:
    module_path = f"klube.commands.{command}.handler.Handler"
    module_name, class_name = module_path.rsplit(".", 1)

    module = importlib.import_module(module_name)
    handler_class = getattr(module, class_name)

    return handler_class

def main():
    command = sys.argv[1]
    args = sys.argv[2:]

    try:
        handler = import_handler(command, args)
        handler(args, config=config).handle()
    except ModuleNotFoundError:
        cmd = ["kubectl", "-n", config.NAMESPACE, command, *args]
        print(" ".join(cmd))
        subprocess.call(cmd)


if __name__ == "__main__":
    main()
