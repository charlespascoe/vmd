from markdown import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
from vmd.elements import *
from html.parser import HTMLParser
import re
import logging


class Parser:
    def __init__(self, tab_spaces):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.tab_spaces = tab_spaces

    def parse(self, md):
        builder = TreeBuilder()
        html = markdown(
            md,
            tab_length=self.tab_spaces,
            extensions=[FencedCodeExtension()]
        )
        self.logger.debug('HTML:\n\n%s\n\nEND HTML', html)
        builder.feed(html)
        return builder.document


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.document = Document()
        self.current_element = self.document
        self.heading_regex = re.compile('^h(1|2|3|4|5|6)$')

        self.unknown_tag_stack = []

        self.logger = logging.getLogger(self.__class__.__name__)

    def get_attr(self, attrs, find_key, default=None):
        for key, value in attrs:
            if key == find_key:
                return value

        return default

    def handle_starttag(self, tag, attrs):
        if len(self.unknown_tag_stack) > 0:
            self.unknown_tag_stack.append(tag)
            return

        heading_match = self.heading_regex.search(tag)

        if heading_match:
            heading = Heading(int(heading_match.group(1)))
            self.new_element(tag, heading)
            self.document.add_heading(heading)
        elif tag == 'p':
            if not isinstance(self.current_element, Blockquote):
                self.new_element(tag, Paragraph())
        elif tag == 'strong':
            self.new_element(tag, Strong())
        elif tag == 'em':
            self.new_element(tag, Emphasis())
        elif tag == 'pre':
            self.new_element(tag, CodeBlock())
        elif tag == 'code':
            if not isinstance(self.current_element, CodeBlock):
                self.new_element(tag, InlineCode())
        elif tag == 'a':
            self.new_element(tag, Link(self.get_attr(attrs, 'href', '[No Link]')))
        elif tag == 'ul':
            self.new_element(tag, List())
        elif tag == 'ol':
            self.new_element(tag, OrderedList())
        elif tag == 'li':
            if isinstance(self.current_element, OrderedList):
                self.new_element(tag, OrderedListItem())
            elif isinstance(self.current_element, List):
                self.new_element(tag, ListItem())
            else:
                self.logger.warning('Unexpected list item found in %s', self.current_element.tag_ancestry())
        elif tag == 'hr':
            self.current_element.add_child(HorizontalRule())
        elif tag == 'blockquote':
            self.new_element(tag, Blockquote())
        else:
            self.logger.warning('Unhandled tag type \'%s\' found in %s', tag, self.current_element.tag_ancestry())
            self.unknown_tag_stack.append(tag)


    def new_element(self, tag, elm):
        elm.tag = tag
        self.current_element.add_child(elm)
        self.current_element = elm

    def handle_endtag(self, tag):
        if len(self.unknown_tag_stack) > 0 and self.unknown_tag_stack[-1] == tag:
            self.unknown_tag_stack.pop(-1)
            return

        if tag == self.current_element.tag:
            self.current_element = self.current_element.parent

    def handle_data(self, data):
        if data != '\n' and len(self.unknown_tag_stack) == 0:
            self.current_element.add_child(data)
