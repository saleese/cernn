import os
from collections import deque
from collections import Counter
from itertools import repeat, chain

from libs.readfile import read
from mi.result import TraceResult, TotalResult

# directory of interaction traces
directory_name = 'dataset/Project_Platform/'

# configurable context size constants
context_size_view = 3
context_size_edit = 1

# recommendation
def recommend():
    # variables
    mined_rules = [] # list of interaction traces

    # statistics variables
    num_queries = 0

    context_queue_view = deque([], context_size_view) # view context queue
    context_queue_edit = deque([], context_size_edit) # edit context queue

    # get file list of interaction traces
    file_list = os.listdir(directory_name)
    file_list = [x for x in file_list if x[-3:] == 'xml']
    file_list = sorted(file_list)

    # total result
    total_result = TotalResult()

    # iterate all files in the directory
    for ii in range(len(file_list)):
        filename = file_list[ii]
        # get interaction trace from file
        trace = read(directory_name + filename)

        # TEST =================================================================

        # initialize nth counter
        nth_count = 0

        # initialize result for an interaction trace
        trace_result = TraceResult(filename)

        # initialization
        context_queue_view.clear()
        context_queue_edit.clear()

        # iterate events
        for event in trace.event_list:
            nth_count += 1 # n-th event increment

            # recommendation list for a context
            recommendation_list = []

            # form context
            brecommend = False
            if event.type == 'view':
                if not event.filename in context_queue_view:
                    context_queue_view.append(event.filename)
                    brecommend = True
            
            elif event.type == 'edit':
                if not event.filename in context_queue_edit:
                    context_queue_edit.append(event.filename)
                    brecommend = True
            
            if check_condition(context_queue_view, context_queue_edit, brecommend):
                #print(event.filename)
                num_queries+=1

                for rule in mined_rules:

                    view_flag = True
                    for view in context_queue_view:
                        if not view in rule.view_set:
                            view_flag = False
                    edit_flag = True
                    for edit in context_queue_edit:
                        if not edit in rule.edit_set:
                            edit_flag = False
                    
                    if view_flag and edit_flag:
                        #print(rule.name)
                        for x in rule.edit_set:
                            if not x in context_queue_edit:
                                if len(rule.view_set) == 0:
                                    print('error')
                                    exit()
                                if not x in context_queue_view:
                                    recommendation_list.append(x)
            
            if len(recommendation_list) != 0:
                # sort
                #print(len(recommendation_list), len(set(recommendation_list)))
                recommendation_list = list(chain.from_iterable(repeat(i, c) for i,c in Counter(recommendation_list).most_common()))
                # remove duplicates
                seen = set()
                seen_add = seen.add
                recommendation_list = [x for x in recommendation_list if not (x in seen or seen_add(x))]
                # top 10 list
                recommendation_list = recommendation_list[:10]

                expected_results = [x for x in trace.edit_set if not x in context_queue_edit and not x in context_queue_view]
                trace_result.add(recommendation_list, expected_results, nth_count)
                #if len(expected_results) != 0:
                #    trace_result.add(expected_results[:10], expected_results, nth_count)

                    
        # append trace result into total result
        if len(trace_result.results) != 0:
            total_result.add(trace_result)


        mined_rules.append(trace)


    (precision, recall, fmeasure) = total_result.statistics()
    print('precision :', precision)
    print('recall :', recall)
    print('feedback :', total_result.num_recommendation() / num_queries)
    print('true :', total_result.num_correct())
    print('false :', total_result.num_wrong())
    print('num_Q :', num_queries)
    print('num_R :', total_result.num_recommendation())
    print('fmeasure :', fmeasure)
    print('average nth :', total_result.nth())
    print('average earliest :', total_result.earliest_nth())

    print('================================')

            
def check_condition(cqv, cqe, b):
    if len(cqv) >= context_size_view and len(cqe) >= context_size_edit and b:
        return True
    return False

if __name__ == '__main__':
    recommend()