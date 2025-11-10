class Must_read():
    with open("data.csv", "r") as file:
        print(file.read())

if __name__ == '__main__':
    try:
        Must_read()
    except FileNotFoundError:
        print("Error: File not found")