#!/usr/bin/env python3
from styles import *
from elements import *
from writer import *
from renderer import Renderer
import default_formatters
import sys
from parser import Parser
from config import Config
import logging

logging.basicConfig(level=logging.DEBUG)

config = Config(['defaults', '~/.vmdrc'])

config.load()

p = Parser()

doc = p.parse(sys.stdin.read())

renderer = Renderer(DisplayWriter(sys.stdout))
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
renderer.formatters['HorizontalRule'] = default_formatters.HorizontalRuleFormatter(config)
renderer.formatters['CodeBlock'] = default_formatters.CodeBlockFormatter(config)

renderer.render_document(doc)

sys.stdout.write('\n')
sys.stdout.flush()
sys.stdout.close()


