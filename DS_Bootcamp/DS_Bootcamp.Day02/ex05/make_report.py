from analytics import Research
from config import *

if __name__ == '__main__':
    try:
        res = Research(input_path)
        count_0, count_1 = res.calc.counts(res.data)
        fraction_0, fraction_1 = res.calc.fractions(count_0, count_1)
        predict = res.calc.predict_random(num_of_steps)
        predict_0, predict_1 = res.calc.counts(predict)
        data = template.format(count_0 + count_1, count_0, count_1, round(fraction_0, 2), round(fraction_1, 2), num_of_steps, predict_0, predict_1)
        res.calc.save_file(data, output_path, 'txt')
    except FileNotFoundError:
        print("Error: File not found")
    except FileExistsError:
        print("Error: File already exists")        
    except Exception:
        print("Error: Incorrect file structure")