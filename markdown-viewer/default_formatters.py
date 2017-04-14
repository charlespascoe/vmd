from styles import *
from formatter import Formatter
from elements import *
import utils


class HeadingFormatter(Formatter):
    def __init__(self, config):
        self.config = config
        super().__init__()

    def format(self, renderer, elm, writer):
        writer.prefix = ''.ljust((elm.level - 1) * 2)
        writer.new_line()

        writer.push_style(self.config.styles.headings[elm.level - 1])
        super().format(renderer, elm, writer)
        writer.pop_style()

        writer.prefix = ''.ljust(elm.level * 2)
        writer.new_line()


class ParagraphFormatter(Formatter):
    def format(self, renderer, elm, writer):
        writer.new_line()

        writer.write_text('  ')

        super().format(renderer, elm, writer)

        writer.new_line()


class StrongFormatter(Formatter):
    def __init__(self):
        self.style = BoldStyle()


class EmphasisFormatter(Formatter):
    def __init__(self):
        self.style = ItalicStyle()


class InlineCodeFormatter(Formatter):
    def __init__(self):
        self.style = CompositeStyle(ClearStyle(), ForegroundColourStyle(196), BackgroundColourStyle(52))


class AppendLinkFormatter(Formatter):
    def __init__(self):
        self.style = ForegroundColourStyle(82)
        self.link_style = ForegroundColourStyle(240)

    def format(self, renderer, elm, writer):
        super().format(renderer, elm, writer)

        linkable = elm.find_linkable_ancestor()

        if linkable is not None:
            link_index = utils.to_superscript(linkable.next_link_index())

            writer.push_style(self.style)
            writer.write_text(link_index)
            writer.pop_style()

            linkable.add_child(Text('\n', Text(self.link_style, link_index, ' ', elm.path)))


class ListFormatter(Formatter):
    def format(self, renderer, elm, writer):
        writer.new_line()
        super().format(renderer, elm, writer)

        if elm.get_depth() == 0:
            writer.new_line()


class ListItemFormatter(Formatter):
    def __init__(self):
        self.bullet_style = ForegroundColourStyle(208)
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
    def format(self, renderer, elm, writer):
        max_index = elm.parent.prev_index

        index = str(elm.index).rjust(len(str(max_index)))

        self.format_list_item(renderer, elm, writer, ' {}. '.format(index))
