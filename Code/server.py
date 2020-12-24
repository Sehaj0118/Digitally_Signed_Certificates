import socket
import hashlib
from time import gmtime
# 9060 is used for communicating with clients

#Credentials of student and verifier
PU_key_student = 182106040449176377254583258871575511
PU_key_verifier = 154234236513598500833278601624812369

### authenticated student data

Dict = {"Dheeraj_2017044":"110062","Sehaj_2017099":"110058"}


#Credentials of director and regitrar
PR_key_director = 154234236513598500833278601624812277
PU_key_director = 182106040449176377254583258871575613

PR_key_registrar = 417941410947963304078191056386622891
PU_key_registrar = 117477982670003491925783789957926211

mod = 471884124816129030187874111122712531 

if __name__ == "__main__":
	soc = socket.socket()          
	print ("Socket has been created")

	soc.bind(('', 9060))         
	print ("Socket is now binded to",str(9060)) 
	
	soc.listen()      
	print ("socket is now listening")            
	
	# Establish connection with A. 
	import RSA
	import datetime

	con, address = soc.accept()

	print ('student is now connected.... ')  	
	req = (con.recv(1024).decode())
	req = RSA.decrypt(req,mod,PU_key_student).split("||")

	name = req[1]+"_"+req[2]
	pin = req[3]

	if name not in Dict or Dict[name]!=pin:
		con.send(str.encode("Your credentials are not in our database......"))
		print()
		print("Credentials are not present in the database......")
	else:		
		final_message = ""
		final_message+=req[1]
		final_message+="||"
		final_message+=req[2]
		final_message+="||"
		final_message+=req[3]
		final_message+="||"
		final_message+="This is to certify that student "+req[1]+" has completed their B.tech from IIITD."
		final_message+="||"	
		t = gmtime()
		timeStamp = str(t.tm_hour) + ":" + str(t.tm_min) + ":" + str(t.tm_sec) + "|" + str(t.tm_mday) + "-" + str(t.tm_mon) + "-" + str(t.tm_year)
		final_message+= timeStamp

		print()
		encrypted_message = RSA.encrypt(final_message,mod,PU_key_student)
		print('student info with gmt being sent from server to student: ', final_message)
		con.send(str.encode(encrypted_message))	

		print()
		# print("final message to be hashed by server = ",final_message)
		hash_message = hashlib.sha256(final_message.encode())
		hash_message = str(hash_message.hexdigest()) 
		# print("hash message from server",hash_message)

		print()
		encrypted_message = RSA.encrypt(hash_message,mod,PU_key_student)
		print('watermark being sent from server to student: ', hash_message)
		con.send(str.encode(encrypted_message))	

		print()
		director_signature = RSA.encrypt(hash_message,mod,PR_key_director)  ### encrypting the hash wih director's PR key
		# print("director's signature on student certificate",director_signature)

		# director_signature = RSA.decrypt(director_signature,mod,PU_key_director)
		# print("director's signature on student certificate",director_signature)	

		print()
		encrypted_message = RSA.encrypt(str(director_signature),mod,PU_key_student)
		print('director signature being sent from server to student: ', director_signature)
		con.send(str.encode(encrypted_message))	

		registrar_signature = RSA.encrypt(hash_message,mod,PR_key_registrar) ### encrypting the hash wih registrar's PR key
		# print("registrar's signature on student certificate",registrar_signature)

		print()
		encrypted_message = RSA.encrypt(str(registrar_signature),mod,PU_key_student)
		print('ragistrar signature being sent from server to student: ', registrar_signature)
		con.send(str.encode(encrypted_message))

	con.close()
	soc.close()

	# registrar_signature = RSA.decrypt(registrar_signature,mod,PU_key_registrar)
	# print("registrar's signature on student certificate",registrar's_signature)	

	# print(hash_message==director_signature)
	# print(hash_message==registrar_signature)

	# final_message="||"+director_signature+"||"+registrar_signature


