from vmd.styles import NoOpStyle, CompositeStyle
from vmd.config.style_parser import StyleParser


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
        self.horizonal_rule = self.parse_style(config, 'horizonal_rule')
        self.code_block_margin = self.parse_style(config, 'code_block_margin')
        self.blockquote = self.parse_style(config, 'blockquote')
        self.blockquote_margin = self.parse_style(config, 'blockquote_margin')

        for key in config:
            raise Exception('Unknown setting in styles section: {}'.format(key))

    def parse_style(self, config, key, default=NoOpStyle()):
        if key not in config:
            return default

        style = config[key]
        del config[key]

        return self.style_parser.parse(style)

