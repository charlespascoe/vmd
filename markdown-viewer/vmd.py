#!/usr/bin/env python3
from styles import *
from elements import *
from writer import *
from renderer import Renderer
import default_formatters
import sys
from parser import Parser
from config import Config

config = Config('~/.vmdrc')

config.load()

p = Parser()

doc = p.parse(sys.stdin.read())

renderer = Renderer(DisplayWriter(sys.stdout, 30))
renderer.formatters['Paragraph'] = default_formatters.ParagraphFormatter(config)
renderer.formatters['Heading'] = default_formatters.HeadingFormatter(config)
renderer.formatters['Strong'] = default_formatters.StrongFormatter(config)
renderer.formatters['Emphasis'] = default_formatters.EmphasisFormatter(config)
renderer.formatters['InlineCode'] = default_formatters.InlineCodeFormatter(config)
renderer.formatters['Link'] = default_formatters.AppendLinkFormatter(config)
renderer.formatters['List'] = default_formatters.ListFormatter()
renderer.formatters['ListItem'] = default_formatters.ListItemFormatter(config)
renderer.formatters['OrderedList'] = 'List'
renderer.formatters['OrderedListItem'] = default_formatters.OrderedListItemFormatter(config)

renderer.render_document(doc)

sys.stdout.write('\n')
sys.stdout.flush()
sys.stdout.close()


