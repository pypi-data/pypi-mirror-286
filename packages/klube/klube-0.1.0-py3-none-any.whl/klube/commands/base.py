from abc import ABC, abstractmethod
import subprocess
from typing import Optional


class BaseHandler(ABC):
    kube_command = ""

    def __init__(self, *args, config):
        self.args = args[0]
        self.config = config

    @abstractmethod
    def handle(self):
        ...

    @property
    def identifiers(self):
        return self.args

    @property
    def command(self):
        return ["kubectl", self.kube_command, "-n", self.config.NAMESPACE, self.find_pod()]

    def find_pod(self) -> Optional[str]:
        command = ["kubectl", "get", "pods", "-n", self.config.NAMESPACE, "-o", "name"]
        all_pods = subprocess.check_output(command).decode("utf-8").splitlines()
        all_pods = [pod.replace("pod/", "") for pod in all_pods]

        for pod in all_pods:
            matches_all = True
            for identifier in self.identifiers:
                if identifier.lower() not in pod.lower():
                    matches_all = False
                    break
            if matches_all:
                return pod
