class Formatter:
    def __init__(self):
        self.style = None

    def format(self, renderer, elm, writer):
        if self.style is not None:
            writer.push_style(self.style)

        for child in elm.children:
            renderer.render(child)

        if self.style is not None:
            writer.pop_style()

