import json
from pathlib import Path


class Config:
    CONFIG_DIR = Path.home() / '.lube'
    CONFIG_FILE = CONFIG_DIR / 'config.json'

    def __init__(self):
        self._config = self.get_config()

    def __getitem__(self, item: str):
        config = self.get_config()
        return config.get(item.upper(), None)

    def __setitem__(self, key, value):
        config = self.get_config()
        config[key.upper()] = value
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

    def get_config(self):
        self._ensure_config_file()
        with open(self.CONFIG_FILE, 'r') as f:
            return json.load(f)

    def _ensure_config_file(self):
        if not self.CONFIG_DIR.exists():
            self.CONFIG_DIR.mkdir(parents=True)
        if not self.CONFIG_FILE.exists():
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump({'NAMESPACE': 'default'}, f, indent=2)


settings = Config()
