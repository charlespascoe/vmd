class Renderer:
    def __init__(self, writer):
        self.formatters = {}
        self.writer = writer

    def render_document(self, doc):
        for child in doc.children:
            self.render(child)

    def render(self, elm):
        formatter = self.get_formatter(elm.__class__.__name__)

        if formatter is not None:
            formatter.format(self, elm, self.writer)
        else:
            self.writer.write_text(elm)

    def get_formatter(self, elm_type):
        if elm_type in self.formatters:
            if isinstance(self.formatters[elm_type], str):
                return self.get_formatter(self.formatters[elm_type])
            else:
                return self.formatters[elm_type]
        else:
            return None
