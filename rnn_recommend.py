import numpy as np
import argparse
from time import time

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, GRU
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras import backend as K # added by saleese, Oct. 07, 2020

from libs.interaction_traces import InteractionTraces
from libs.makedataset import make_dataset, integer_encode, integer_encode_without_zero_index

# parser initialization
def add_argments2parser():
    # parser initialization
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', choices=['Mylyn', 'Platform', 'PDE', 'ECF', 'MDT'])
    parser.add_argument('--remove_dupe', action='store_true', default=False)
    parser.add_argument('--window_size', type=int, default=4)
    parser.add_argument('--step', type=int, default=10)
    parser.add_argument('--lookup', type=int, default=1000)
    parser.add_argument('--embedding_size', type=int, default=512)
    parser.add_argument('--lstm_memory_cells', type=int, default=256)
    parser.add_argument('--lstm_dropout', type=float, default=0)
    parser.add_argument('--lstm_recurrent_dropout', type=float, default=0)
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--epochs', type=int, default=100)
    parser.add_argument('--threshold', type=float, default=0.5)
    parser.add_argument('--top_k', type=int, default=10, choices=range(1, 11))
    parser.add_argument('--start_trace_num', type=int, default=1)
    return parser

def create_ytrain(y_train_list_temp, num_categories, is_init, y_train):
    if y_train_list_temp:
        temp = [np.array(x) for x in y_train_list_temp]
        temp = [to_categorical(x, num_categories) for x in temp]
        temp = np.array([x.sum(axis=0) for x in temp])

        if is_init:
            y_train = np.copy(temp)
            is_init = False
        else:
            y_train = np.vstack((y_train, temp))
    return is_init, y_train

def create_model(num_files, num_categories):
    model = Sequential()
    model.add(Embedding(num_files,
                        embedding_size,
                        # num_categories,
                        # embeddings_initializer='glorot_uniform',
                        embeddings_initializer='random_uniform',
                        mask_zero=True,
                        input_length=window_size))
    # model.add(GRU(num_categories))
    model.add(LSTM(num_categories, activation='sigmoid'))
    # model.add(LSTM(num_categories, dropout=lstm_dropout, activation='sigmoid'))
    # model.add(LSTM(lstm_memory_cells, return_sequences=True, dropout=lstm_dropout))
    # model.add(LSTM(lstm_memory_cells, dropout=lstm_dropout))
    # model.add(Dense(num_categories, activation='sigmoid'))
    # model.add(Dense(num_categories, activation='softmax'))
    # print(model.summary())

    # model setting
    model.compile(loss='binary_crossentropy',
                  # loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model

def print_intermediate_result(precision_list, recall_list, num_queries, num_recommendations):
    print(' Queries:', num_queries)
    print(' Recommendations:', num_recommendations)

    if precision_list:
        print(' Precision: {0:.4f}'.format(sum(precision_list) / len(precision_list)))
        print(' Recall: {0:.4f}'.format(sum(recall_list) / len(recall_list)))
        print(' Feedback: {0:.4f}'.format(num_recommendations / num_queries))
        # logFile = open("log.txt", "a+")
        # logFile.write('{0:.4f}'.format(sum(precision_list) / len(precision_list)) + ", " + '{0:.4f}'.format(sum(recall_list) / len(recall_list)) + "\n")
        # logFile.close()

def print_final_result(precision_list, recall_list, num_queries, num_recommendations):
    # final result
    total_precision = total_recall = f_measure = 0.0

    if precision_list:
        total_precision = sum(precision_list) / len(precision_list)
        total_recall = sum(recall_list) / len(recall_list)

    if total_precision + total_recall:
        f_measure = (2 * total_precision * total_recall) / (total_precision + total_recall)

    print('==================================')
    print(' Final Result')
    print('==================================')
    print(' Precision: {0:.4f}'.format(total_precision))
    print(' Recall: {0:.4f}'.format(total_recall))
    print(' F-measure: {0:.4f}'.format(f_measure))
    print(' Feedback: {0:.4f}'.format(num_recommendations / num_queries))
    print(' Recommendations:', num_recommendations)
    print('==================================')
    print(' Parameters')
    print(vars(args))
    print('==================================')

def print_time(start_time, end_time):
    # transform seconds to h:mm:ss
    m, s = divmod(int(end_time - start_time), 60)
    h, m = divmod(m, 60)

    print('==================================')
    print(' Execution Time: {0}h {1:02d}m {2:02d}s'.format(h, m, s))

parser = add_argments2parser()
# for a normal run
args = parser.parse_args()
# for a test
#args = parser.parse_args(
#    ["--project", "MDT", "--window_size", "3", "--step", "10", "--lookup", "1000", "--batch_size", "32",
#     "--epochs", "500", "--threshold", "0.91", "--remove_dupe"])

# project directory
directory_name = 'dataset/Project_{0}/'.format(args.project)

# remove redundant events in a trace (AAAABBBCCDAABBB -> ABCDAB)
is_remove_dupe = args.remove_dupe

# Hyperparameters
window_size = args.window_size
n_step = args.step
n_lookup = args.lookup
embedding_size = args.embedding_size
lstm_memory_cells = args.lstm_memory_cells
lstm_dropout = args.lstm_dropout
train_batch_size = args.batch_size
epochs = args.epochs
threshold = args.threshold
top_k = args.top_k
start_trace_num = args.start_trace_num

def run():
    # create interaction trace set
    interaction_traces = InteractionTraces(directory_name)

    # the number of learning
    iterations = len(interaction_traces.interaction_trace_set)

    # file index
    file_indexes = integer_encode_without_zero_index(interaction_traces.event_set)
    num_files = len(file_indexes) + 1
    
    # category_indexes and the number of categories (size of unique edit events)
    category_indexes = integer_encode(interaction_traces.edit_set)
    num_categories = len(category_indexes)
    
    # the number of queries
    num_queries = 0
    num_recommendations = 0

    # initialize train dataset
    x_train_list = []

    # to calculate precision and recall of a whole project
    precision_list, recall_list = [], []

    print('the number of files is', num_files) # 4082 for MDT, 1617 for ECF, 1961 for PDE, 6091 for Platform, 14195 for Mylyn
    print('the number of categories is', num_categories) # 114 for MDT, 150 for ECF, 351 for PDE, 786 for Platform, 2315 for Mylyn

    is_init = True
    y_train = None

    # record start time
    start_time = time()

    # prepare the pre-data
    for iteration in range(1, start_trace_num):
        # get each trace for training and test, respectively
        train_trace = interaction_traces.interaction_trace_set[iteration - 1]
        # load dataset
        x_train_list_temp, y_train_list_temp = make_dataset(train_trace, file_indexes, category_indexes,
                                                            window_size=window_size, step=n_step, lookup=n_lookup,
                                                            is_remove_dupe=is_remove_dupe)
        x_train_list += x_train_list_temp

        # make train set for multi labels
        is_init, y_train = create_ytrain(y_train_list_temp, num_categories, is_init, y_train)

        print('----------------------------------')
        print(' {0}th iteration'.format(iteration))

    # online learning
    for iteration in range(start_trace_num, iterations):

        # get each trace for training and test, respectively
        train_trace = interaction_traces.interaction_trace_set[iteration-1]
        test_trace = interaction_traces.interaction_trace_set[iteration]

        # load dataset
        x_train_list_temp, y_train_list_temp = make_dataset(train_trace, file_indexes, category_indexes,
                                                            window_size=window_size, step=n_step, lookup=n_lookup,
                                                            is_remove_dupe=is_remove_dupe)
        x_test_list, y_test_list = make_dataset(test_trace, file_indexes, category_indexes,
                                                window_size=window_size, step=n_step, lookup=n_lookup,
                                                is_remove_dupe=is_remove_dupe)
        x_train_list += x_train_list_temp

        # make train set for multi labels
        is_init, y_train = create_ytrain(y_train_list_temp, num_categories, is_init, y_train)

        print('----------------------------------')
        print(' {0}th iteration'.format(iteration))

        # training and evaluation
        if x_train_list and x_test_list:
            x_train = np.array(x_train_list)
            x_test = np.array(x_test_list)

            # create a model
            model = create_model(num_files, num_categories)

            # model learning (verbose: 0 = silent, 1 = progress bar, 2 = one line per epoch.)
            model.fit(x_train, y_train, batch_size=train_batch_size, epochs=epochs, verbose=0)

            # generate predictions
            pred = model.predict(x_test, verbose=0)
            # pred_class = model.predict_classes(x_test, verbose=0)
            # print(pred)

            # make recommendations
            for i in range(pred.shape[0]):
                # initialize precision and recall
                precision = recall = 0.0
                # get answers for test set
                answer_set = set(y_test_list[i])
                # get indices for top 10 recommendations
                ind = np.argsort(-pred[i])[:top_k]
                # get recommendations only above threshold
                recommend_set = set([x for x in ind if pred[i][x] > threshold])
                
                if recommend_set:
                    num_recommendations += 1
                    
                    if answer_set:
                        intersection_set_size = len(recommend_set & answer_set)
                        precision = intersection_set_size / len(recommend_set)
                        recall = intersection_set_size / len(answer_set)

                    precision_list.append(precision)
                    recall_list.append(recall)

                    # pairs of each recommendation and its probability
                    recommendations = [(x, round(pred[i][x], 4)) for x in recommend_set]

                    # print(' ', recommend_set, answer_set)
                    # print(' ', recommendations, answer_set)
                    print(' Context:', x_test_list[i])
                    print('   Recommendations:', recommendations)
                    print('   Answer Set:', answer_set)
                    print('   P: {0:.4f}, R: {1:.4f}'.format(precision, recall))

                    # the code block removing the remaining part when the first edit turns out to be false.
                    if (precision == 0.0) and (recall == 0.0):
                        recommend_set.clear()
                        answer_set.clear()
                        break

                recommend_set.clear()
                answer_set.clear()

            # This code is to remove a model from the memory
            K.clear_session() # added by saleese, Oct. 07, 2020
            del model # added by saleese, Oct. 07, 2020

        # print intermediate result
        num_queries += len(x_test_list)
        print_intermediate_result(precision_list, recall_list, num_queries, num_recommendations)

    # record end time
    end_time = time()

    print_time(start_time, end_time)
    print_final_result(precision_list, recall_list, num_queries, num_recommendations)

if __name__ == '__main__':
    run()
