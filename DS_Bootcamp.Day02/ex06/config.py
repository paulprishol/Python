import logging

token = "8228489203:AAHkmGEwo9_hhWZh-90c-NQ6beThvfzBD-w"
url = f"https://api.telegram.org/bot{token}/sendMessage"
chat_id = "338135148"
input_path = "data.csv"
output_path = "report"
num_of_steps = 3
template = """We have made {} observations from tossing a coin: {} of them were tails and {} of
them were heads. The probabilities are {}% and {}%, respectively. Our
forecast is that in the next {} observations we will have: {} tails and {} heads."""
logging.basicConfig(level=logging.INFO, filename="analytics.log",
                    format="%(asctime)s %(message)s")