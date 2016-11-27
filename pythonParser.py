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
        self.lines1 = self.parseLines(fileToParse)
        t = self.parser_line
        print("hey")
        l = map(t,self.lines1)
        print(list(l))
        print(self.lines1)
        exit()

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
            if(line is ''):
                continue
            count += 1
            parsedLines.append(line.replace(' ',''))
        sndParsed = []
        for line in parsedLines:
            m = varNumFinder.search(line)
            if(m):
                if(m.group(1) in self.vDef):
                    sndParsed.append("@%s"%self.vDef[m.group(1)])
                else:
                    sndParsed.append("@%s" %self.allocateMemory())
            else:
                sndParsed.append(line)
        return sndParsed


    def allocateMemory(self):
        if(self.memory in self.vDef.values()):
            self.memory+=1
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
        second_split = line.index(';') #there is a bug here.
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
        print(line)
        if line[0] == '@':
            print("A")
            return self.parser_a_instruction(line)
        else:
            print("C")
            return self.parser_c_instruction(line)
