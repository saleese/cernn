import os
from libs.readfile import read

# interaction trace set
class InteractionTraceSet:
    def __init__(self, directory_name):
        self.directory_name = directory_name
        self.interaction_trace_set = []
        self.event_set = set()
        self.edit_set = set()
        self.view_set = set()
        self.initialize()

    def initialize(self):
        self.get_interaction_trace_set()
        self.get_unique_event_set()

    def get_interaction_trace_set(self):
        # get file list of interaction traces
        file_list = os.listdir(self.directory_name)
        file_list = [x for x in file_list if x[-3:] == 'xml']
        file_list = sorted(file_list, key=lambda x: x.split('-')[2])

        # iterate all files in the directory
        for i in range(len(file_list)):
            filename = file_list[i]
            # get interaction trace from file
            self.interaction_trace_set.append(read(self.directory_name + filename))

    def get_unique_event_set(self):
        interaction_trace_set = self.interaction_trace_set

        for interaction_trace in interaction_trace_set:
            self.event_set.update(interaction_trace.event_tuple_set)
            self.edit_set.update(interaction_trace.edit_set)
            self.view_set.update(interaction_trace.view_set)
        
        self.event_set = sorted(self.event_set, key=lambda x: x[1])
        self.edit_set = sorted(self.edit_set)
        self.view_set = sorted(self.view_set)

    def get_max_len_interaction_trace(self):
        return max([x.num_events for x in self.interaction_trace_set])
