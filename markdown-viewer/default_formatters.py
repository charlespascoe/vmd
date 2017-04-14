from styles import *
from formatter import Formatter
from elements import *
import utils


class HeadingFormatter(Formatter):
    def __init__(self, config):
        self.config = config
        super().__init__()

    def format(self, renderer, elm, writer):
        indent = min(elm.level - 1, self.config.formatting.heading_indent_limit) * 2

        writer.prefix = ''.ljust(indent + 1)
        writer.new_line()

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
        self.format_list_item(renderer, elm, writer, ' • ')

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

        index = str(elm.index).rjust(len(str(max_index)))

        self.format_list_item(renderer, elm, writer, ' {}. '.format(index))
