from markdown import markdown
from elements import *
from html.parser import HTMLParser
import re


class Parser:
    def parse(self, md):
        builder = TreeBuilder()
        html = markdown(md)
        print(html)
        builder.feed(html)
        return builder.document


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.document = Document()
        self.current_element = self.document
        self.heading_regex = re.compile('^h(1|2|3|4|5|6)$')

    def handle_starttag(self, tag, attrs):
        heading_match = self.heading_regex.search(tag)

        if heading_match:
            self.new_element(Heading(int(heading_match.group(1))))
        elif tag == 'p':
            self.new_element(Paragraph())
        elif tag == 'strong':
            self.new_element(Strong())
        elif tag == 'em':
            self.new_element(Emphasis())
        else:
            raise Exception('Unhandled tag type: ' + tag)


    def new_element(self, elm):
        self.current_element.add_child(elm)
        self.current_element = elm

    def handle_endtag(self, tag):
        if tag == 'br':
            return

        self.current_element = self.current_element.parent

    def handle_data(self, data):
        if data != '\n':
            self.current_element.add_child(data)
