import re
import os
from styles import *


class Config:
    def __init__(self, path):
        self.path = path

    def load(self):
        path = os.path.abspath(os.path.expanduser(self.path))

        if not os.path.isfile(path):
            self.formatting_config = FormattingConfig()
            self.style_config = StyleConfig()
            return

        with open(path) as f:
            reader = ConfigReader(f)
            config = reader.read_config()

        if 'formatting' in config:
            self.formatting_config = FormattingConfig(config['formatting'])
        else:
            self.formatting_config = FormattingConfig()

        if 'styles' in config:
            self.style_config = StyleConfig(config['styles'])
        else:
            self.style_config = StyleConfig()


class ConfigReader:
    def __init__(self, conf_file):
        self.conf_file = conf_file
        self.comment_regex = re.compile('^([^#]*)#?')
        self.group_header_regex = re.compile('^\[([a-z_]+)\]$')
        self.entry_regex = re.compile('^(\s|\t)*([a-z0-9_]+)(\s|\t)*=(.*)$')

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
        config = {}

        while line is not None:
            entry_match = self.entry_regex.search(line)

            if entry_match is not None:
                if current_group is None:
                    raise Exception('Unexpected line in config: {}'.format(line))

                config[current_group][entry_match.group(2)] = entry_match.group(4).strip()

                line = self.read_line()
                continue

            group_header_match = self.group_header_regex.search(line)

            if group_header_match is not None:
                current_group = group_header_match.group(1)

                if current_group in config:
                    raise Exception('Group defined twice: {}'.format(current_group))

                config[current_group] = {}

                line = self.read_line()
                continue

            raise Exception('Unparsable line in config: {}'.format(line))

        return config


class StyleConfig:
    def __init__(self, config={}):
        self.config = config

        self.style_parser = StyleParser()

        self.heading_base = self.parse_style('heading_base', CompositeStyle(ClearStyle(), BoldStyle(), ForegroundColourStyle(208)))
        self.headings = [
            CompositeStyle(self.heading_base, self.parse_style('heading1')),
            CompositeStyle(self.heading_base, self.parse_style('heading2')),
            CompositeStyle(self.heading_base, self.parse_style('heading3')),
            CompositeStyle(self.heading_base, self.parse_style('heading4')),
            CompositeStyle(self.heading_base, self.parse_style('heading5')),
            CompositeStyle(self.heading_base, self.parse_style('heading6'))
        ]

    def parse_style(self, key, default=None):
        if key not in self.config:
            return default

        style = self.config[key]
        del self.config[key]

        return self.style_parser.parse(style)


class StyleParser:
    def __init__(self):
        self.simple_styles = {
            'clear': ClearStyle(),
            'bold': BoldStyle(),
            'italic': ItalicStyle()
        }

        self.colour_style_regex = re.compile('^(f|b)gcolour\((\d{1,3})\)$')

    def parse(self, styles_str):
        styles = []

        for style_str in styles_str.split(','):
            style_str = style_str.lower().strip()

            if style_str in self.simple_styles:
                styles.append(self.simple_styles[style_str])
            else:
                colour_match = self.colour_style_regex.search(style_str)

                if colour_match is None:
                    raise Exception('Unknown style identifier: "{}" (for {})'.format(style_str, key))

                if colour_match.group(1) == 'f':
                    styles.append(ForegroundColourStyle(int(colour_match.group(2))))
                else:
                    styles.append(BackgroundColourStyle(int(colour_match.group(2))))

        if len(styles) == 0:
            return CompositeStyle()

        if len(styles) == 1:
            return styles[0]

        return CompositeStyle(*styles)


class FormattingConfig:
    def __init__(self, formatting_config={}):
        pass
