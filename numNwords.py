
l0 = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"] 
l1 = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
l2 = "twenty"
l3 = "thirty"
l4 = "forty"
l5 = "fifty"
l6 = "sixty"
l7 = "seventy"
l8 = "eighty"
l9 = "ninety"
l10 = "hundred"

def createList(w):
	l = [w+l0[i] for i in range(1,10)]
	return [w] + l


NUM_WORDS = l0 + l1 + createList(l2) + createList(l3) + createList(l4) + createList(l5) + createList(l6) + createList(l7) + createList(l8) + createList(l9) + [l10]

# print(len(NUM_WORDS))

def word2num(w):
	try:
		return NUM_WORDS.index(w)
	except:
		print(f"Invalid key length: {w}")

def num2word(n):
	if n < 100:
		return NUM_WORDS[n]
	else:
		print(f"Vignere key length should be between {1} and {100}")
		return 0

