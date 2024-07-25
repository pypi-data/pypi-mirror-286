from klube.commands.base import BaseHandler
import subprocess


class Handler(BaseHandler):
    kube_command = "exec"

    @property
    def identifiers(self):
        if "--" in self.args:
            return self.args[:self.args.index("--")]
        return self.args

    @property
    def exec_command(self):
        if "--" in self.args:
            return self.args[self.args.index("--"):]
        return ["--", "bash"]

    @property
    def command(self):
        return ["kubectl", self.kube_command, "-n", self.config.NAMESPACE, "-it", self.find_pod(), *self.exec_command]

    def handle(self):
        print(f"{' '.join(self.command)}")
        subprocess.call(self.command)
