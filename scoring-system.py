# coding: utf-8

import ui
from scoring   import * ## need the scoring algorithms
from sql_utils import * ## need to do some SQL stuff
from io        import * ## we shall see...

def push_view(sender):
	'@type sender: ui.Button'
	nav_view = sender.superview
	nav_view.push_view(ui.View())

v = ui.load_view()
options = ui.ButtonItem('Options')
v.right_button_items = [options]
print v['nav-view']
v.present('sheet')
