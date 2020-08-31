import gmpy2 as gmp
from gmpy2 import mpz
import math
from helper import *

#TODO multiple keylength
# KEY_LENGTH = "TWENTY"
B = 27


def rsaBlockDecrypt(c,d,N):
    r = len(c)-1
    c_int = string2int(c)
    c = sum([el*pow(B,i) for i,el in enumerate(c_int)])
    m = gmp.powmod(c,d,N)
    
    m_list = int2baseB(m, r-1)
    
    return int2string(m_list)
    
      
def simpleRsaDecrypt(k,d,N):
	return pow(k,d,N)



def rsaDecrypt(c,d,N):
	# 26^r < n
	r = int(math.log(N) // math.log(B)) + 1


	# divide m into blocks encrypt with rsa

	c_list = [(c[i:i+r]) for i in range(0, len(c), r)]


	decM = "".join([rsaBlockDecrypt(block, d, N) for block in c_list])

	return decM


# print(rsaDecrypt("iibafsgbwlpaheibzjhbxagaaa",16971, 25777))


# def rsaDecBlock(m, e, N):
# 	# m:string
# 	m_int = string2int(m)
# 	r = math.log(N) // math.log(B)

# 	m = sum([el*pow(B,i) for i,el in enumerate(m_int)])

# 	print(m)

# 	c = pow(m,e,N)

# 	print(c)
	

# 	c_list = int2baseB(c, r)
# 	print(c_list)
    

# 	return int2string(c_list)
