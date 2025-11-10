import sys

class Research():
    def __init__(self, path):
        self.path = path
    
    def file_reader(self):
        with open(self.path, "r") as file:
            data = file.readlines()
            if check_structure(data):
                file.seek(0) 
                return file.read()
            else:
                raise Exception
        
def check_structure(data):
    res = True
    if len(data[0].split(',')) != 2 or len(data) < 2:
        res = False
    else:
        regexp = ['0', '1']
        for line in data[1:]:
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
            print(res.file_reader())
        else:
            raise ValueError
    except ValueError:
        print("Error: Incorrect amount of arguments")
    except FileNotFoundError:
        print("Error: File not found")
    except Exception:
        print("Error: Incorrect file structure")