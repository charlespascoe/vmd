import re
import os
from styles import *


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


class StylesConfig:
    def __init__(self, config={}):
        self.style_parser = StyleParser()

        self.heading_base = self.parse_style(config, 'heading_base')
        self.headings = [
            CompositeStyle(self.heading_base, self.parse_style(config, 'heading1')),
            CompositeStyle(self.heading_base, self.parse_style(config, 'heading2')),
            CompositeStyle(self.heading_base, self.parse_style(config, 'heading3')),
            CompositeStyle(self.heading_base, self.parse_style(config, 'heading4')),
            CompositeStyle(self.heading_base, self.parse_style(config, 'heading5')),
            CompositeStyle(self.heading_base, self.parse_style(config, 'heading6'))
        ]

        self.heading_index_base = self.parse_style(config, 'heading_index_base')

        self.heading_index = [
            CompositeStyle(self.headings[0], self.heading_index_base, self.parse_style(config, 'heading1_index')),
            CompositeStyle(self.headings[1], self.heading_index_base, self.parse_style(config, 'heading2_index')),
            CompositeStyle(self.headings[2], self.heading_index_base, self.parse_style(config, 'heading3_index')),
            CompositeStyle(self.headings[3], self.heading_index_base, self.parse_style(config, 'heading4_index')),
            CompositeStyle(self.headings[4], self.heading_index_base, self.parse_style(config, 'heading5_index')),
            CompositeStyle(self.headings[5], self.heading_index_base, self.parse_style(config, 'heading6_index')),
        ]

        self.strong = self.parse_style(config, 'strong')
        self.emphasis = self.parse_style(config, 'emphasis')
        self.inline_code = self.parse_style(config, 'inline_code')
        self.link = self.parse_style(config, 'link')
        self.link_index = self.parse_style(config, 'link_index')
        self.link_hint = self.parse_style(config, 'link_hint')
        self.list_bullet = self.parse_style(config, 'list_bullet')
        self.list_number = CompositeStyle(self.list_bullet, self.parse_style(config, 'list_number'))
        self.paragraph = self.parse_style(config, 'paragraph')

        for key in config:
            raise Exception('Unknown setting in styles section: {}'.format(key))

    def parse_style(self, config, key, default=NoOpStyle()):
        if key not in config:
            return default

        style = config[key]
        del config[key]

        return self.style_parser.parse(style)


class StyleParser:
    def __init__(self):
        self.simple_styles = {
            'clear': ClearStyle(),
            'bold': BoldStyle(),
            'italic': ItalicStyle(),
            'underline': UnderlineStyle(),
            'inverse': InverseStyle(),
            'faint': FaintStyle()
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
                    raise Exception('Unknown style identifier: "{}"'.format(style_str))

                if colour_match.group(1) == 'f':
                    styles.append(ForegroundColourStyle(int(colour_match.group(2))))
                else:
                    styles.append(BackgroundColourStyle(int(colour_match.group(2))))

        if len(styles) == 0:
            return CompositeStyle()

        if len(styles) == 1:
            return styles[0]

        return CompositeStyle(*styles)


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


class FormattingConfig:
    def __init__(self, config={}):
        self.indent_paragraph_first_line = parse_boolean(config, 'indent_paragraph_first_line', True)
        self.heading_indent_limit = parse_int(config, 'heading_indent_limit', 6)
        self.align_content_with_headings = parse_boolean(config, 'align_content_with_headings', True)

        for key in config:
            raise Exception('Unknown setting in formatting section: {}'.format(key))
