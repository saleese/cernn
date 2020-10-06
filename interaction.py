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

# interaction trace
class InteractionTrace:
    def __init__(self, event_list, name):
        # get source file name
        self.name = name[name.rfind('/') + 1:]

        # get interaction event list
        self.event_list = event_list

        # sort by startdate
        self.event_list = sorted(self.event_list, key=lambda x: x.time)

        # get the number of interaction events
        self.num_events = len(self.event_list)

        # get interaction filenames list
        self.event_list_names = [x.filename for x in self.event_list]

        # get interaction tuple of (type, filenames)
        self.event_tuple_list = [(x.type, x.filename) for x in self.event_list]

        # [k for k, g in groupby('AAAABBBCCDAABBB')] --> A B C D A B
        self.event_tuple_list_groupby = [k for k, g in groupby(self.event_tuple_list)]

        '''temp = [k for k, g in groupby(self.event_tuple_list)]
        self.event_tuple_set_groupby = [temp[0]]
        for x, y in zip(temp, temp[1:]):
            self.event_tuple_set_groupby.pop()
            if x[0] is 'view' and y[0] is 'edit' and x[1] == y[1]:
                self.event_tuple_set_groupby.append(y)
            else:
                self.event_tuple_set_groupby.extend([x, y])'''

        # get interaction event set
        self.event_tuple_set = list(OrderedDict.fromkeys([x for x in self.event_tuple_list]))

        # get string set of viewed files
        self.view_set = list(OrderedDict.fromkeys([x.filename for x in self.event_list if x.type == 'view']))

        # get string set of edited files
        self.edit_set = list(OrderedDict.fromkeys([x.filename for x in self.event_list if x.type == 'edit']))
