# individual result for each interaction event
class Result:
    # intialization
    def __init__(self, recommended, expected, nth):
        # get attributes
        self.nth = nth
        self.num_recommendation = len(recommended)
        self.num_expected = len(expected)
        self.num_correct = len([x for x in recommended if x in expected])
        self.num_wrong = self.num_recommendation - self.num_correct

        # calculate precision and recall
        self.precision = self.num_correct / self.num_recommendation
        if self.num_expected == 0: # divide by zero
            self.recall = None
        else:
            self.recall = self.num_correct / self.num_expected

# individual result for each interaction trace
class TraceResult:
    # initialization
    def __init__(self, filename):
        self.filename = filename
        self.results = []
    
    # add event result
    def add(self, recommended, expected, nth):
        self.results.append(Result(recommended, expected, nth))

    # get earliest recommendation count
    def nth(self):
        # if there is no recommendation in the trace, print error
        if len(self.results) == 0:
            print('error')
            exit()

        # find smallest nth value among recommendations
        nth = 99999999
        for result in self.results:
            if result.nth < nth:
                nth = result.nth
        return nth

    # get number of events with recommendation
    def num_recommendation(self):
        return len(self.results)

    # get number of correct recommendations
    def num_correct(self):
        count = 0
        for result in self.results:
            count += result.num_correct
        return count
    
    # get number of wrong recommendations
    def num_wrong(self):
        count = 0
        for result in self.results:
            count += result.num_wrong
        return count

    def precision(self):
        sum_precision = 0
        divider_precision = 0
        for result in self.results:
            sum_precision += result.precision
            divider_precision += 1
        if divider_precision == 0:
            return 0
        return sum_precision / divider_precision


# total result for a project - including individual event results
class TotalResult:
    # initialization
    def __init__(self):
        self.trace_results = []
    
    # add recommendation result for a interaction trace
    def add(self, trace_result):
        self.trace_results.append(trace_result)

    # count total number of events with recommendation
    def num_recommendation(self):
        count = 0
        for trace_result in self.trace_results:
            count += trace_result.num_recommendation()
        return count
    
    # number of correct recommendations
    def num_correct(self):
        count = 0
        for trace_result in self.trace_results:
            count += trace_result.num_correct()
        return count
    
    # number of wrong recommendations
    def num_wrong(self):
        count = 0
        for trace_result in self.trace_results:
            count += trace_result.num_wrong()
        return count
    
    # get precision, recall, and f-measure
    def statistics(self):
        sum_precision = 0
        divider_precision = 0
        sum_recall = 0
        divider_recall = 0

        for trace_result in self.trace_results:
            for result in trace_result.results:
                sum_precision += result.precision
                divider_precision += 1
                # for recall, ignore recommendations with empty expected results
                if result.recall != None:
                    sum_recall += result.recall
                    divider_recall += 1
        

        precision = sum_precision / divider_precision
        recall = sum_recall / divider_recall

        fmeasure = 2 * precision * recall / (precision + recall)

        return precision, recall, fmeasure
    
    # get average recommendation timepoint
    def nth(self):
        temp_sum = 0
        divider = 0
        # sum all nth count
        for trace_result in self.trace_results:
            for result in trace_result.results:
                temp_sum += result.nth
                divider += 1
        
        return temp_sum // divider

    # get earlist recommendation timepoint
    def earliest_nth(self):
        temp_sum = 0

        # get average among traces
        for trace_result in self.trace_results:
            temp_sum += trace_result.nth()
        
        return temp_sum // len(self.trace_results)
        