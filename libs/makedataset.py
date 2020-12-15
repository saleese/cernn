from collections import OrderedDict

def integer_encode(mylist):
    return {v: i for i, v in enumerate(mylist)}

def integer_encode_without_zero_index(mylist):
    return {v: i+1 for i, v in enumerate(mylist)}

def get_key_from_value(mydict, myvalue):
    return [k for k, v in mydict.items() if v == myvalue]

def make_dataset(kind, trace, file_indexes, category_indexes, window_size, step, lookup, oversampling=0, is_various_window=False, is_remove_dupe=False):
    if is_remove_dupe:
        event_tuple_list = trace.event_tuple_list_groupby
    else:        
        event_tuple_list = trace.event_tuple_list

    # input and output
    contexts_list, output = [], []

    if kind is 'train':
        for i in range(len(event_tuple_list) - window_size):
            context = event_tuple_list[i:(i+window_size)]
            recommend = []

            if context[-1][0] == 'edit':
                recommend = [category_indexes[x[1]] for x in event_tuple_list[(i + window_size):(i + window_size + lookup)] if x[0] is 'edit' and x != context[-1]]
                # recommend = [category_indexes[x[1]] for x in event_tuple_list[(i+window_size):(i+window_size+lookup)] if x[0] is 'edit' and x[1] not in list(map(lambda x: x[1], context))]
                # recommend = [category_indexes[x[1]] for x in event_tuple_list[(i+window_size):(i+window_size+lookup)] if x[0] is 'edit' and x not in context]
                # recommend = [category_indexes[x[1]] for x in event_tuple_list[(i+window_size):(i+window_size+lookup)] if x[0] is 'edit']

            if recommend:
                recommend = list(OrderedDict.fromkeys([x for x in recommend]))[:step]

                if is_various_window:
                    for j in range(window_size):
                        contexts_list.append([file_indexes[x] for x in context[j:]])
                        output.append(recommend)
                elif oversampling:
                    for j in range(oversampling):
                        contexts_list.append([file_indexes[x] for x in context])
                        output.append(recommend)
                else:
                    contexts_list.append([file_indexes[x] for x in context])
                    output.append(recommend)
    else:
        for i in range(len(event_tuple_list)-window_size):
            context = event_tuple_list[i:(i+window_size)]
            recommend = []

            if context[-1][0] == 'edit':
                recommend_candidates = [x for x in event_tuple_list[(i+window_size):(i+window_size+lookup)] if x[0] is 'edit']
                if recommend_candidates:
                    recommend = [category_indexes[x[1]] for x in recommend_candidates if x != context[-1]]
                    recommend = list(OrderedDict.fromkeys([x for x in recommend]))[:step]
                    output.append(recommend)
                    contexts_list.append([file_indexes[x] for x in context])

    return contexts_list, output


if __name__ == '__main__':
    import numpy as np
    from keras.preprocessing import sequence
    from libs.interaction_traces import InteractionTraces

    # directory of interaction traces
    directory_name = 'dataset/Project_ECF/'
    interaction_trace_set = InteractionTraces(directory_name)

    # file index
    idx = integer_encode_without_zero_index(interaction_trace_set.event_set)
    # print(idx)
    category = integer_encode(interaction_trace_set.edit_set)
    # print(category)
    num_category = len(interaction_trace_set.edit_set)

    trace = interaction_trace_set.interaction_trace_set[1]
    # print(trace.event_edit_tuple_list)

    x_train, y_train = make_dataset('train', trace, idx, category, window_size=4, step=5, lookup=30, is_various_window=True, is_remove_dupe=False)
    x_test, y_test = make_dataset('test', trace, idx, category, window_size=4, step=5, lookup=30, is_remove_dupe=False)
    
    x_train = np.array(x_train)
    x_train = sequence.pad_sequences(x_train, maxlen=4)
    
    # y_train = [np.array(x) for x in y_train]
    # y_train = [to_categorical(x, num_category) for x in y_train]
    # y_train = np.array([x.sum(axis=0) for x in y_train])

    print(x_train)
    print(y_train)
    print(x_test)
    print(y_test)

    # print(x_train.shape)
    # print(y_train.shape)