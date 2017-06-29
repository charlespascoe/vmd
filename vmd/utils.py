from vmd.elements import Text

def get_printable_length(text):
    if isinstance(text, str):
        return sum((char.isprintable() for char in text))

    if isinstance(text, Text):
        return sum((get_printable_length(child) for child in text.children))

    raise Exception('Unknown text type: {}'.format(text.__class__.__name__))

def to_superscript(number):
    supers = '⁰¹²³⁴⁵⁶⁷⁸⁹'
    return ''.join((supers[int(d)] for d in str(number)))
