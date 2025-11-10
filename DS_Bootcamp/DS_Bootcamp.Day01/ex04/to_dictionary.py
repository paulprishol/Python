def to_dictionary():
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

    keys_set = {i[1] for i in list_of_tuples}
    dictionary = {}
    for i in keys_set:
        dictionary.update({i: get_value(list_of_tuples, i)})
    for k, v in dictionary.items():
        for i in v:
            print("{:5} : {:1}".format(f"'{k}'", f"'{i}'"))
        
def get_value(list_of_tuples, k):
    values = []
    for i in list_of_tuples:
        if k in i:
            values.append(i[0])
    return values

if __name__ == '__main__':
    to_dictionary()