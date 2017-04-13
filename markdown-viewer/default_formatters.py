from styles import *
from formatter import Formatter
from elements import *
import utils


class HeadingFormatter(Formatter):
    def __init__(self):
        self.style = CompositeStyle(
            ClearStyle(),
            BoldStyle(),
            ForegroundColourStyle(208)
        )

    def format(self, renderer, elm, writer):
        writer.prefix = ''.ljust((elm.level - 1) * 2)
        writer.new_line()

        super().format(renderer, elm, writer)

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

        para = elm.find_ancestor(Paragraph)

        link_index = utils.to_superscript(para.next_link_index())

        writer.push_style(self.style)
        writer.write_text(link_index)
        writer.pop_style()

        para.add_child(Text('\n', Text(self.link_style, link_index, ' ', elm.path)))
