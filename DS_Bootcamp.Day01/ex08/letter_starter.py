import sys

def letter_starter(email, filepath):
    with open(filepath, 'r') as file:
        for line in file.readlines()[1:]:
            line_upd = [i.rstrip() for i in line.split('\t')]
            if email in line_upd:
                return f'Dear {line_upd[0]}, welcome to our team. We are sure that it will be a pleasure ' \
                        'to work with you. That’s a precondition for the professionals that our company hires.'
    raise Exception

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            letter = letter_starter(sys.argv[1], 'employees.tsv')
            print(letter)
    except FileNotFoundError:
        print('File does not exist')
    except Exception:
        print('E-mail not found')