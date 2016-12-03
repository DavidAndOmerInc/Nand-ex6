#!/usr/bin/env python
import os
import sys

from PythonParser import HackFile


def path_to_string(path):
    print('parsing : %s'%path)
    asm = open(path)
    lines = ''
    for line in asm:
        lines += line
    asm.close()
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
        tmp = HackFile(path_to_string(asm_file))
        tmp.save(asm_file)
