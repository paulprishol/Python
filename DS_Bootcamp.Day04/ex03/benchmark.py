import timeit
import sys
from functools import reduce

def loop_sum(num):
    sum = 0
    for i in range(num + 1):
        sum += i * i
    return sum

def reduce_sum(num):
    return reduce(lambda sum, i: sum + i * i, range(num + 1))

def case_func(num, func, count):
    match func:
        case 'loop':
            exec_time = timeit.timeit(lambda: loop_sum(num), number=count)
        case 'reduce':
            exec_time = timeit.timeit(lambda: reduce_sum(num), number=count)
    return exec_time

if __name__ == '__main__':
    try:
        if len(sys.argv) == 4:
            functions = ['loop', 'reduce']
            func, count, num = sys.argv[1].lower(), int(sys.argv[2]), int(sys.argv[3])
            if count <= 0 or num <= 0:
                raise IndexError
            if func in functions:
                exec_time = case_func(num, func, count)
                print(exec_time)
            else:
                raise NameError
        else:
            raise Exception
    except (ValueError, AttributeError, TypeError) as e:
        print(f'Error: {e}')
    except NameError:
        print('Error: Incorrect function name. Try \'loop\' or \'reduce\'')
    except IndexError:
        print('Error: endpoint and number of calls must be more than 0')
    except Exception:
        print('Error: Incorrect amount of arguments')