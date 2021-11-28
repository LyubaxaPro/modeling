from time import time
from random import random
TIME_DELTA = 0.01
FINISH_PROCESS_REQUEST = 1
СURRENT_REQUEST = 0
DONT_HAVE_FREE_OPERATOR = -1

class Time:
    def get_time(self):
        return 0


class TimeDistribution(Time):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def get_time(self):
        return self.a + (self.b - self.a) * random()
    
    
class TimeConstant(Time):
    def __init__(self, t):
        self.t = t

    def get_time(self):
        return self.t
    
    
class TimeProcessor:
    def __init__(self, time_distribution):
        self.time_distribution = time_distribution
        self.remaining_time = 0

    def update_time(self):
        if self.remaining_time > 0:
            self.remaining_time -= TIME_DELTA

        if self.remaining_time <= 1e-5:
            self.remaining_time = self.time_distribution.get_time()
            return Request()

        return None


class Operator:
    def __init__(self, recipient, time_distribution):
        self.time_distribution = time_distribution
        self.recipient = recipient
        self.remaining_time = 0
        self.is_busy = False
        self.processing_request = None

    def update_time(self):
        self.remaining_time -= TIME_DELTA
        if self.is_busy and self.remaining_time <= 1e-5:
            self.finish_process_request()

    def start_process_new_request(self, request):
        self.is_busy = True
        self.processing_request = request
        self.remaining_time = self.time_distribution.get_time()

    def finish_process_request(self):
        self.recipient.append(self.processing_request)
        self.is_busy = False
        self.processing_request = None


class Request:
    request_id = 0

    def __init__(self):
        global СURRENT_REQUEST
        self.request_id = СURRENT_REQUEST
        СURRENT_REQUEST += 1

class Processor:
    def __init__(self, requests_storage, time_distribution):
        self.requests_storage = requests_storage
        self.time_distribution = time_distribution
        self.is_busy = False
        self.processing_request = None
        self.remaining_time = 0

    def update_time(self):
        if self.remaining_time != 0:
            self.remaining_time -= TIME_DELTA

        if self.is_busy and self.remaining_time <= 1e-5:
            self.is_busy = False
            self.processing_request = None
            return FINISH_PROCESS_REQUEST

        if not self.is_busy and len(self.requests_storage) != 0:
            self.processing_request = self.requests_storage.pop(0)
            self.remaining_time = self.time_distribution.get_time()
            self.is_busy = True


def find_free_operator(operators):
    for i in range(len(operators)):
        if not operators[i].is_busy:
            return i
    return DONT_HAVE_FREE_OPERATOR


def iteration(clients, operators, processors, request_info, is_new=True):
    if is_new:
        request = clients.update_time()
        if request:
            request_info['generated_count'] += 1
            free_operator_number = find_free_operator(operators)
            if free_operator_number == DONT_HAVE_FREE_OPERATOR:
                request_info['lost_count'] += 1
            else:
                operators[free_operator_number].start_process_new_request(request)

    for operator in operators:
        operator.update_time()

    for processor in processors:
        result = processor.update_time()
        if result == FINISH_PROCESS_REQUEST:
            request_info['processed_count'] += 1


def modeling(clients, operators, processors, requests_count):
    statistics_info = {'generated_count': 0, 'processed_count': 0, 'lost_count': 0}

    while statistics_info['generated_count'] < requests_count:
        iteration(clients, operators, processors, statistics_info)

    while statistics_info['lost_count'] + statistics_info['processed_count'] < requests_count:
        iteration(clients, operators, processors, statistics_info, False)

    return statistics_info


if __name__ == '__main__':
    requests_count = int(input("Введите количество запросов: "))
    if requests_count <= 0:
        print("Неверное количество запросов")
        exit(1)

    clients = TimeProcessor(TimeDistribution(8, 12))

    storage_1 = []
    storage_2 = []

    processors = [Processor(storage_1, TimeConstant(15)), Processor(storage_2, TimeConstant(30))]

    operators = [Operator(storage_1, TimeDistribution(15, 25)), Operator(storage_1, TimeDistribution(30, 50)),
                 Operator(storage_2, TimeDistribution(20, 60))]

    start_time = time()

    result = modeling(clients, operators, processors, requests_count)

    print('Время работы программы (в секундах): ', round((time() - start_time), 4))
    print('Общее количество запросов: ', result['generated_count'])
    print('Количество обработанных запросов: ', result['processed_count'])
    print('Количество запросов, которым было отказано в обработке: ', result['lost_count'])
    print('Процент запросов, которым было отказано в обработке: ', round((result['lost_count'] / requests_count), 4))
