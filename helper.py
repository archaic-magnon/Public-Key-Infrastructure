B = 27

def chr2int(c):
     return ord(c) - 97
    
def int2chr(n):
     return chr(n + 97)


def string2int(s):
    return [chr2int(el) for el in s]

def int2string(l):
    return "".join([int2chr(el) for el in l])

def gcd(a,b):
    if b==0:
        return a
    return gcd(b,a%b)


def inverse(a,m):
	pass


def int2baseB(n,r):
	a = []
	
	last_a = 0
	for i in range(r, 0, -1):
		last_a = n // pow(B,i)
		a.append(last_a)
		n = n-last_a*pow(B,i)
		# print(last_a, n)
	a.append(n)
	return a
	# [3,2,10]

def pad(m, count):
	return m + count*"a"
