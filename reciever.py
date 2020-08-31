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



def readCipherText():
	global cipher_path
	data = ""
	with open(cipher_path, "r") as file:
		data = file.read().replace('\n', ' ')
		return data


def recieveMsg(u2, u1):
	# print(u1, u2)
	print("Cipher file is reading")
	data = readCipherText()

	# Vkey_len_word =  num2word(Vkey_len)


	u2_d, u2_n = getUserPrivateKey(u2)
	u1_e, u1_n = getUserPublicKey(u1)


	DM = rsaDecrypt(data, u2_d, u2_n)
	print("Decrypted with reciever's private key")

	M = rsaDecrypt(DM, u1_e, u1_n)
	print("Decrypted with sender's public key")

	with open("RecieverVignere", "w") as file:
		file.write(M)

	Vkey_len_word, Vkey, Vcipher = M.split("{")
	print("Vignere Key and Vgnere Cipher extracted")

	Vdec = Vdecrypt(Vcipher, Vkey)
	print("Vignere Cipher decrypted")

	with open("decrypted_vignere_key", "w") as file:
		file.write(Vkey)

	with open("decrypted_message", "w") as file:
		file.write(Vdec)

	print("Decrypted text is saved to file")
	print("Decrypted key is saved to file")

	return True




def init():
	
	print("Recieving message...")
	recieveMsg(2,1)
	print("Recieving Completed")
	print("_"*30)



cipher_path = "cipher"

if __name__ == "__main__":
	cipher_path = sys.argv[1]
	init()



# print(sendMsg(1,2))
# print(recieveMsg(2,1))