import os
import sys

from pythonParser import hackFile


def path_to_string(path):
    asm = open(path)
    lines = ''
    for line in asm_file:
        lines += line
    return lines


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
    for asm_file in files:
        hackFile(path_to_string(asm_file))
