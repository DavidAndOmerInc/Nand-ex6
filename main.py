import os
import sys

if __name__ == '__main__':
    arg = sys.argv
    if os.path.isdir(arg[1]):
        files = list()
        files_list = os.listdir(arg[1])
        for file in files_list:
            if file.endswith('.asm'):
                files.append(arg[1] + '/' + file)
    else:
        files = [arg[1]]

