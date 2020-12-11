from collections import OrderedDict
from itertools import groupby

# interaction event
class InteractionEvent:
    def __init__(self, event):
        # get attributes - time, name, type
        self.time = event.get('StartDate')
        self.endtime = event.get('EndDate')
        self.filename_full = event.get('StructureHandle')
        temp_type = event.get('Kind')
        if temp_type == 'edit':
            self.type = 'edit'
        elif temp_type == 'selection':
            self.type = 'view'

        # if startdate = enddate --> view
        if self.time == event.get('EndDate') and self.type == 'edit':
            self.type = 'view'

        # get filename
        self.filename = self.filename_full
        if '{' in self.filename:
            self.filename = self.filename[self.filename.rfind('{'):]
        if '/' in self.filename:
            self.filename = self.filename[self.filename.rfind('/'):]
        if '[' in self.filename:
            self.filename = self.filename[:self.filename.find('[')]