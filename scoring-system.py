# coding: utf-8

import ui
from main_view import MainView
from scoring   import * ## need the scoring algorithms
from sql_utils import * ## need to do some SQL stuff
from io        import * ## we shall see...

database = ':memory:'

def init_nav_view(root,main):
	rw,rh = root.width, root.height
	lw,lh = root['label1'].width, root['label1'].height
	nav_view = ui.NavigationView(main)
	nav_view.frame = (0,lh,rw,rh-lh)
	nav_view.flex = 'wlrt'
	return nav_view

@ui.in_background
def add_judge(sender):
	

main_view = ui.load_view('main_view')
root_view = ui.load_view()

nav_view  = init_nav_view(root_view,main_view)

root_view.add_subview(nav_view)
root_view.present('sheet')
