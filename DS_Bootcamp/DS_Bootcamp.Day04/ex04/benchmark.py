import timeit
import random
from collections import Counter

def list_to_dict_my(data: list):
    my_dict = {}
    for val in data:
        if val not in my_dict:
            my_dict[val] = 1
        else:
            my_dict[val] += 1
    return my_dict

def list_to_dict_counter(data: list):
    return Counter(data)

def top_ten_my(data: list):
    my_dict = list_to_dict_my(data)
    sorted_list = sorted(my_dict.items(), reverse=True, key=lambda item: item[1])
    return sorted_list[:10]

def top_ten_counter(data: list):
    return list_to_dict_counter(data).most_common()[:10]

if __name__ == '__main__':
    my_list = [random.randint(0, 100) for _ in range(1000000)]
    exec_time_my = timeit.timeit(lambda: list_to_dict_my(my_list), number=1)
    exec_time_counter = timeit.timeit(lambda: list_to_dict_counter(my_list), number=1)
    exec_time_my_top = timeit.timeit(lambda: top_ten_my(my_list), number=1)
    exec_time_counter_top = timeit.timeit(lambda: top_ten_counter(my_list), number=1)
    print(f'my function: {exec_time_my}')
    print(f'Counter: {exec_time_counter}')
    print(f'my top: {exec_time_my_top}')
    print(f'Counter\'s top: {exec_time_counter_top}')