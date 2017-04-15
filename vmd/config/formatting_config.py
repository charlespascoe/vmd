from config import config_reader

class FormattingConfig:
    def __init__(self, config={}):
        self.indent_paragraph_first_line = config_reader.parse_boolean(config, 'indent_paragraph_first_line', True)
        self.heading_indent_limit = config_reader.parse_int(config, 'heading_indent_limit', 6)
        self.align_content_with_headings = config_reader.parse_boolean(config, 'align_content_with_headings', True)

        for key in config:
            raise Exception('Unknown setting in formatting section: {}'.format(key))
