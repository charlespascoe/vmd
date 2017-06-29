from vmd.config import config_reader

class FormattingConfig:
    def __init__(self, config={}):
        self.indent_paragraph_first_line = config_reader.parse_boolean(config, 'indent_paragraph_first_line', False)
        self.heading_indent_limit = config_reader.parse_int(config, 'heading_indent_limit', 0)
        self.align_content_with_headings = config_reader.parse_boolean(config, 'align_content_with_headings', False)
        self.blockquote_quote_marks = config_reader.parse_boolean(config, 'blockquote_quote_marks', False)

        for key in config:
            raise Exception('Unknown setting in formatting section: {}'.format(key))
