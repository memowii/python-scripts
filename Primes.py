from math import sqrt

def IsPrime(n):
	"""Returns True if a number is prime, otherwise returns False"""
	if n == 0 or n == 1:
		return False
	
	for divisor in xrange(2, int(sqrt(n))+1):
		if n % divisor == 0:
			return False
	else:
		return True

def GetPrimeList(n):
	return [num for num in xrange(n+1) if IsPrime(num)]

def GetNPrimes(n):
	"""Returns a list with n prime numbers"""
	NPrimes, TPrimes, num = [], 0, 0
	while TPrimes < n:
		if IsPrime(num):
			NPrimes.append(num)
			TPrimes += 1
		num += 1
	else:
		return NPrimes

def GetRemainders(n):
	_sum, PrimeList = 1, GetNPrimes(n)
	for PrimeN in PrimeList:
		_sum *= PrimeN
	else:
		_sum += 1

	for PrimeN in PrimeList:
		print _sum, PrimeN, _sum % PrimeN, float(_sum) / PrimeN, PrimeList


GetRemainders(14)
