#!/usr/bin/env python3
from styles import *
from elements import *
from writer import *
from renderer import Renderer
import default_formatters
import sys
from parser import Parser

p = Parser()

doc = p.parse(sys.stdin.read())

renderer = Renderer(DisplayWriter(sys.stdout, 30))
renderer.formatters['Paragraph'] = default_formatters.ParagraphFormatter()
renderer.formatters['Heading'] = default_formatters.HeadingFormatter()
renderer.formatters['Strong'] = default_formatters.StrongFormatter()
renderer.formatters['Emphasis'] = default_formatters.EmphasisFormatter()
renderer.formatters['InlineCode'] = default_formatters.InlineCodeFormatter()
renderer.formatters['Link'] = default_formatters.AppendLinkFormatter()
renderer.formatters['List'] = default_formatters.ListFormatter()
renderer.formatters['ListItem'] = default_formatters.ListItemFormatter()
renderer.formatters['OrderedList'] = 'List'
renderer.formatters['OrderedListItem'] = default_formatters.OrderedListItemFormatter()

renderer.render_document(doc)

sys.stdout.write('\n')
sys.stdout.flush()
sys.stdout.close()


