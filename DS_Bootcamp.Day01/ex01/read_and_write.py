def line_process(line):
    in_quotes = 1
    new_line = ""
    for i in line:
        if i == '"':
            in_quotes *= -1
        if i == ',' and in_quotes == 1:
            new_line += '\t'
        else:
            new_line += i
    return new_line

def read_and_write(input_file, output_file):
    with open(input_file, 'r') as source:
        dest = open(output_file, 'w')
        for line in source.readlines():
            dest.write(line_process(line))
        dest.close()

if __name__ == '__main__':
    try:
        read_and_write("ds.csv", "ds.tsv")
    except FileNotFoundError:
        print('File does not exist')
