import re

isComment = re.compile("[ ]*//")
emptyLine = re.compile(" *")
varFinder = re.compile("\(([A-Za-z0-9_\,\.\$\-]+)\)")
varNumFinder = re.compile("@([A-Za-z_-][A-Za-z0-9_\,\.\$\-]*)")

compute_to_bin = {'0': '101010', '1': '111111', '-1': '111010', 'D': '001100', 'A': '110000', '!D': '001101',
                  '!A': '110001', '-D': '001111', '-A': '110011', 'D+1': '011111', 'A+1': '110111',
                  'D-1': '001110', 'A-1': '110010', 'D+A': '000010', 'D-A': '010011', 'A-D': '000111',
                  'D&A': '000000', 'D|A': '010101'}


def parser_jmp(jmp):
    if jmp == 'JGT':
        return '001'
    elif jmp == 'JEQ':
        return '010'
    elif jmp == 'JGE':
        return '011'
    elif jmp == 'JLT':
        return '100'
    elif jmp == 'JNE':
        return '101'
    elif jmp == 'JLE':
        return '110'
    else:
        return '111'


def parser_a_instruction(line):
    tmp_bin = str(bin(int(line[1:])))[2:]
    length = len(tmp_bin)
    if length < 15:
        return '0' * (16 - length) + tmp_bin
    elif length == 15:
        return '0%s' % tmp_bin
    else:
        return '0%s' % tmp_bin[-15:]


def parser_destination(destination):
    d1 = '1' if 'A' in destination else '0'
    d2 = '1' if 'D' in destination else '0'
    d3 = '1' if 'M' in destination else '0'
    return d1 + d2 + d3


def parser_comp(comp):
    a = '1' if 'M' in comp else '0'
    comp = comp.replace('M', 'A')
    c2 = '0'
    if '<<' in comp:
        c1 = '1'
        if comp[0] == 'D':
            a = '0'
            c2 = '1'
        return '01' + a + c1 + c2 + '0000'
    elif '>>' in comp:
        c1 = '0'
        if comp[0] == 'D':
            c2 = '1'
        return '01' + a + c1 + c2 + '0000'
    else:
        c = compute_to_bin[comp]
        return '11' + a + c


def parser_c_instruction(line):
    first_split = line.find('=')
    if first_split > -1:
        destination = parser_destination(line[:first_split])
        line = line[first_split + 1:]
    else:
        destination = '000'
    second_split = line.find(';')
    if second_split == -1:
        comp = parser_comp(line)
        jmp = '000'
    else:
        comp = parser_comp(line[:second_split])
        jmp = parser_jmp(line[second_split + 1:])
    return '1' + comp + destination + jmp


def parser_line(line):
    if line[0] == '@':
        return parser_a_instruction(line)
    else:
        return parser_c_instruction(line)


class HackFile:
    def __init__(self, file_to_parse):
        self.memory = 16
        self.vDef = {"KBD": 24576, "SCREEN": 16384, "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4}
        for i in range(16):
            self.vDef["R" + str(i)] = i
        self.lines = self.parse_lines(file_to_parse)
        l = self.lines.copy()
        self.lines.clear()
        for line in l:
            self.lines.append(parser_line(line))

    def parse_lines(self, lines):
        count = 0
        lines = lines.split("\n")
        parsed_lines = []
        for line in lines:
            m = isComment.search(line)
            if m:
                line = line[0:m.span()[0]]
            if line is '':
                continue
            line = self.change_variables(line, count)
            if line is '':
                continue
            count += 1
            parsed_lines.append(line.replace(' ', ''))
        snd_parsed = []
        c = 0
        for line in parsed_lines:
            m = varNumFinder.search(line)
            if m:
                if m.group(1) in self.vDef:
                    snd_parsed.append("@%s" % self.vDef[m.group(1)])
                else:

                    km = self.allocate_memory()
                    snd_parsed.append("@%s" % km)
                    self.vDef[m.group(1)] = km
            else:
                snd_parsed.append(line)
            c += 1
        return snd_parsed

    def allocate_memory(self):
        m = self.memory
        self.memory += 1
        return m

    def change_variables(self, line, count):

        m = varFinder.search(line)
        if m:
            self.vDef[m.group(1)] = count
            return ''
        return line

    def save(self, path):
        k = path.rfind(".")
        path = path[:k] + ".hack"
        f = open(path, 'w')
        for line in self.lines:
            f.write(line)
            f.write("\n")
