from random import randint
from config import *
import requests

class Research:
    def __init__(self, path):
        logging.info("Creating object Research")
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
            logging.info("Reading file and making list of heads and tails")
            return res
        
    def send_message(self, status: bool):
        if status:
            params = {"chat_id": chat_id, "text": "The report has been successfully created"}
        else:
            params = {"chat_id": chat_id, "text": "The report hasn't been created due to an error"}
        response = requests.get(url, params=params)
        if response.ok:
            logging.info("Sending message")
        else:
            logging.info(f"Error: Can't send message, status code: {response.status_code}")

    class Calculations:
        def __init__(self, data):
            logging.info("Creating object Calculations")
            self.data = data
        
        def counts(self, data):
            logging.info("Calculating the counts of heads and tails")
            heads = tails = 0
            for i in data:
                if i[0] == 1:
                    heads += 1
                else:
                    tails += 1
            return heads, tails       
        
        def fractions(self, count_0, count_1):
            logging.info("Calculating percentage ratio of heads and tails")
            sum_count = count_0 + count_1
            return count_0 / sum_count * 100, count_1 / sum_count * 100
    
    class Analytics(Calculations):
        def predict_random(self, count):
            logging.info("Predicting the next coin tosses")
            rand_list = [[0, 1], [1, 0]]
            return [rand_list[randint(0, 1)] for _ in range(0, count)]
        
        def predict_last(self):
            logging.info("Taking the last coin toss")
            return self.data[-1]
        
        def save_file(self, data, filename, ext = 'txt'):
            logging.info("Saving information into the file")
            with open(f'{filename}.{ext}', 'w') as file:
                file.write(data)

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