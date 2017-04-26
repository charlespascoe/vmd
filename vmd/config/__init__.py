import re
import os
from vmd.styles import *
from vmd.config.config_reader import ConfigReader
from vmd.config.styles_config import StylesConfig
from vmd.config.formatting_config import FormattingConfig
import logging


class Config:
    def __init__(self, paths):
        self.paths = paths

        self.config_classes = {
            'styles': StylesConfig,
            'formatting': FormattingConfig
        }

        self.config = {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def load(self):
        config = {}

        for path in self.paths:
            path = os.path.abspath(os.path.expanduser(path))

            self.logger.info('Attempting to load config file: %s', path)

            try:
                with open(path) as f:
                    reader = ConfigReader(f, config)
                    config = reader.read_config()
            except FileNotFoundError:
                self.logger.info('Config file not found: %s', path)

        for key, config_class in self.config_classes.items():
            if key in config:
                self.logger.debug('Loading config for %s', key)
                self.config[key] = config_class(config[key])
            else:
                self.logger.debug('Loading default config for %s', key)
                self.config[key] = config_class()


    def __getattr__(self, name):
        return self.config[name]
