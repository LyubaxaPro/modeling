from prettytable import PrettyTable
from scipy.stats import poisson, uniform
from numpy import random as numpy_random
import sys
COUNT = 10000
class Generator:
    def __init__(self, generator):
        self.generator = generator
        self.receivers = set()

    def add_receiver(self, receiver):
        self.receivers.add(receiver)

    def remove_receiver(self, receiver):
        try:
            self.receivers.remove(receiver)
        except KeyError:
            print("Ошибка!")
            sys.exit(0)

    def get_time(self):
        return self.generator.generate()

    def request(self):
        for receiver in self.receivers:
            receiver.receive_request()

class Processor(Generator):
    def __init__(self, generator, reenter_prob=0):
        super().__init__(generator)
        self.queue_size = 0
        self.max_queue_size = 0
        self.processed_requests = 0
        self.reentered_requests = 0
        self.reenter_prob = reenter_prob

    # Обработка запроса
    def process(self):
        if self.queue_size > 0:
            self.processed_requests += 1
            self.queue_size -= 1
            self.request()
            # Возвращение запроса в очередь при соблюдении условий вероятности
            if numpy_random.random_sample() <= self.reenter_prob and self.reentered_requests < self.reenter_prob * COUNT:
                self.reentered_requests += 1
                self.receive_request()

    # Добавление запроса в очередь
    def receive_request(self):
        self.queue_size += 1
        if self.queue_size > self.max_queue_size:
            self.max_queue_size = self.queue_size

class UniformDistribution:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b
        self.scale = self.b - self.a

    def generate(self):
        return uniform.rvs(loc=self.a, scale=self.scale, size=1)[0]


class PoissonDistribution:
    def __init__(self, lmbda):
        self.lmbda = lmbda

    def generate(self):
        return poisson.rvs(self.lmbda, size=1)[0]


class Model:
    def __init__(self, uniform_a, uniform_b, lmbda, reenter_prop):
        self.generator = Generator(UniformDistribution(uniform_a, uniform_b))
        self.processor = Processor(PoissonDistribution(lmbda), reenter_prop)
        self.generator.add_receiver(self.processor)

    def event_based_system(self, request_count):
        generator = self.generator
        processor = self.processor

        gen_period = generator.get_time()
        proc_period = gen_period + processor.get_time()

        while processor.processed_requests < request_count:
            if gen_period <= proc_period:
                generator.request()
                gen_period += generator.get_time()
            if gen_period >= proc_period:
                processor.process()

                if processor.queue_size > 0:
                    proc_period += processor.get_time()
                else:
                    proc_period = gen_period + processor.get_time()

        return (processor.processed_requests, processor.reentered_requests,
                processor.max_queue_size, round(proc_period, 3))

    def time_based_modelling(self, request_count, dt):
        generator = self.generator
        processor = self.processor

        gen_period = generator.get_time()
        proc_period = gen_period
        current_time = 0
        while processor.processed_requests < request_count:
            if gen_period <= current_time:
                generator.request()
                gen_period += generator.get_time()
            if current_time >= proc_period:
                processor.process()
                if processor.queue_size > 0:
                    proc_period += processor.get_time()
                else:
                    proc_period = gen_period + processor.get_time()

            current_time += dt

        return (processor.processed_requests, processor.reentered_requests,
                processor.max_queue_size, round(current_time, 3))

if __name__ == '__main__':

    a, b = map(int, input("Введите(через пробел) значения параметров a и b для равномерного распределения: ").split())

    if a >= b:
        print("Параметр a должен быть меньше параметра b")
        sys.exit(0)

    lmbda = int(input("Введите λ для распределения Пуассона: "))

    if lmbda < 0:
        print("λ должна быть больше 0")
        sys.exit(0)

    repeat_probality = float(input("Введите максимальное значение процента задач, которые возвращаются в очередь после обработки (в %): "))
    if repeat_probality >= 0 and repeat_probality <= 100:
        repeat_probality = repeat_probality / 100
    else:
        print("Неверный ввод")
        sys.exit(0)

    total_tasks = COUNT
    step = 0.01

    model = Model(a, b, lmbda, repeat_probality)
    result1 = model.event_based_system(total_tasks)
    model2 = Model(a, b, lmbda, repeat_probality)
    result2 = model2.time_based_modelling(total_tasks, step)

    table = PrettyTable()
    table.add_column("Метод", ["Событийный", "Пошаговый"])
    table.add_column("Кол-во обработанных запросов", [result1[0], result2[0]])
    table.add_column("Кол-во возвращенных запросов", [result1[1], result2[1]])
    table.add_column("Максимальный размер очереди", [result1[2], result2[2]])
    table.add_column("Время работы ", [result1[3], result2[3]])
    print(table)