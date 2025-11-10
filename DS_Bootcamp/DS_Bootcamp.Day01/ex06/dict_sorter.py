def dict_sorter():
    list_of_tuples = [
        ('Russia', '25'),
        ('France', '132'),
        ('Germany', '132'),
        ('Spain', '178'),
        ('Italy', '162'),
        ('Portugal', '17'),
        ('Finland', '3'),
        ('Hungary', '2'),
        ('The Netherlands', '28'),
        ('The USA', '610'),
        ('The United Kingdom', '95'),
        ('China', '83'),
        ('Iran', '76'),
        ('Turkey', '65'),
        ('Belgium', '34'),
        ('Canada', '28'),
        ('Switzerland', '26'),
        ('Brazil', '25'),
        ('Austria', '14'),
        ('Israel', '12')
    ]

    dictionary = dict(list_of_tuples)
    for v in sorted([int(i) for i in set(dictionary.values())], reverse=True):
        for k in get_key_list(dictionary, str(v)):
            print(k)
        
def get_key_list(dictionary, value):
    key_list = []
    for k, v in dictionary.items():
        if v == value:
            key_list.append(k)
    return sorted(key_list)

if __name__ == '__main__':
    dict_sorter()