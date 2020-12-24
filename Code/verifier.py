# first of all import the socket library 
import socket, RSA, datetime 
import hashlib
from fpdf import FPDF
# 9060 for communication with Public Key Distribution Authority
# 10030 for communication with client A
# 7090 for exchanging replies with A
IP = '127.0.0.1'
#credentials of A
PU_key_A = -1
ID_A = -1

PU_key_student = 182106040449176377254583258871575511

PU_key_director = 182106040449176377254583258871575613
PU_key_registrar = 117477982670003491925783789957926211

#credentials of verifier
PR_key_verifier = 117477982670003491925783789957926129
PU_key_verifier = 154234236513598500833278601624812369
mod = 471884124816129030187874111122712531


if __name__ == "__main__":
	soc = socket.socket()          
	soc.bind(('', 10030))         
	 
	soc.listen()      
	print ("Socket is now listening")            

	print()
	con, address = soc.accept()      
	print ('Successful connection with student')

	reply_student_info = RSA.decrypt(con.recv(1024).decode(), mod, PR_key_verifier)
	req = reply_student_info.split("||") #split into list of parameters sent
	print()
	print("student info received from student : ",req)
	print()

	reply_watermark = RSA.decrypt(con.recv(1024).decode(), mod, PR_key_verifier)
	print()
	print("watermark received from student : ",reply_watermark)
	print()

	reply_director_sign = con.recv(1024).decode()
	reply_director_sign = RSA.decrypt(reply_director_sign,mod,PR_key_verifier)
	print()
	print("Received Director's signature : ",reply_director_sign)
	print()

	reply_registrar_sign = con.recv(1024).decode()
	reply_registrar_sign = RSA.decrypt(reply_registrar_sign,mod,PR_key_verifier)
	print()	
	print("Received Registrar's signature : ",reply_registrar_sign)
	print()


	pdf = FPDF('L','mm','A4')
	# Add a page
	pdf.add_page(orientation='L')
	pdf.set_auto_page_break(0)
	
	timeStamp = req[4]
	i=0
	while(i<22):
		if i == 7:
			pdf.set_font("Times",size=20,style='b')
			pdf.cell(200, 10, txt="Certificate Of Graduation", ln=i, align='C')

		elif i == 8:
			pdf.set_font("Courier", size=15, style='b')
			pdf.cell(200, 5, txt="IIITD", ln=i, align='C')

		elif i == 9:
			pdf.set_font("Arial", size=10, style='b')
			pdf.cell(200, 10, txt="Name of the Student : "+req[0], ln=i, align='L')

		elif i == 10:
			pdf.set_font("Arial", size=10, style='b')
			pdf.cell(200, 10, txt="Roll No. : "+req[1], ln=i, align='L')

		elif i == 11:
			pdf.set_font("Arial", size=10, style='b')
			pdf.cell(200, 10, txt="Pin Code : "+req[2], ln=i, align='L')

		elif i == 12:
			pdf.set_font("Arial", size=15, style='b')
			pdf.cell(200, 10, txt=req[3], ln=i, align='C')

		elif i == 13:
			pdf.set_font("Arial", size=10, style='b')  
			pdf.cell(200, 10, txt="Date & Time- ", ln=i, align='L')

		elif i == 14:
			pdf.set_font("Arial", size=15, style='b')   
			pdf.cell(200, 10, txt=timeStamp, ln=i, align='L')

		elif i==15:
			pdf.set_font("Arial", size=15, style='b')
			pdf.cell(200, 10, txt="Director's Signature - ", ln=i, align='L')

		elif i==16:
			pdf.set_font("Arial", size=6, style='b')
			pdf.cell(200, 10, txt=reply_director_sign, ln=i, align='L')

		elif i==17:
			pdf.set_font("Arial", size=15, style='b')
			pdf.cell(200, 10, txt="Registrar's Signature - ", ln=i, align='L')
		elif i==18:
			pdf.set_font("Arial", size=6, style='b')
			pdf.cell(200, 10, txt=reply_registrar_sign, ln=i, align='L')	
		elif i==19:
			pdf.set_font("Arial", size=15, style='b')
			pdf.cell(200, 10, txt="Digital Watermark - ", ln=i, align='L')
		elif i==20:
			pdf.set_font("Arial", size=8, style='b')
			pdf.cell(200, 10, txt=reply_watermark, ln=i, align='L')

		else:
			pdf.set_font("Arial", size=2, style='b')
			pdf.cell(200, 10, txt="", ln=i, align='C')
		i+=1

	pdf.image('iiitd_image.png', x=10, y=8, w=100)
	name = req[0] + "_" + req[1] + "_"+req[2]+"_verify.pdf"
	pfile = pdf.output(name)


	con.close() 
	soc.close()

	################ Connecting with student again
	soc = socket.socket()
	soc.connect((IP, 7090))

	print("generating the hash value for the student certificate info to verify the signatures")
	hash_message = hashlib.sha256(reply_student_info.encode())
	hash_message = str(hash_message.hexdigest()) 
	print("hash message at verifier side",hash_message)

	director_hash = RSA.decrypt(reply_director_sign,mod,PU_key_director)
	registrar_hash = RSA.decrypt(reply_registrar_sign,mod,PU_key_registrar)

	if(director_hash==registrar_hash):
		if(director_hash==hash_message):
			encrypted_message = RSA.encrypt("Document is verified Successfully..........",mod,PU_key_student)
			soc.send(str.encode(encrypted_message))
		else:
			encrypted_message = RSA.encrypt("Document is not verified Successfully!!!! Ceritificate has is not matching.....",mod,PU_key_student)
			soc.send(str.encode(encrypted_message))
	else:
		encrypted_message = RSA.encrypt("Document is not verified Successfully!!! Director's and Registra's sign is not matching......",mod,PU_key_student)		
		soc.send(str.encode(encrypted_message))

	soc.close()	







	# # ID_A = reply_from_A[0]
	# # nonceA = int(reply_from_A[1])

	# print('Request from A is received')
	# print ("ID of A: " + str(ID_A) + "  Nonce received: " + str(nonceA) + "\n\n")
	# # Close the connection with the A 
	# con.close() 
	# soc.close()

	# soc = socket.socket()          
	
	# send_time = datetime.datetime.now()
	# message = 'Key request for client A' + '||' + str(send_time)
	# # Connection request of A
	# soc.connect((IP, 9060))
	# soc.send(str.encode(message))
	# print("Message from client B to PKDA: " + message)

	# reply = RSA.decrypt(soc.recv(1024).decode(), mod, PU_key_pkda).split("||")
	# print("\n\n" + str(reply) + '\n\n')
	# receive_time = datetime.datetime.strptime(reply[2], '%Y-%m-%d %H:%M:%S.%f') #formatting the date

	# diff = receive_time - send_time
	# if(diff.total_seconds() <= 1):
	# 	print("message is received within time")
	# else:
	# 	print("message is NOT received within time")

	# print("Message received from PKDA: "+ str(reply))
	# print ('Public key of A received from PKDA: ', int(reply[0]))
	# soc.close()

	# # Connecting with A again
	# soc = socket.socket()
	# soc.connect((IP, 7090))
	# # Talking to A
	# print('Sending confirmation/reply to A...')

	# import random
	# nonceB = random.randint(10**10, 10**15)

	# soc.send(RSA.encrypt(str(nonceA) + '||' + str(nonceB), mod, int(reply[0])).encode())

	# reply_from_A = (RSA.decrypt(soc.recv(1024).decode(), mod, PR_key)).split("||")
	
	# print ('\n Received confirmation of A', reply_from_A)

	# if(int(reply_from_A[0]) == nonceB):
	# 	print("Nonce sent is equal to nonce received")
	# else:
	# 	print("Nonce sent is not equal to nonce received")
		

	# i=0
	# while i < 3:
	# 	print("Message from A: " + RSA.decrypt(soc.recv(1024).decode(), mod, PR_key))
	# 	soc.send(RSA.encrypt('Got it ' + str(i + 1), mod, int(reply[0])).encode())
	# 	i+=1
	# soc.close()