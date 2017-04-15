class Style:
    def apply(self, output):
        raise NotImplemented()

    def write_escape_code(self, code, output):
        output.write('\x1b[{}m'.format(code))


class NoOpStyle(Style):
    def apply(self, output):
        pass


class ClearStyle(Style):
    def apply(self, output):
        self.write_escape_code('0', output)


class BoldStyle(Style):
    def apply(self, output):
        self.write_escape_code('1', output)


class ItalicStyle(Style):
    def apply(self, output):
        self.write_escape_code('3', output)


class ForegroundColourStyle(Style):
    def __init__(self, colour_code):
        self.colour_code = colour_code

    def apply(self, output):
        self.write_escape_code('38;5;{}'.format(self.colour_code), output)


class BackgroundColourStyle(Style):
    def __init__(self, colour_code):
        self.colour_code = colour_code

    def apply(self, output):
        self.write_escape_code('48;5;{}'.format(self.colour_code), output)


class UnderlineStyle(Style):
    def apply(self, output):
        self.write_escape_code('4', output)


class InverseStyle(Style):
    def apply(self, output):
        self.write_escape_code('7', output)


class FaintStyle(Style):
    def apply(self, output):
        self.write_escape_code('2', output)


class CompositeStyle(Style):
    def __init__(self, *styles):
        self.styles = styles

    def apply(self, output):
        for style in self.styles:
            if style is not None:
                style.apply(output)
