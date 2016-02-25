import sys

class Phrase(object):
	WordsList = []

	def __init__(self, phrase=''):
		self.phrase = phrase

	def GetWordsList(self):
		for word in self.phrase.split(' '):
			Top, Middle, Button = Word(word).GetNewFormat()
			Phrase.WordsList.append([Top, Middle, Button])
	
	def PrintNewFormattedWord(self): 
		for i in xrange(3):
			for j in xrange(len(Phrase.WordsList)):
				sys.stdout.write(Phrase.WordsList[j][i])
				sys.stdout.write(' ')
			sys.stdout.write('\n')

class Word(object):
	def __init__(self, word=''):
		self.word = word

	def GetNewFormat(self):
		Nmiddle = '* ' + self.word + ' *'
		Ntop = len(Nmiddle) * '*'
		Nbutton = len(Nmiddle) * '*'
		return Ntop, Nmiddle, Nbutton

def Main():
	UserPhrase = raw_input('Write a phrase: ')
	print
	phrase = Phrase(UserPhrase)
	phrase.GetWordsList()
	phrase.PrintNewFormattedWord()
	print

Main()