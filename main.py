import os
import sys

from pythonParser import hackFile


def path_to_string(path):
    asm = open(path)
    lines = ''
    for line in asm:
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
#
#
# def parser_dest(dest):
#     return ''
#
#
# def parser_comp(comp):
#     return ''
#
#
# def parser_jmp(jmp):
#     return ''
#
#
# def parser_c_instruction(line):
#     first_split = line.index('=')
#     if first_split > -1:
#         dest = parser_dest(line[:first_split])
#         line = line[first_split + 1:]
#     else:
#         dest = ''
#     second_split = line.index(';')
#     if second_split == -1:
#         comp = parser_comp(line)
#         jmp = ''
#     else:
#         comp = parser_comp(line[:second_split])
#         jmp = parser_jmp(line[second_split + 1:])
#     return comp + dest + jmp
#
#
# def parser_a_instruction(line):
#     tmp_bin = str(bin(int(line[1:])))[2:]
#     length = len(tmp_bin)
#     if length < 15:
#         tmp_bin = '0' * (15 - length) + tmp_bin
#     elif length == 15:
#         return '0' + tmp_bin
#     else:
#         return '0' + tmp_bin[-15:]
#
#
# def parser_line(line):
#     if line[0] == '@':
#         return parser_a_instruction(line)
#     else:
#         return parser_c_instruction(line)
