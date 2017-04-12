from styles import Style

class Text:
    def __init__(self, *args):
        args = list(args)

        if len(args) > 0 and isinstance(args[0], Style):
            self.style = args.pop(0)
        else:
            self.style = None

        self.children = args


class Strong(Text):
    pass


class Emphasis(Text):
    pass


class Paragraph(Text):
    pass


class Heading(Text):
    def __init__(self, level, *args):
        if not isinstance(level, int) or level < 1 or level > 6:
            raise Exception('Invalid Heading level: {}'.format(level))
        self.level = level
        super().__init__(*args)
