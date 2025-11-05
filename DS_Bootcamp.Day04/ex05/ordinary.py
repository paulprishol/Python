import sys
import resource

def file_read(path):
    with open(path, 'r') as file:
        content = file.readlines()
    return content

if __name__ == '__main__':
    try:
        if len(sys.argv) == 2:
            start = resource.getrusage(resource.RUSAGE_SELF)
            filename = sys.argv[1]
            content = file_read(filename)
            for i in content:
                pass
            end = resource.getrusage(resource.RUSAGE_SELF)
            peak_memory = end.ru_maxrss / (1024 * 1024)
            user_time = end.ru_utime - start.ru_utime
            system_time = end.ru_stime - start.ru_stime
            total_time = user_time + system_time
            print(f"Peak Memory Usage = {peak_memory:.3f} GB")
            print(f"User Mode Time + System Mode Time = {total_time:.2f}s")
        else:
            raise Exception
    except(FileExistsError, FileNotFoundError,
           ValueError, AttributeError, TypeError) as e:
        print(f'Error: {e}')
    except Exception:
        print('Error: Incorrect amount of arguments')