import json
from klube.config import settings


from klube.commands.base import BaseHandler


class Handler(BaseHandler):

    def handle(self):
        if len(self.args) == 0:
            # Display current configuration
            print(json.dumps(settings.get_config(), indent=2))

        elif len(self.args) == 1:
            # Display specific configuration key
            key = self.args[0].upper()
            value = settings[key]

            if value is not None:
                print(f"{key}: {value}")
            else:
                print(f"Configuration key '{key}' not set.")

        elif len(self.args) == 2:
            # Set configuration key-value pair
            key, value = self.args[0], self.args[1]
            settings[key] = value
            print(f"Set {key} to {value}")

        else:
            print("Usage: lube config [KEY] [VALUE]")
            print("  - No arguments: Display all configuration")
            print("  - One argument: Display specific configuration key")
            print("  - Two arguments: Set configuration key-value pair")
