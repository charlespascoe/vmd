import sys
import shutil
from styles import ClearStyle
from elements import Text
import re


class TextStyleWriter:
    def __init__(self, output):
        self.style_stack = []
        self.output = output

    def push_style(self, style):
        self.style_stack.append(style);
        style.apply(self.output)

    def pop_style(self):
        popped_style = self.style_stack.pop()
        ClearStyle().apply(self.output)
        self.apply_all_styles()
        return popped_style

    def apply_all_styles(self):
        for style in self.style_stack:
            style.apply(self.output)

    def write_text(self, text):
        if isinstance(text, str):
            self.output.write(text)
        elif isinstance(text, Text):
            if text.style is not None:
                self.push_style(text.style)

            for child in text.children:
                self.write_text(child)

            if text.style is not None:
                self.pop_style()
        else:
            raise Exception('Unknown type passed to TextStyleWriter.write_text: {}'.format(text.__class__.__name__))


class DisplayWriter(TextStyleWriter):
    def __init__(self, output, columns = None):
        super().__init__(output)

        if columns is None:
            columns, lines = shutil.get_terminal_size((80, 24))

        self.columns = columns

        self.chars_on_line = 0

        self.break_regex = re.compile(' ')

    def write_text(self, text):
        # This method override is only interested in actual strings
        # Let the super method walk the tree
        if not isinstance(text, str):
            super().write_text(text)
            return

        buf = ''

        for char in text:
            if char == '\n':
                self.output.write(buf)
                buf = ''
                self.new_line()
                continue

            buf += char

            if char.isprintable():
                self.chars_on_line += 1

            if self.chars_on_line > self.columns:
                break_index = self.get_break_index(buf)

                if break_index is None:
                    # If we can't find a break point, then just break where we are
                    # The last char is the char that went over the limit,
                    # so put it on the next line
                    self.output.write(buf[:-1])
                    self.new_line()
                    buf = char
                else:
                    self.output.write(buf[:break_index])
                    self.new_line()
                    buf = buf[break_index + 1:]

        self.output.write(buf)

    def get_break_index(self, text):
        break_match = self.break_regex.search(text[::-1])

        if break_match is None:
            return None
        else:
            return len(text) - break_match.start() - 1

    def new_line(self):
        self.output.write('\n')
        self.chars_on_line = 0
