# PYTHON_ARGCOMPLETE_OK
import sys
import argparse


VERSION = '0.0.0'


def build_parser(args):
    from vmd.parser import Parser

    return Parser(args.tab_spaces)


def create_display_writer(output):
    from vmd.writer import DisplayWriter

    return DisplayWriter(output)


def load_config():
    from vmd.config import Config
    import re
    import os

    themes_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'themes')

    theme = os.path.join(themes_directory, 'default')

    if 'VMD_THEME' in os.environ:
        if re.search('^[a-zA-Z_\-0-9]+$', os.environ['VMD_THEME']):
            theme = os.path.join(themes_directory, os.environ['VMD_THEME'])
        else:
            theme = os.environ['VMD_THEME']

    config = Config([theme, '~/.vmdrc'])

    config.load()

    return config


def build_render(writer, config):
    from vmd.renderer import Renderer
    import vmd.default_formatters

    renderer = Renderer(writer)
    renderer.formatters['Paragraph'] = vmd.default_formatters.ParagraphFormatter(config)
    renderer.formatters['Heading'] = vmd.default_formatters.HeadingFormatter(config)
    renderer.formatters['Strong'] = vmd.default_formatters.StrongFormatter(config)
    renderer.formatters['Emphasis'] = vmd.default_formatters.EmphasisFormatter(config)
    renderer.formatters['InlineCode'] = vmd.default_formatters.InlineCodeFormatter(config)
    renderer.formatters['Link'] = vmd.default_formatters.AppendLinkFormatter(config)
    renderer.formatters['List'] = vmd.default_formatters.ListFormatter()
    renderer.formatters['ListItem'] = vmd.default_formatters.ListItemFormatter(config)
    renderer.formatters['OrderedList'] = 'List'
    renderer.formatters['OrderedListItem'] = vmd.default_formatters.OrderedListItemFormatter(config)
    renderer.formatters['HorizontalRule'] = vmd.default_formatters.HorizontalRuleFormatter(config)
    renderer.formatters['CodeBlock'] = vmd.default_formatters.CodeBlockFormatter(config)
    renderer.formatters['Blockquote'] = vmd.default_formatters.BlockquoteFormatter(config)

    return renderer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='count', default=0, dest='verbosity')
    parser.add_argument('-V', '--version', action='store_true', dest='version', help='Show version and exit')

    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument('file', nargs='?', metavar='FILE', help='The path to the markdown file')
    input_group.add_argument('--stdin', dest='stdin', action='store_true', help='Read Markdown from stdin')

    parser.add_argument('-t', '--tab-spaces', dest='tab_spaces', default=4, type=int, help='Number of spaces in a tab (defaults to 4)')

    try:
        import argcomplete
        argcomplete.autocomplete(parser)
    except Exception:
        pass # Optional argcomplete module not installed

    args = parser.parse_args()

    if args.version:
        print('vmd {}'.format(VERSION))
        sys.exit(0)

    import logging

    if args.verbosity != 0:
        logging_level = 10 * max(0, 3 - args.verbosity)

        logging.basicConfig(level=logging_level)

    mdparser = build_parser(args)

    config = load_config()

    writer = create_display_writer(sys.stdout)

    renderer = build_render(writer, config)

    if args.stdin:
        doc = mdparser.parse(sys.stdin.read())
    elif args.file is not None:
        with open(args.file) as f:
            doc = mdparser.parse(f.read())
    else:
        parser.print_help()
        sys.exit(1)

    renderer.render_document(doc)

    sys.stdout.write('\n')
    sys.stdout.flush()
    sys.stdout.close()

if __name__ == '__main__':
    main()
