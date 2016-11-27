import re

isComment = re.compile("[ ]*//")
emptyLine = re.compile(" *")
varFinder = re.compile("\(([A-Za-z0-9_-]+)\)")
varNumFinder = re.compile("@([A-Za-z_-][A-Za-z0-9_-]*)")


class hackFile:
    def __init__(self, fileToParse):
        self.memory = 16
        self.vDef = {}
        for i in range(15):
            self.vDef["R" + str(i)] = i
        self.lines = self.parseLines(fileToParse)
        l = self.lines.copy()
        self.lines.clear()
        for line in l:
            self.lines.append(self.parser_line(line))
    def parseLines(self, lines):
        count = 0
        lines = lines.split("\n")
        parsedLines = []
        for line in lines:
            m = isComment.search(line)
            if (m):
                line = line[0:m.span()[0]]
            if (line is ''):
                continue
            line = self.changeVariables(line, count)
            if (line is ''):
                continue
            count += 1
            parsedLines.append(line.replace(' ', ''))
        sndParsed = []
        for line in parsedLines:
            m = varNumFinder.search(line)
            if (m):
                if (m.group(1) in self.vDef):
                    sndParsed.append("@%s" % self.vDef[m.group(1)])
                else:
                    sndParsed.append("@%s" % self.allocateMemory())
            else:
                sndParsed.append(line)
        return sndParsed

    def allocateMemory(self):
        if (self.memory in self.vDef.values()):
            self.memory += 1
            return self.allocateMemory()
        m = self.memory
        self.memory += 1
        return m

    def changeVariables(self, line, count):
        m = varFinder.search(line)
        if (m):
            self.vDef[m.group(1)] = count
            return ''
        return line

    # Parse The asm file

    def parser_dest(self, dest):
        d1 = '0'
        d2 = '0'
        d3 = '0'
        if 'A' in dest:
            d1 = '1'
        if 'M' in dest:
            d3 = '1'
        if 'D' in dest:
            d2 = '1'
        return d1 + d2 + d3

    def parser_comp(self, comp):
        a = '0' if 'A' in comp else '1'
        comp.replace('M', 'A')
        inst1 = '1'
        inst2 = '1'
        c1 = '0'
        c2 = '0'
        c3 = '0'
        c4 = '0'
        c5 = '0'
        c6 = '0'
        if '<<' in comp:
            inst2 = '0'
            c1 = '1'
            if comp[2] == 'D':
                a = '0'
                c2 = '1'
            return inst1 + inst2 + a + c1 + c2 + c3 + c4 + c5 + c6
        elif '>>' in comp:
            inst2 = '0'
            if comp[2] == 'D':
                a = '0'
                c2 = '1'
            return inst1 + inst2 + a + c1 + c2 + c3 + c4 + c5 + c6
        if comp == '0':
            c1 = '1'
            c3 = '1'
            c5 = '1'
        elif comp == '1':
            c1 = '1'
            c2 = '1'
            c3 = '1'
            c4 = '1'
            c5 = '1'
            c6 = '1'
        elif comp == '-1':
            c1 = '1'
            c2 = '1'
            c3 = '1'
            c5 = '1'
        elif comp == 'D':
            c3 = '1'
            c4 = '1'
        elif comp == 'A':
            c1 = '1'
            c2 = '1'
        elif comp == '!D':
            c3 = '1'
            c4 = '1'
            c6 = '1'
        elif comp == '!A':
            c1 = '1'
            c2 = '1'
            c6 = '1'
        elif comp == '-D':
            c3 = '1'
            c4 = '1'
            c5 = '1'
            c6 = '1'
        elif comp == '-A':
            c1 = '1'
            c2 = '1'
            c5 = '1'
            c6 = '1'
        elif comp == 'D+1':
            c2 = '1'
            c3 = '1'
            c4 = '1'
            c5 = '1'
            c6 = '1'
        elif comp == 'A+1':
            c1 = '1'
            c2 = '1'
            c4 = '1'
            c5 = '1'
            c6 = '1'
        elif comp == 'D-1':
            c3 = '1'
            c4 = '1'
            c5 = '1'
        elif comp == 'A-1':
            c1 = '1'
            c2 = '1'
            c5 = '1'
        elif comp == 'D+A':
            c5 = '1'
        elif comp == 'D-A':
            c2 = '1'
            c5 = '1'
            c6 = '1'
        elif comp == 'A-D':
            c4 = '1'
            c5 = '1'
            c6 = '1'
        elif comp == 'D!A':
            c2 = '1'
            c4 = '1'
            c6 = '1'
        return inst1 + inst2 + a + c1 + c2 + c3 + c4 + c5 + c6

    def parser_jmp(self, jmp):
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

    def parser_c_instruction(self, line):
        first_split = line.find('=')
        if first_split > -1:
            dest = self.parser_dest(line[:first_split])
            line = line[first_split + 1:]
        else:
            dest = '000'
        second_split = line.find(';')  # there is a bug here.
        if second_split == -1:
            comp = self.parser_comp(line)
            jmp = '000'
        else:
            comp = self.parser_comp(line[:second_split])
            jmp = self.parser_jmp(line[second_split + 1:])
        return comp + dest + jmp

    def parser_a_instruction(self, line):
        tmp_bin = str(bin(int(line[1:])))[2:]
        length = len(tmp_bin)
        if length < 15:
            return '0' * (16 - length) + tmp_bin
        elif length == 15:
            return '0%s' % tmp_bin
        else:
            return '0%s' % tmp_bin[-15:]

    def parser_line(self, line):
        if line[0] == '@':
            return self.parser_a_instruction(line)
        else:
            return self.parser_c_instruction(line)

    def save(self, path):
        k = path.rfind(".")
        path = path[:k]+".hack"
        f = open(path, 'w')
        for line in self.lines:
            f.write(line)
            f.write("\n")
