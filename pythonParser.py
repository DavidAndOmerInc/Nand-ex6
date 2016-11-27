import re

isComment = re.compile("[ ]*//")
emptyLine = re.compile(" *")
varFinder = re.compile("\(([A-Za-z0-9]+)\)")
varNumFinder = re.compile("\((R?([0-9]|1[0-5]))")


class hackFile:
    def __init__(self, fileToParse):
        self.vDef = {}
        for i in range(15):
            self.vDef["R" + str(i)] = i
        __lines = self.parseLines(fileToParse)

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
            count += 1
            parsedLines.append(line)
        print(parsedLines)
        exit()

    def changeVariables(self, line, count):
        m = varFinder.search(line)
        if (m):
            self.vDef[m.group(1)] = count
            return "(%s)" % count
        return line

    # Parse The asm file

    def parser_dest(self, dest):
        return ''

    def parser_comp(self, comp):
        return ''

    def parser_jmp(self, jmp):
        return ''

    def parser_c_instruction(self, line):
        first_split = line.index('=')
        if first_split > -1:
            dest = self.parser_dest(line[:first_split])
            line = line[first_split + 1:]
        else:
            dest = ''
        second_split = line.index(';')
        if second_split == -1:
            comp = self.parser_comp(line)
            jmp = ''
        else:
            comp = self.parser_comp(line[:second_split])
            jmp = self.parser_jmp(line[second_split + 1:])
        return comp + dest + jmp

    def parser_a_instruction(self, line):
        tmp_bin = str(bin(int(line[1:])))[2:]
        length = len(tmp_bin)
        if length < 15:
            tmp_bin = '0' * (15 - length) + tmp_bin
        elif length == 15:
            return '0' + tmp_bin
        else:
            return '0' + tmp_bin[-15:]

    def parser_line(self, line):
        if line[0] == '@':
            return self.parser_a_instruction(line)
        else:
            return self.parser_c_instruction(line)
