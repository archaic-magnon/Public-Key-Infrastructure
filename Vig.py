import time
from helper import *

def Vencrypt(data, key):
	data = string2int(data)
	key = string2int(key)
	m = len(key)
	enc = [(el +  key[idx%m])%26 for idx, el in enumerate(data)]
	return int2string(enc)


def Vdecrypt(data, key):
	data = string2int(data)
	key = string2int(key)
	m = len(key)
	enc = [(el -  key[idx%m])%26 for idx, el in enumerate(data)]
	return int2string(enc)


# text = ['a']*1000000

# b = "".join(text)

# key = "abcd"

# s = time.time()
# Vdecrypt(Vencrypt(text, key), key)
# print(time.time() - s)