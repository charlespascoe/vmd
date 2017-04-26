from vmd.styles import Style

class Element:
    def __init__(self, *args):
        args = list(args)

        if len(args) > 0 and isinstance(args[0], Style):
            self.style = args.pop(0)
        else:
            self.style = None

        self.children = args
        self.parent = None
        self.tag = '<Unknown>'

    def add_child(self, child):
        self.children.append(child)

        if isinstance(child, Element):
            child.parent = self

    def find_ancestor(self, element_type):
        if self.parent is None or isinstance(self.parent, element_type):
            return self.parent

        return self.parent.find_ancestor(element_type)

    def tag_ancestry(self):
        ancestor_tags = ''

        if self.parent is not None:
            ancestor_tags = self.parent.tag_ancestry() + ' > '

        return ancestor_tags + self.tag


class Text(Element):
    pass


class Strong(Text):
    pass


class Emphasis(Text):
    pass


class Linkable(Text):
    def __init__(self, *args):
        self.prev_link_index = 0
        super().__init__(*args)

    def next_link_index(self):
        self.prev_link_index += 1
        return self.prev_link_index


class Paragraph(Linkable):
    pass

class Heading(Text):
    def __init__(self, level, *args):
        if not isinstance(level, int) or level < 1 or level > 6:
            raise Exception('Invalid Heading level: {}'.format(level))
        self.level = level
        self.prev_subheading_index = 0
        self.index = '0'
        super().__init__(*args)

    def next_subheading_index(self):
        self.prev_subheading_index += 1
        return '{}.{}'.format(self.index, self.prev_subheading_index)


class InlineCode(Text):
    pass


class CodeBlock(Text):
    def lines(self):
        text = ''.join((text for text in self.children if isinstance(text, str)))

        return text.rstrip().split('\n')


class Link(Text):
    def __init__(self, path, *args):
        self.path = path
        super().__init__(*args)

    def find_linkable_ancestor(self):
        return self.find_ancestor(Linkable)


class List(Element):
    def get_depth(self):
        if isinstance(self.parent, ListItem):
            return self.parent.get_depth() + 1
        else:
            return 0

    def add_child(self, child):
        if not isinstance(child, ListItem):
            raise Exception('child must be a ListItem')

        super().add_child(child)


class Blockquote(Text):
    pass


class ListItem(Linkable):
    def get_depth(self):
        return self.parent.get_depth()

    @property
    def is_last(self):
        return self.parent.children[-1] == self


class OrderedList(List):
    def __init__(self, *args):
        self.prev_index = 0
        super().__init__(*args)

    def add_child(self, child):
        super().add_child(child)

        self.prev_index += 1

        child.index = self.prev_index


class OrderedListItem(ListItem):
    def __init__(self, *args):
        self.index = 1
        super().__init__(*args)


class HorizontalRule: # Not element - it cannot have children
    def __init__(self):
        self.tag = 'hr'


class Document(Element):
    def __init__(self, *args):
        super().__init__(*args)
        self.headings = []
        self.prev_heading_index = 0
        self.tag = 'document'

    def add_heading(self, new_heading):
        for heading in reversed(self.headings):
            if heading.level < new_heading.level:
                new_heading.index = heading.next_subheading_index()
                break
        else:
            self.prev_heading_index += 1
            new_heading.index = str(self.prev_heading_index)

        self.headings.append(new_heading)
