# coding: utf-8

import ui

class ScoreView (ui.View):
	def __init__(self, judges, contestants):
		self.judges      = judges
		self.contestants = contestants
		
		self.background_color = 1
		
		rows = len(self.contestants)
		cols = len(self.judges) + 2
		w,h  = ui.measure_string(string=' '*10, font=('DejaVuSansMono',24))
		for x in range(cols):
			for y in range(1,rows+1):
				if x is 0:
					label        = ui.Label()
					label.text   = ' %-5d %-10s'%self.contestants[y-1]
					label.width  = w
					label.height = h
					label.x      = x*w
					label.y      = y*h
					label.border_width = 1
					self.add_subview(label)
		
		self.size_to_fit()
		

judges      = [(1,'Brooks MacBeth'), (2,'Alexa MacBeth')]
contestants = [(1,'TJ Zito'),        (2,'Wendy Zito')]

v = ScoreView(judges, contestants)
v.present('sheet')
