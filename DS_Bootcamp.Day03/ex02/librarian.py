import os
import tarfile

if __name__ == '__main__':
    try:
        if os.environ["VIRTUAL_ENV"].endswith("cleansee"):
            os.system('pip install Beautifulsoup4 pytest')
            os.system('pip freeze')
            os.system('pip freeze > requirements.txt')
            archive = 'venv_archive.tar'
            with tarfile.open(archive, 'w') as tar:
                tar.add(os.environ["VIRTUAL_ENV"], archive)
        else:
            raise KeyError
    except KeyError:
        print('Error: Wrong environment')
    except FileExistsError:
        print('Error: File already exists')