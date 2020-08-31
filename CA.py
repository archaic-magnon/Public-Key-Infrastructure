import gmpy2 as gmp
from gmpy2 import mpz
import random
import os


# random_state(...) random_state([seed]) returns a new object containing state information for the random number
# generator. An optional integer argument can be specified as the seed value. Only the Mersenne Twister random
# number generator is supported.

# mpz_rrandomb(...) mpz_rrandomb(random_state, b) returns a random integer between 0 and 2**b - 1 with long
# sequences of zeros and one in its binary representation. The parameter random_state must be created by random_state() first


# next_prime(...) next_prime(x) returns the next probable prime number > x

def StrongPrime(p1,p2,p3):
	bit_count = 512
	if(len(p2)!=512):
		return False
	return  p2 > ((p1+p3)/2) 

def getRandomSeed():
	return random.randrange(100) + random.randrange(100) + 1

def getNextPrime(n):
	return gmp.next_prime(n)

def getStrongPrime():
	bit_count = 512

	rand_state = gmp.random_state(getRandomSeed())
	rand_no = gmp.mpz_rrandomb(rand_state, bit_count)
	p1 = getNextPrime(rand_no)
	p2 = getNextPrime(p1)
	p3 = getNextPrime(p2)
	while(not StrongPrime(p1,p2,p3)):
		rand_state = gmp.random_state(getRandomSeed())
		rand_no = gmp.mpz_rrandomb(rand_state, bit_count)
		p1 = getNextPrime(rand_no)
		p2 = getNextPrime(p1)
		p3 = getNextPrime(p2)    
	return p2


def getRandomPrime():
	bits = random.randrange(5,100)
	rand_state = gmp.random_state(getRandomSeed())
	rand_no = gmp.mpz_rrandomb(rand_state, bits)
	return getNextPrime(rand_no)


def getRandomNumber():
	return random.randrange(10e15) + random.randrange(10e15) + 3


# def getInverseMod(a,m):
# 	try:
# 		d = gmp.invert(e, phi_n)
# 		return d
# 	except:

# def inverseExist(e, phi_n):
# 	try:
# 		d = gmp.invert(e, phi_n)
# 		return True
# 	except:
# 		return False


def genkeyPair():
	p = getStrongPrime()
	q = getStrongPrime()
	n = p*q

	phi_n = (p-1)*(q-1)


	e = getRandomPrime()
	while  gmp.gcd(e, phi_n) != 1:
		e += 2


	d = gmp.invert(e, phi_n)

	public_key = (e, n)
	private_key = (d, n)

	return (e,d,n)

def saveFile(file_name, data, mode):
	with open(file_name, mode) as myfile:
		myfile.write(data)
		myfile.write("\n")

def setupCA():
	e,d,n = genkeyPair()
	
	public_key = str(e) + " " + str(n)
	private_key	= str(d) + " " + str(n)
	saveFile("ca_public", public_key, "w")
	saveFile("ca_private", private_key, "w")
	return d, n


def setupPublicKeyDirectory(D, N):
	user_count = 2
	is_restart_ca = False

	if os.path.exists("pub_dir"):
		os.remove("pub_dir")



	for i in range(1, user_count+1):
		e,d,n = genkeyPair()

		try_count = 0
		try_max = 100
		while n > N or gmp.powmod(n, D, N) == 0:
			try_count+=1
			if(try_max > 200):
				is_restart_ca = True
				break
			e,d,n = genkeyPair()

		if is_restart_ca:
			break

		user_name = str(i)
		# store ith user name
		enc_e = gmp.powmod(e, D, N)
		enc_n = gmp.powmod(n, D, N)

		public_key = user_name + " " + str(enc_e) + " " + str(enc_n)
		private_key	= str(d) + " " + str(n)

		saveFile("pub_dir", public_key, "a+")
		saveFile(user_name+"_private", private_key, "w")

		print(f"user: {user_name} CA public key / private key generated")

	if is_restart_ca:
		restartCA()


def restartCA():
	print("public key / private key generation failed: CA is restarting")
	startCA()

def startCA():
	D, N = setupCA()
	print("CA public key / private key generated")

	setupPublicKeyDirectory(D, N)
	print("Public key directory generated, encrypted with CA private key: pub_dir")



print("_"*30)
print("CA setup is starting...")

startCA()

print("CA setup done")
print("_"*30)


