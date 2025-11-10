import sys
from random import randint

class Research:
    def __init__(self, path):
        self.path = path
        self.data = self.file_reader()
        self.calc = self.Analytics(self.data)
    
    def file_reader(self, has_header=True):
        with open(self.path, "r") as file:
            data = file.readlines()
            header = data[0].split(',')
            if len(header) == 2:
                if header[0].isdigit() and header[1].rstrip('\n').isdigit():
                    has_header = False
            else:
                raise Exception
            if check_structure(data, has_header) == False:
                raise Exception
            file.seek(0)
            data = file.readlines()
            flag = 0
            if has_header:
                flag = 1
            res = [[int(i) for i in line.rstrip('\n').split(',')] for line in data[flag:]]
            return res
        
    class Calculations:
        def __init__(self, data):
            self.data = data
        
        def counts(self, data):
            heads = tails = 0
            for i in data:
                if i[0] == 1:
                    heads += 1
                else:
                    tails += 1
            return heads, tails       
        
        def fractions(self, count_0, count_1):
            sum_count = count_0 + count_1
            return count_0 / sum_count * 100, count_1 / sum_count * 100
    
    class Analytics(Calculations):
        def predict_random(self, count):
            rand_list = [[0, 1], [1, 0]]
            return [rand_list[randint(0, 1)] for _ in range(0, count)]
        
        def predict_last(self):
            return self.data[-1]

def check_structure(data, has_header):
    res = True
    flag = 0
    if has_header:
        flag = 1
    regexp = ['0', '1']
    for line in data[flag:]:
        check = line.rstrip('\n').split(',')
        if len(check) == 2:
            if check[0] not in regexp or check[1] not in regexp or check[0] == check[1]:
                res = False
                break
        else:
            res = False
            break
    return res

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            res = Research(sys.argv[1])
            count_0, count_1 = res.calc.counts(res.data)
            fraction_0, fraction_1 = res.calc.fractions(count_0, count_1)
            print(res.data)
            print(count_0, count_1)
            print(fraction_0, fraction_1)
            print(res.calc.predict_random(3))
            print(res.calc.predict_last())
        else:
            raise ValueError
    except ValueError:
        print("Error: Incorrect amount of arguments")
    except FileNotFoundError:
        print("Error: File not found")
    except Exception:
        print("Error: Incorrect file structure")