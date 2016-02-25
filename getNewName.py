from os import system

def getNewName(oldName):
    return '-'.join(oldName.lower().split(' ')) + '.sh'

def getTerminalSentence(newName):
    return 'echo ' + "'" + newName + "'" + ' | ' + 'pbcopy'

def putValInPb(terminalSentence):
    system(getTerminalSentence(getNewName(terminalSentence)))

putValInPb('hola mundo querido')
