from vmd.styles import *
from vmd.formatter import Formatter
from vmd.elements import *
import vmd.utils as utils


class HeadingFormatter(Formatter):
    def __init__(self, config):
        self.config = config
        super().__init__()

    def format(self, renderer, elm, writer):
        indent = min(elm.level - 1, self.config.formatting.heading_indent_limit) * 2

        writer.prefix = ''.ljust(indent + 1)
        writer.new_line()

        writer.push_style(self.config.styles.heading_index[elm.level - 1])
        writer.write_text(elm.index)
        writer.pop_style()
        writer.write_text(' ')
        writer.push_style(self.config.styles.headings[elm.level - 1])
        super().format(renderer, elm, writer)
        writer.pop_style()

        if self.config.formatting.align_content_with_headings:
            writer.prefix = ''.ljust(indent + 3)
        else:
            writer.prefix = ' '

        writer.new_line()


class ParagraphFormatter(Formatter):
    def __init__(self, config):
        self.style = config.styles.paragraph
        self.indent = config.formatting.indent_paragraph_first_line

    def format(self, renderer, elm, writer):
        writer.new_line()

        if self.indent:
            writer.write_text('  ')

        super().format(renderer, elm, writer)

        writer.new_line()


class StrongFormatter(Formatter):
    def __init__(self, config):
        self.style = config.styles.strong


class EmphasisFormatter(Formatter):
    def __init__(self, config):
        self.style = config.styles.emphasis


class InlineCodeFormatter(Formatter):
    def __init__(self, config):
        self.style = config.styles.inline_code


class CodeBlockFormatter(Formatter):
    def __init__(self, config):
        self.margin_style = config.styles.code_block_margin
        super().__init__()

    def format(self, renderer, elm, writer):
        prefix = writer.prefix

        lines = elm.lines()

        line_pos_width = max(len(str(len(lines))), 2)

        for line_pos, line in enumerate(elm.lines()):
            writer.new_line()
            writer.write_text(Text(self.margin_style, ' {} ┃ '.format(str(line_pos + 1).rjust(line_pos_width))))
            writer.prefix = Text(self.margin_style, prefix, ' {} ┃ '.format(''.rjust(line_pos_width)))
            writer.write_text(line)
            writer.prefix = prefix

        writer.new_line()


class AppendLinkFormatter(Formatter):
    def __init__(self, config):
        self.style = config.styles.link
        self.link_index_style = config.styles.link_index
        self.link_hint_style = config.styles.link_hint

    def format(self, renderer, elm, writer):
        super().format(renderer, elm, writer)

        linkable = elm.find_linkable_ancestor()

        if linkable is not None:
            link_index = utils.to_superscript(linkable.next_link_index())

            writer.push_style(self.link_index_style)
            writer.write_text(link_index)
            writer.pop_style()

            linkable.add_child(Text('\n', Text(self.link_hint_style, link_index, ' ', elm.path)))


class ListFormatter(Formatter):
    def format(self, renderer, elm, writer):
        writer.new_line()
        super().format(renderer, elm, writer)

        if elm.get_depth() == 0:
            writer.new_line()


class ListItemFormatter(Formatter):
    def __init__(self, config):
        self.bullet_style = config.styles.list_bullet
        super().__init__()

    def format(self, renderer, elm, writer):
        self.format_list_item(renderer, elm, writer, '  • ')

    def format_list_item(self, renderer, elm, writer, bullet):
        prev_prefix = writer.prefix
        writer.prefix = Text(writer.prefix, ''.ljust(len(bullet)))
        writer.write_text(Text(self.bullet_style, bullet))

        super().format(renderer, elm, writer)

        writer.prefix = prev_prefix

        if not elm.is_last:
            writer.new_line()


class OrderedListItemFormatter(ListItemFormatter):
    def __init__(self, config):
        super().__init__(config)
        self.bullet_style = config.styles.list_number

    def format(self, renderer, elm, writer):
        max_index = elm.parent.prev_index

        index = str(elm.index).rjust(max(len(str(max_index)), 2))

        self.format_list_item(renderer, elm, writer, ' {}. '.format(index))


class HorizontalRuleFormatter(Formatter):
    def __init__(self, config):
        self.style = config.styles.horizonal_rule

    def format(self, renderer, elm, writer):
        prev_prefix = writer.prefix
        writer.prefix = ''
        writer.new_line()

        writer.push_style(self.style)
        writer.write_text(' ' + ''.ljust(writer.columns - 2, '━') + ' ')
        writer.pop_style()

        writer.prefix = prev_prefix
        writer.new_line()


class BlockquoteFormatter(Formatter):
    def __init__(self, config):
        super().__init__()
        self.style = config.styles.blockquote
        self.margin_style = config.styles.blockquote_margin
        self.use_quotes = config.formatting.blockquote_quote_marks

    def format(self, renderer, elm, writer):
        prev_prefix = writer.prefix

        writer.prefix = Text(prev_prefix, Text(self.margin_style, '┃ '))
        writer.new_line()

        if self.use_quotes:
            writer.write_text(Text(self.style, '"'))

        super().format(renderer, elm, writer)

        if self.use_quotes:
            writer.write_text(Text(self.style, '"'))

        writer.prefix = prev_prefix
        writer.new_line()
