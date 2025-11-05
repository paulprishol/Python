import sys

def marketing(task):
    clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
        'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
        'elon@paypal.com', 'jessica@gmail.com']
    participants = ['walter@heisenberg.com', 'vasily@mail.ru',
        'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
        'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
    recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']
    if task == 'call_center':
        return call_center(clients, recipients)
    elif task == 'potential_clients':
        return potential_clients(clients, participants)
    elif task == 'loyalty_program':
        return loyalty_program(clients, participants)

def call_center(clients, recipients):
    return list(set(clients) - set(recipients))

def potential_clients(clients, participants):
    return list(set(participants) - set(clients))

def loyalty_program(clients, participants):
    return list(set(clients) - set(participants))

if __name__ == '__main__':
    tasks = ['call_center', 'potential_clients', 'loyalty_program']
    try:
        if len(sys.argv) == 2 and sys.argv[1] in tasks:
            result = marketing(sys.argv[1])
            print(result)
        else:
            raise ValueError
    except ValueError:
            print(f"Error: command not found")
