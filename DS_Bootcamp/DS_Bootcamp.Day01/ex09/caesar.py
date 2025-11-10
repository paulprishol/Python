import sys

def encode(data, shift):
    res = ""
    for i in data:
        if i.isalpha():
            check = ord(i) + shift
            if check > ord('z') or (check > ord('Z') and ord(i) < ord('a')):
                check -= 26
            elif check < ord('A') or (check < ord('a') and ord(i) > ord('Z')):
                check += 26
            res += chr(check)
        else:
            res += i
    return res

def decode(data, shift):
    return encode(data, -shift)

def caesar(task, data, shift):
    if data.isascii() == False:
        raise Exception
    shift = int(shift) % 26
    res = ""
    if task == 'encode':
        res = encode(data, shift)
    elif task == 'decode':
        res = decode(data, shift)
    else:
        raise ValueError
    return res

if __name__ == '__main__':
    try:
        if len(sys.argv) == 4:
            res = caesar(sys.argv[1], sys.argv[2], sys.argv[3])
            print(res)
        else:
            raise TypeError
    except TypeError:
        print('Error: Incorrect amount of arguments')
    except ValueError:
        print('Error: Incorrect input')
    except Exception:
        print('Error: Only English language supported')