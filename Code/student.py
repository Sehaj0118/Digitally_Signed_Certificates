#import statements for socket and RSA
import socket
import RSA
from fpdf import FPDF

#importing datetime for sending timestamps
import datetime
# import gmpy2
# 9060 for communication with Public Key Distribution Authority
# 10030 for communication with client B
# 7090 for exchanging replies with B

IP = '127.0.0.1'
#credentials for the student (updated) 
PU_key = 182106040449176377254583258871575511
PR_key= 710464149512386391
mod = 471884124816129030187874111122712531
id_A = 1

#credentials for PKDA
# PU_key_pkda = 182106040449176377254583258871575613

PU_key_verifier = 154234236513598500833278601624812369

#credentials of client B not known

#### name, roll number, GMT time(from server side)


if __name__ == "__main__":
	soc = socket.socket()
	soc.connect((IP,9060))
	name = input("Enter your name = ")
	roll_number = input("Enter your roll number = ")
	pin_code = input("Enter your pin code = ")
	msg = "certificate request from server" + "||" + name+"||"+roll_number+"||"+pin_code
	print()
	print("Message from student to server: " + msg)
	encrypted_message = RSA.encrypt(msg,mod,PR_key) ### encrypting the msg with the private key of student	
	soc.send(str.encode(encrypted_message))

	reply_student_info = soc.recv(1024).decode()
	if reply_student_info == "Your credentials are not in our database......":
		print(reply_student_info)
		quit()

	reply_student_info = RSA.decrypt(reply_student_info,mod,PR_key)
	req = reply_student_info.split("||")
	print()
	print("Received student info")
	for i in req:
		print(i)
	print()	

	reply_watermark = soc.recv(1024).decode()
	reply_watermark = RSA.decrypt(reply_watermark,mod,PR_key)	
	print()

	print("Received Director's signature")
	reply_director_sign = soc.recv(1024).decode()
	reply_director_sign = RSA.decrypt(reply_director_sign,mod,PR_key)
	print(reply_director_sign)
	print()


	print("Received Registrar's signature")	
	reply_registrar_sign = soc.recv(1024).decode()
	reply_registrar_sign = RSA.decrypt(reply_registrar_sign,mod,PR_key)
	print(reply_registrar_sign)
	print()

	##################################         crtificate file code needs to be inserted here  ###################################

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

	pdf.image('iiitd_image.png', x=10, y=8, w=70)
	name = req[0] + "_" + req[1] + "_"+req[2]+".pdf"
	pfile = pdf.output(name)

	# # Now, send message to B
	soc = socket.socket()
	soc.connect((IP, 10030))
	print('Now Sending certificate to verifier... \n\n')

	encrypted_message = RSA.encrypt(reply_student_info,mod,PU_key_verifier)
	# print('student info with gmt being sent from student to verifier: ', encrypted_message)
	soc.send(str.encode(encrypted_message))	
	print()
	# soc.send(str.encode(RSA.encrypt(str(id_A) + '||' + str(nonce), mod, PU_key_B)))

	encrypted_message = RSA.encrypt(reply_watermark,mod,PU_key_verifier)
	# print('student info with gmt being sent from student to verifier: ', encrypted_message)
	soc.send(str.encode(encrypted_message))	
	print()

	director_signature = RSA.encrypt(reply_director_sign,mod,PU_key_verifier)  
	# print('director signature being sent from student to verifier: ', director_signature)
	soc.send(str.encode(director_signature))
	print()

	registrar_signature = RSA.encrypt(reply_registrar_sign,mod,PU_key_verifier)  
	# print('registrar signature being sent from student to verifier: ', registrar_signature)
	soc.send(str.encode(registrar_signature))	
	print()
	# con.close()
	soc.close()

	######### Checking for a response from verifier

	soc = socket.socket()
	soc.bind(('', 7090))         
	print ("Socket is now binded to " + str(7090)) 
	soc.listen()      
	print ("Socket is now listening")            
	con, address = soc.accept()      
	print()
	print ('Successful connection with verifier') 
	print ('Reply from verifier is received')
	reply_from_verifier = RSA.decrypt(con.recv(1024).decode(), mod, PR_key) 
	print()
	print(reply_from_verifier)
	print()

	con.close()
	soc.close()
