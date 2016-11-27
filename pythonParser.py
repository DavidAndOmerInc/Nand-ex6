import re
isComment = re.compile("[ ]*//")
emptyLine = re.compile(" *")
varFinder = re.compile("\(([A-Za-z0-9]+)\)")
varNumFinder = re.compile("\((R?([0-9]|1[0-5]))")
class hackFile:
    def __init__(self, fileToParse):
        self.vDef = {}
        for i in range(15):
            self.vDef["R"+str(i)] = i
        __lines = self.parseLines(fileToParse)

    def parseLines(self, lines):
        count = 0
        lines = lines.split("\n")
        parsedLines = []
        for line in lines:
            m = isComment.search(line)
            if(m):
                line = line[0:m.span()[0]]
            if(line is ''):
                continue
            line = self.changeVariables(line, count)
            count+=1
            parsedLines.append(line)
        print(parsedLines)
        exit()

    def changeVariables(self,line, count):
        m = varFinder.search(line)
        if(m):
            self.vDef[m.group(1)] = count
            return "(%s)" %count
        return line







