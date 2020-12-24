#p = 664191324980996971
#q = 710464149512386361 
#mod = 471884124816129030187874111122712531
import gmpy2

def encrypt(msg, mod, e):
	#converting string characters to binary plaintext 
	plaintext = ''
	plaintext = make_binary(plaintext,msg)
	window_length = 100 # size of window from the binary plaintext

	rem = len(plaintext) % window_length
	j=0
	plaintext += '1'
	while j< window_length - rem : 
		plaintext+='0'
		j+=1
	
	return get_cipher(plaintext,window_length,e,mod)

def make_binary(plaintext,msg):
	i=0
	while i < len(msg): # for every character
		b = bin(ord(msg[i]))[2:] #convert to binary
		# b = '0'*(8-len(b)) + b
		c = ''
		for j in range(8-len(b)):
			c += '0'
		b= c+b
		#  #filling up zeroes in the front (to make an 8 bit binary number)
		plaintext += b #concatenate to the final plaintext
		i+=1
	return plaintext

def get_cipher(plaintext, window_length, e, mod):
	cipher=''
	num_blocks = int(len(plaintext) / window_length)
	i=0
	while i < num_blocks:
		cipher += str(gmpy2.powmod(int(plaintext[i * window_length : (i + 1) * window_length],2),e,mod)) + ' '
		i+=1
	return cipher

def decrypt(msg, mod, d):
	
	msg = list(map(int, msg.rstrip(' ').split()))
	
	ciphertext = convert(msg,mod,d)

	ciphertext = ciphertext.rstrip('0')[:len(ciphertext) - 1]
	
	
	return get_plaintext(ciphertext)

def convert(msg,mod, d,):
	ciphertext = ''
	window_length = 100
	i=0
	while i < len(msg):
		c = bin(gmpy2.powmod(msg[i],d,mod))[2:]
		x = ''
		for j in range(window_length - len(c)):
			x+='0'
		c = x + c
		ciphertext += c
		i+=1
	return ciphertext
def get_plaintext(ciphertext):
	plaintext = ''
	num_chars = int(len(ciphertext) / 8)
	i = 0
	while i < num_chars:
		plaintext += chr(int(ciphertext[i * 8 : (i + 1) * 8],2))
		i+=1
	return plaintext