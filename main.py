import os
import sys

from pythonParser import hackFile


def path_to_string(path):
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
        tmp = hackFile(path_to_string(asm_file))
        tmp.save(asm_file)


# def parser_dest(dest):
#     d1 = '0'
#     d2 = '0'
#     d3 = '0'
#     if 'A' in dest:
#         d1 = '1'
#     if 'M' in dest:
#         d3 = '1'
#     if 'D' in dest:
#         d2 = '1'
#     return d1 + d2 + d3
#
#
# def parser_comp(comp):
#     a = '0' if 'A' in comp else '1'
#     comp.replace('M', 'A')
#     inst1 = '1'
#     inst2 = '1'
#     c1 = '0'
#     c2 = '0'
#     c3 = '0'
#     c4 = '0'
#     c5 = '0'
#     c6 = '0'
#     if '<<' in comp:
#         inst2 = '0'
#         c1 = '1'
#         if comp[2] == 'D':
#             a = '0'
#             c2 = '1'
#         return inst1 + inst2 + a + c1 + c2 + c3 + c4 + c5 + c6
#     elif '>>' in comp:
#         inst2 = '0'
#         if comp[2] == 'D':
#             a = '0'
#             c2 = '1'
#         return inst1 + inst2 + a + c1 + c2 + c3 + c4 + c5 + c6
#     if comp == '0':
#         c1 = '1'
#         c3 = '1'
#         c5 = '1'
#     elif comp == '1':
#         c1 = '1'
#         c2 = '1'
#         c3 = '1'
#         c4 = '1'
#         c5 = '1'
#         c6 = '1'
#     elif comp == '-1':
#         c1 = '1'
#         c2 = '1'
#         c3 = '1'
#         c5 = '1'
#     elif comp == 'D':
#         c3 = '1'
#         c4 = '1'
#     elif comp == 'A':
#         c1 = '1'
#         c2 = '1'
#     elif comp == '!D':
#         c3 = '1'
#         c4 = '1'
#         c6 = '1'
#     elif comp == '!A':
#         c1 = '1'
#         c2 = '1'
#         c6 = '1'
#     elif comp == '-D':
#         c3 = '1'
#         c4 = '1'
#         c5 = '1'
#         c6 = '1'
#     elif comp == '-A':
#         c1 = '1'
#         c2 = '1'
#         c5 = '1'
#         c6 = '1'
#     elif comp == 'D+1':
#         c2 = '1'
#         c3 = '1'
#         c4 = '1'
#         c5 = '1'
#         c6 = '1'
#     elif comp == 'A+1':
#         c1 = '1'
#         c2 = '1'
#         c4 = '1'
#         c5 = '1'
#         c6 = '1'
#     elif comp == 'D-1':
#         c3 = '1'
#         c4 = '1'
#         c5 = '1'
#     elif comp == 'A-1':
#         c1 = '1'
#         c2 = '1'
#         c5 = '1'
#     elif comp == 'D+A':
#         c5 = '1'
#     elif comp == 'D-A':
#         c2 = '1'
#         c5 = '1'
#         c6 = '1'
#     elif comp == 'A-D':
#         c4 = '1'
#         c5 = '1'
#         c6 = '1'
#     elif comp == 'D!A':
#         c2 = '1'
#         c4 = '1'
#         c6 = '1'
#     return inst1 + inst2 + a + c1 + c2 + c3 + c4 + c5 + c6
#
#
# def parser_jmp(jmp):
#     if jmp == 'JGT':
#         return '001'
#     elif jmp == 'JEQ':
#         return '010'
#     elif jmp == 'JGE':
#         return '011'
#     elif jmp == 'JLT':
#         return '100'
#     elif jmp == 'JNE':
#         return '101'
#     elif jmp == 'JLE':
#         return '110'
#     else:
#         return '111'
#
#
# def parser_c_instruction(line):
#     first_split = line.index('=')
#     if first_split > -1:
#         dest = parser_dest(line[:first_split])
#         line = line[first_split + 1:]
#     else:
#         dest = '000'
#     second_split = line.index(';')
#     if second_split == -1:
#         comp = parser_comp(line)
#         jmp = '000'
#     else:
#         comp = parser_comp(line[:second_split])
#         jmp = parser_jmp(line[second_split + 1:])
#     return '1' + comp + dest + jmp
#
#
# def parser_a_instruction(line):
#     tmp_bin = str(bin(int(line[1:])))[2:]
#     length = len(tmp_bin)
#     if length < 15:
#         return '0' * (15 - length) + tmp_bin
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
