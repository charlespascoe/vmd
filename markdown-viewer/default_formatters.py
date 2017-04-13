from styles import *
from formatter import Formatter


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
