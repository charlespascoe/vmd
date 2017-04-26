import re
from vmd.styles import *


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
            return NoOpStyle()

        if len(styles) == 1:
            return styles[0]

        return CompositeStyle(*styles)
