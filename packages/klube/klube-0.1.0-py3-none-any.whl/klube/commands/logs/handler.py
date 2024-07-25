import subprocess

from klube.commands.base import BaseHandler


class Handler(BaseHandler):
    kube_command = "logs"

    def handle(self):
        print(f"{' '.join(self.command)}")
        subprocess.call(self.command)
