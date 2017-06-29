import re
import os

class ConfigReader:
    def __init__(self, conf_file, config={}):
        self.conf_file = conf_file
        self.comment_regex = re.compile('^([^#]*)#?')
        self.group_header_regex = re.compile('^\[([a-z_]+)\]$')
        self.entry_regex = re.compile('^(\s|\t)*([a-z0-9_]+)(\s|\t)*=(.*)$')
        self.config = config
        self.no_group = {}

    def read_line(self):
        while True:
            line = self.conf_file.readline()

            if line != '\n':
                break

        if line == '':
            return None

        line = self.comment_regex.search(line).group(1).strip()

        if line == '':
            return self.read_line()

        return line

    def read_config(self):
        line = self.read_line()
        current_group = self.no_group

        while line is not None:
            entry_match = self.entry_regex.search(line)

            if entry_match is not None:
                current_group[entry_match.group(2)] = entry_match.group(4).strip()

                line = self.read_line()
                continue

            group_header_match = self.group_header_regex.search(line)

            if group_header_match is not None:
                group_key = group_header_match.group(1)

                if group_key not in self.config:
                    self.config[group_key] = {}

                current_group = self.config[group_key]

                line = self.read_line()
                continue

            raise Exception('Unparsable line in config: "{}"'.format(line))

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
