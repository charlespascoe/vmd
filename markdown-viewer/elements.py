from styles import Style

class Element:
    def __init__(self, *args):
        args = list(args)

        if len(args) > 0 and isinstance(args[0], Style):
            self.style = args.pop(0)
        else:
            self.style = None

        self.children = args
        self.parent = None

    def add_child(self, child):
        self.children.append(child)

        if isinstance(child, Element):
            child.parent = self

    def find_ancestor(self, element_type):
        if self.parent is None or isinstance(self.parent, element_type):
            return self.parent

        return self.parent.find_ancestor(element_type)


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
        super().__init__(*args)


class InlineCode(Text):
    pass


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


class Document(Element):
    pass
