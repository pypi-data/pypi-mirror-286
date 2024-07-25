import subprocess

from klube.commands.base import BaseHandler
import pathlib


class Handler(BaseHandler):
    kube_command = "cp"

    def handle(self):
        handler = FromPodHandler
        if ":" in self.args[-1] and any(["/" in arg or "." in arg for arg in self.args[:-1]]):
            handler = ToPodHandler

        handler(self.args, config=self.config).handle()


class ToPodHandler(Handler):

    @property
    def destination(self):
        destination = pathlib.Path(self.args[-1].split(":")[1])
        if "." not in destination.name:
            return str(destination / pathlib.Path(self.source).name)
        return str(destination)

    @property
    def source(self):
        source = pathlib.Path(self.args[0])
        return str(source.resolve())

    @property
    def identifiers(self):
        identifiers = self.args[1:-1]
        last_identifier = self.args[-1].split(":")[0]
        if last_identifier:
            identifiers.append(last_identifier)
        return identifiers

    @property
    def command(self):
        return ["kubectl", self.kube_command, "-n", self.config.NAMESPACE, self.source, f"{self.find_pod()}:{self.destination}"]

    def handle(self):
        print(f"{' '.join(self.command)}")
        subprocess.call(self.command)


class FromPodHandler(Handler):

    @property
    def destination_specified(self):
        return any(["/" in arg for arg in self.args[:-1]])

    @property
    def destination(self):
        if self.destination_specified and self.args[-1] != ".":
            destination = pathlib.Path(self.args[-1])
        else:
            destination = (pathlib.Path("") / pathlib.Path(self.source).name).resolve()

        if "." not in pathlib.Path(destination).name:
            return destination / pathlib.Path(self.source).name
        return destination

    @property
    def source(self):
        if self.destination_specified:
            return self.args[-2].split(":")[1]
        return self.args[-1].split(":")[1]

    @property
    def identifiers(self):
        identifiers = self.args[:-2]
        last_identifier = self.args[-2].split(":")[0]
        if last_identifier:
            identifiers.append(last_identifier)
        return identifiers

    @property
    def command(self):
        return ["kubectl", self.kube_command, "-n", self.config.NAMESPACE, f"{self.find_pod()}:{self.source}", f"{self.destination}"]

    def handle(self):
        print(f"{' '.join(self.command)}")
        subprocess.call(self.command)
