import gmpy2 as gmp
from gmpy2 import mpz
from Vig import *
from RSAEnc import *
from RSADec import *
from numNwords import *
import CA
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
	data = ""
	plain = ""
	with open("plain", "r") as file:
		data = file.read().replace('\n', ' ').lower()
		
		for el in data:
			if ord('a') <= ord(el) <= ord('z'):
				plain+= el

	return plain

def readCipherText():
	data = ""
	with open("cipher", "r") as file:
		data = file.read().replace('\n', ' ')
		return data



def getVigKey():
	with open("vig_key", "r") as file:
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


def main():
	init()



def init():

	print("Sending message...")
	sendMsg(1,2)
	print("Sending Completed")
	print("_"*30)

	print("Recieving message...")
	recieveMsg(2,1)
	print("Recieving Completed")
	print("_"*30)




init()


# print(sendMsg(1,2))
# print(recieveMsg(2,1))