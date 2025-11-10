def data_types():
    i = 1
    st = "str"
    f = 1.5
    b = True
    l = [1, 2, 3]
    d = {1: 'a', 2: 'b', 3: 'c'}
    t = (1, 2, 3)
    s = {1, 2, 3}
    types = [i.__name__ for i in [type(i), type(st), type(f), type(b), type(l), type(d), type(t), type(s)]]
    print(f'[{', '.join(types)}]')

if __name__ == '__main__':
      data_types()
