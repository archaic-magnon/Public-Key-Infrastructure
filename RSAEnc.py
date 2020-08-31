import gmpy2 as gmp
from gmpy2 import mpz
import math
from helper import *
#TODO multiple keylength
# KEY_LENGTH = "TWENTY"
B = 27


def rsaBlockEncrypt(m, e, N):
	# print(m)

	r = len(m)

	m_int = string2int(m)
	m_int.reverse()

	m = sum([el*pow(B,i) for i,el in enumerate(m_int)])
	c = gmp.powmod(m,e,N)

	c_list = int2baseB(c,r)

	c_list.reverse()
	# print(len(c_list))

	return int2string(c_list)


# def simpleRsaEncrypt(k,e,N):
# 	return pow(k,e,N)


def rsaEncrypt(m,e,N):
	# print(m)

	# 26^r < n
	# print(N, B)
	r = int(math.log(N) // math.log(B))
	
	# print(r)
	# print(len(m))
	m = pad(m, r - len(m)%r)

	# print(len(m))

	# divide m into blocks encrypt with rsa

	m_list = [(m[i:i+r]) for i in range(0, len(m), r)]


	encM = "".join([rsaBlockEncrypt(block, e, N) for block in m_list])

	return encM



# print(rsaEncrypt("hellomydearfriend", 3,25777))

# def rsaEncBlock(m, e, N):


# 	m_int = string2int(m)[::-1]
# 	r = len(m)

# 	m = sum([el*pow(B,i) for i,el in enumerate(m_int)])

# 	print(m)

# 	c = pow(m,e,N)

# 	print(c)
	

# 	c_list = int2baseB(c, r)[::-1]
# 	print(c_list)
    

# 	return int2string(c_list)







	# m^e mod n 
	
	# return pow(m,e,n)



# def encrypt(m, N):

# 	# 26^r < n
# 	r = math.log(N) // math.log(B)

# 	m = pad(m, int(len(m)%r))

# 	# divide m into blocks encrypt with rsa

# 	m_list = [(m[i:i+int(r)]) for i in range(0, len(m), int(r))]


# 	encM = "".join([rsaEncBlock(block, 3, N) for block in m_list])

# 	return encM








