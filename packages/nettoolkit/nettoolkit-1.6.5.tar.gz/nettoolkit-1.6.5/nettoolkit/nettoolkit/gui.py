
# ---------------------------------------------------------------------------------------
try:
	import PySimpleGUI as sg
except:
	pass

import nettoolkit as nt
#
from .forms.gui_template import GuiTemplate
from .forms.tab_event_funcs import BUTTUN_PALLETE_NAMES, TAB_EVENT_UPDATERS
from .forms.formitems import *
from .forms.var_frames import FRAMES
from .forms.var_event_funcs import EVENT_FUNCTIONS
from .forms.var_event_updators import EVENT_UPDATORS
from .forms.var_event_item_updators import EVENT_ITEM_UPDATORS
from .forms.var_retractables import RETRACTABLES
#
from nettoolkit.addressing.forms.subnet_scanner import count_ips
# ---------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Class to initiate UserForm
# -----------------------------------------------------------------------------

class Nettoolkit(GuiTemplate):
	'''Minitools UserForm asking user inputs.	'''

	# Object Initializer
	def __init__(self):
		self.header = f'Nettoolkit: {nt.version()} - {super().header}'
		super().__init__()
		self.initialize_variables()
		self.set_button_pallete()

	def initialize_variables(self):
		"""Initialize all variables
		"""		
		self.tabs_dic = FRAMES
		self.event_catchers = EVENT_FUNCTIONS
		self.event_updaters = EVENT_UPDATORS
		self.event_item_updaters = EVENT_ITEM_UPDATORS
		#
		self.tab_updaters = self.tab_updaters.union(TAB_EVENT_UPDATERS)
		#
		self.retractables = RETRACTABLES
		#
		self.custom_dynamic_cmd_class = None      # custom dynamic commands execution class
		self.custom_ff_class = None  # custom facts-finder class
		self.custom_fk = {}          # custom facts-finder foreign keys

	def user_events(self, i, event):
		"""specific event catchers

		Args:
			i (dict): dictionary of GUI fields variables
			event (str): event
		"""		
		if event == 'file_md5_hash_check':
			self.event_update_element(file_md5_hash_value={'value': ""})
		if event == 'go_count_ips':
			self.event_update_element(ss_ip_counts={'value': count_ips(i['pfxs'], i['till'])})

	@property
	def cleanup_fields(self):
		"""fields variables which are to be cleaned

		Returns:
			set: retractables
		"""		
		return self.retractables

	def set_button_pallete(self):
		"""button pallete definition
		"""		
		nbpb = [sg.Button(name, change_submits=True, key=key) for name, key in BUTTUN_PALLETE_NAMES.items()]
		self.add_to_button_pallete_buttons(nbpb)


# ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- ---------- 



# ------------------------------------------------------------------------------
# Main Function
# ------------------------------------------------------------------------------
if __name__ == '__main__':
	pass
# ------------------------------------------------------------------------------
