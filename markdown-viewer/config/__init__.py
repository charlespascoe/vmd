import re
import os
from styles import *
from config.config_reader import ConfigReader
from config.styles_config import StylesConfig
from config.formatting_config import FormattingConfig


class Config:
    def __init__(self, paths):
        self.paths = paths

        self.config_classes = {
            'styles': StylesConfig,
            'formatting': FormattingConfig
        }

        self.config = {}

    def load(self):
        for path in self.paths:
            path = os.path.abspath(os.path.expanduser(path))

            try:
                with open(path) as f:
                    reader = ConfigReader(f, self.config)
                    self.config = reader.read_config()
            except FileNotFoundError:
                pass # Just ignore non-existent files

        for key, config_class in self.config_classes.items():
            if key in self.config:
                self.config[key] = config_class(self.config[key])
            else:
                self.config[key] = config_class()

    def __getattr__(self, name):
        return self.config[name]
