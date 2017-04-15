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
import os
import re

logging.basicConfig(level=logging.DEBUG)

themes_directory = os.path.join(os.path.dirname(__file__), 'themes')

theme = os.path.join(themes_directory, 'default')

if 'VMD_THEME' in os.environ:
    if re.search('^[a-zA-Z_\-0-9]+$', os.environ['VMD_THEME']):
        theme = os.path.join(themes_directory, os.environ['VMD_THEME'])
    else:
        theme = os.environ['VMD_THEME']

config = Config([theme, '~/.vmdrc'])

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


