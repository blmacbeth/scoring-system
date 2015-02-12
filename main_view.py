import ui, sql_utils

db_init = False
database = sql_utils.Database('test.db', db_init)
if db_init:
	database.add_judge(1, 'Brooks MacBeth')
	database.add_judge(2, 'Alexa MacBeth')

	database.add_competitor(1, 'TJ Zito')
	database.add_competitor(2, 'Wendy Zito')

class JudgeDataSource (object):
	def __init__(self, db):
		self.db = db
		self.items = []
		for id, judge in db.get_all_judges():
			s = '%3d %20s' % (id, judge)
			self.items.append({'title':s})

	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.selectable = True 
		cell.text_label.text = self.items[row]['title']
		return cell

	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		return 'Judges'

	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		pass

	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		pass

	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		pass

	def tableview_did_deselect(self, tableview, section, row):
		# Called when a row was de-selected (in multiple selection mode).
		pass

	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		return 'Delete'

class CompetitorDataSource (object): 
	def __init__(self, db):
		self.db = db
		self.items = []
		for id, comp in db.get_all_competitors():
			s = '%3d %20s' % (id, comp)
			self.items.append({'title':s})

	def tableview_number_of_sections(self, tableview):
		# Return the number of sections (defaults to 1)
		return 1

	def tableview_number_of_rows(self, tableview, section):
		# Return the number of rows in the section
		return len(self.items)

	def tableview_cell_for_row(self, tableview, section, row):
		# Create and return a cell for the given section/row
		cell = ui.TableViewCell()
		cell.selectable = True 
		cell.text_label.text = self.items[row]['title']
		return cell

	def tableview_title_for_header(self, tableview, section):
		# Return a title for the given section.
		# If this is not implemented, no section headers will be shown.
		return 'Competitors'

	def tableview_can_delete(self, tableview, section, row):
		# Return True if the user should be able to delete the given row.
		return False

	def tableview_can_move(self, tableview, section, row):
		# Return True if a reordering control should be shown for the given row (in editing mode).
		return False

	def tableview_delete(self, tableview, section, row):
		# Called when the user confirms deletion of the given row.
		pass

	def tableview_move_row(self, tableview, from_section, from_row, to_section, to_row):
		# Called when the user moves a row with the reordering control (in editing mode).
		pass

	def tableview_did_select(self, tableview, section, row):
		# Called when a row was selected.
		pass

	def tableview_did_deselect(self, tableview, section, row):
		# Called when a row was de-selected (in multiple selection mode).
		pass

	def tableview_title_for_delete_button(self, tableview, section, row):
		# Return the title for the 'swipe-to-***' button.
		return 'Delete'

class MainView (ui.View):
	def __init__(self):
		pass

	def did_load(self):
		judge_data = JudgeDataSource(database)
		self['judge-table'].data_source = judge_data
		self['judge-table'].delegate    = judge_data
		self['judge-table'].allows_multiple_selection = True
		
		competitor_data = CompetitorDataSource(database)
		self['competition-table'].data_source = competitor_data
		self['competition-table'].delegate    = competitor_data
		self['competition-table'].allows_multiple_selection = True

if __name__ == '__main__':
	v = ui.load_view()
	v.present('sheet')
