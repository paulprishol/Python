import timeit

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

if __name__ == '__main__':
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
              'anna@live.com', 'philipp@gmail.com'] * 5
    exec_time_loop = timeit.timeit(lambda: loop_append(emails), number=90000000)
    exec_time_comp = timeit.timeit(lambda: list_comprehension(emails), number=90000000)
    exec_time_map = timeit.timeit(lambda: list_map(emails), number=90000000)
    exec_time = sorted([exec_time_loop, exec_time_comp, exec_time_map])
    if exec_time[0] == exec_time_comp:
        print('it is better to use a list comprehension')
    elif exec_time[0] == exec_time_loop:
        print('it is better to use a loop')
    else:
        print('it is better to use a map')
    print(f'{exec_time[0]} vs {exec_time[1]} vs {exec_time[2]}')