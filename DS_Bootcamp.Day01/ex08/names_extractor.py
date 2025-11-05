import sys

def names_extractor(filepath):
    with open(filepath, 'r') as input_file:
        output_file = open('employees.tsv', 'w')
        output_file.write('Name\tSurname\tE-mail\n')
        for line in input_file.readlines():
            output_file.write(get_info(line))
        output_file.close()

def get_info(line):
    res = line.split('@')
    res = res[0].split('.')
    return res[0].capitalize() + "\t" + res[1].capitalize() + "\t" + line

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            names_extractor(sys.argv[1])
    except FileNotFoundError:
        print('File does not exist')