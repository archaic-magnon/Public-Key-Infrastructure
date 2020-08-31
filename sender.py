import gmpy2 as gmp
from gmpy2 import mpz
from Vig import *
from RSAEnc import *
from RSADec import *
from numNwords import *
import os, sys



def getCAPublicKey():
	with open("ca_public") as fp: 
		lines = fp.readlines() 
		line = lines[0]
		e,n = line.split()
		return mpz(e), mpz(n)



def getUserPublicKey(user):

	E, N = getCAPublicKey()

	with open("pub_dir") as fp: 
		lines = fp.readlines() 
		for line in lines: 
			u, enc_e, enc_n = line.split()

			u = int(u)
			enc_e = mpz(enc_e)
			enc_n = mpz(enc_n)
			if user == u:
				e = gmp.powmod(enc_e, E, N)
				n = gmp.powmod(enc_n, E, N)

				return (e, n)
	print(f"user {user} doesn't exist")
	return False


def getUserPrivateKey(user):
	file_name = str(user) + "_private"
	with open(file_name) as file: 
		data = file.read()
		
		d, n = data.split()
		return mpz(d),mpz(n)

def readPlainText():
	global plain_path
	data = ""
	plain = ""
	with open(plain_path, "r") as file:
		data = file.read().replace('\n', ' ').lower()
		
		for el in data:
			if ord('a') <= ord(el) <= ord('z'):
				plain+= el

	return plain



def getVigKey(path="vig_key"):
	global key_path
	with open(key_path, "r") as file:
		data = file.read().replace('\n', ' ')
		return data

def sendMsg(u1, u2):
	# print(u1, u2)

	print("Reading Plain Text file...")
	data = readPlainText()
	print("Reading Vignere Key file...")
	Vkey = getVigKey()


	u1_d, u1_n = getUserPrivateKey(u1)
	u2_e, u2_n = getUserPublicKey(u2)

	v_data = Vencrypt(data, Vkey)
	print("File encrypted with Vignere Cipher")

	Vkey_len = len(Vkey)
	Vkey_len_word =  num2word(Vkey_len)

	# message M before sending
	M = Vkey_len_word + "{" + Vkey + "{" + v_data
	print("Key length, Vignere Key and Vignere Cipher is appended")

	DS_M =  rsaEncrypt(M, u1_d, u1_n)
	print("Digital Signature is generated using sender's private key")

	with open("SenderVignere", "w") as file:
		file.write(M)

	# encrypt using rsa
	# print("u2_n", u2_n)
	C = rsaEncrypt(DS_M, u2_e, u2_n)
	print("Encrypted with reciever's public key")

	with open("cipher", "w") as file:
		file.write(C)

	print("Cipher Text is written to file")
	return True





def init():
	print("Sending message...")
	sendMsg(1,2)
	print("Sending Completed")
	print("_"*30)

plain_path = "plain"
key_path = "vig_key"

if __name__ == "__main__":
	plain_path = sys.argv[1]
	key_path = sys.argv[2]
	init()


# print(sendMsg(1,2))
# print(recieveMsg(2,1))