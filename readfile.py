from xml.etree.ElementTree import parse

from interaction import InteractionEvent, InteractionTrace

# read xml file and return InteractionTrace object
def read(filename):
    # parse xml file
    tree = parse(filename)
    root = tree.getroot()

    # list of events in the interaction trace
    event_list = []

    # iterate events
    for event in root.getchildren():
        # if event type is either selection or edit, append to event list
        if event.get('Kind') in ['selection', 'edit']:
            event_list.append(InteractionEvent(event))
    
    return InteractionTrace(event_list, filename)

# check existence of edit
def check_edit(filename):
    tree = parse(filename)
    root = tree.getroot()

    for event in root.getchildren():
        if event.get('Kind') == 'edit':
            if event.get('StartDate') != event.get('EndDate'):
                return True
    
    return False

# main for testing
if __name__ == '__main__':
    directory_name = 'AllProjects/Project_MDT/'

    '''import os
    file_list = os.listdir(directory_name)
    file_list = [x for x in file_list if x[-3:] == 'xml']
    file_list = sorted(file_list)

    v = 0
    e = 0
    vv = 0
    ee = 0

    for filename in file_list:
        trace = read(directory_name + filename)
        vv += len(trace.view_set)
        ee += len(trace.edit_set)
        for event in trace.event_list:
            if event.type == 'view':
                v += 1
            elif event.type == 'edit':
                e += 1
            else:
                print('error')
                exit()
        
    print(len(file_list))
    print(v / len(file_list), e / len(file_list))
    print(vv / len(file_list), ee / len(file_list))'''
    
    '''trace = read(directory_name + 'MDT-249789-157262.xml')
    print(len(trace.event_list))
    new = []
    prev = None
    prev_type = None
    for event in trace.event_list:
        if event.filename != prev or (event.filename == prev and event.type != prev_type):
            prev = event.filename
            prev_type = event.type
            new.append(event)
    print(len(new))'''

    import os
    file_list = os.listdir(directory_name)
    file_list = [x for x in file_list if x[-3:] == 'xml']
    file_list = sorted(file_list)

    for filename in file_list:
        trace = read(directory_name + filename)
        if len(trace.edit_set) != 0:
            print(filename)

