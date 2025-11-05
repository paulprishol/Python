import timeit
import sys

def loop_append(data: list):
    res = []
    for email in data:
        if email.endswith('gmail.com'):
            res.append(email)
    return res

def list_comprehension(data: list):
    return [email for email in data if email.endswith('gmail.com')]

def list_map(data: list):
    return list(map(lambda email: email if email.endswith('gmail.com') else None, data))

def list_filter(data: list):
    return list(filter(lambda email: email.endswith('gmail.com'), data))

def case_func(emails, func, count):
    match func:
        case 'loop':
            exec_time = timeit.timeit(lambda: loop_append(emails), number=count)
        case 'list_comprehension':
            exec_time = timeit.timeit(lambda: list_comprehension(emails), number=count)
        case 'map':
            exec_time = timeit.timeit(lambda: list_map(emails), number=count)
        case 'filter':
            exec_time = timeit.timeit(lambda: list_filter(emails), number=count)
    return exec_time

if __name__ == '__main__':
    try:
        if len(sys.argv) == 3:
            emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
                    'anna@live.com', 'philipp@gmail.com'] * 5
            functions = ['loop', 'list_comprehension', 'map', 'filter']
            func, count = sys.argv[1].lower(), int(sys.argv[2])
            if count <= 0:
                raise IndexError
            if func in functions:
                exec_time = case_func(emails, func, count)
                print(exec_time)
            else:
                raise NameError
        else:
            raise Exception
    except (ValueError, AttributeError, TypeError) as e:
        print(f'Error: {e}')
    except NameError:
        print('Error: Incorrect function name. Try \'loop\', \'list_comprehension\', \'map\' or \'filter\'')
    except IndexError:
        print('Error: number of calls must be more than 0')
    except Exception:
        print('Error: Incorrect amount of arguments')