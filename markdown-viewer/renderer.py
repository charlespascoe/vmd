class Renderer:
    def __init__(self, writer):
        self.formatters = {}
        self.writer = writer

    def render_document(self, doc):
        for child in doc.children:
            self.render(child)

    def render(self, elm):
        elm_type = elm.__class__.__name__

        if elm_type in self.formatters:
            self.formatters[elm_type].format(self, elm, self.writer)
        else:
            self.writer.write_text(elm)
