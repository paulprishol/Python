from analytics import Research
import requests
from config import *

if __name__ == '__main__':
    try:
        res = Research(input_path)
        if res.data is not None:
            count_0, count_1 = res.calc.counts(res.data)
            fraction_0, fraction_1 = res.calc.fractions(count_0, count_1)
            predict = res.calc.predict_random(num_of_steps)
            predict_0, predict_1 = res.calc.counts(predict)
            data = template.format(count_0 + count_1, count_0, count_1, round(fraction_0, 2), round(fraction_1, 2), num_of_steps, predict_0, predict_1)
            res.calc.save_file(data, output_path, 'txt')
            res.send_message(status=True)
        else:
            res.send_message(status=False)
    except FileNotFoundError as fn:
        print("Error: File not found")
        logging.error(f"Error: {fn}") 
    except FileExistsError as fe:
        print("Error: File already exists")     
        logging.error(f"Error: {fe}")   
    except ValueError as v:
        print(f"Error: {v}")
        logging.error(f"Error: {v}")  
    except TypeError as t:
        print(f"Error: {t}")
        logging.error(f"Error: {t}")  
    except Exception as e:
        print("Error: Incorrect file structure")
        logging.error(f"Error: File {input_path} has an incorrect structure")