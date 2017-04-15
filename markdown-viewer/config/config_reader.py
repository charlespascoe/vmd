import re
import os

class ConfigReader:
    def __init__(self, conf_file, config={}):
        self.conf_file = conf_file
        self.comment_regex = re.compile('^([^#]*)#?')
        self.group_header_regex = re.compile('^\[([a-z_]+)\]$')
        self.entry_regex = re.compile('^(\s|\t)*([a-z0-9_]+)(\s|\t)*=(.*)$')
        self.config = config

    def read_line(self):
        line = self.conf_file.readline()

        while line == '\n':
            line = self.conf_file.readline()

        if line == '':
            return None

        return self.comment_regex.search(line).group(1).strip()

    def read_config(self):
        line = self.read_line()
        current_group = None

        while line is not None:
            entry_match = self.entry_regex.search(line)

            if entry_match is not None:
                if current_group is None:
                    raise Exception('Unexpected line in config: {}'.format(line))

                self.config[current_group][entry_match.group(2)] = entry_match.group(4).strip()

                line = self.read_line()
                continue

            group_header_match = self.group_header_regex.search(line)

            if group_header_match is not None:
                current_group = group_header_match.group(1)

                if current_group not in self.config:
                    self.config[current_group] = {}

                line = self.read_line()
                continue

            raise Exception('Unparsable line in config: {}'.format(line))

        return self.config


def parse_boolean(config, key, default=False):
    if key not in config:
        return default

    val = config[key]

    del config[key]

    if val.lower() == 'true':
        return True
    elif val.lower() == 'false':
        return False
    else:
        raise Exception('Failed to parse boolean expression: {}'.format(val))


def parse_int(config, key, default=0):
    if key not in config:
        return default

    val = config[key]

    del config[key]

    try:
        return int(val)
    except:
        raise Exception('Failed to parse boolean expression: {}'.format(val))
