from Crypto.Hash import SHA256
from Crypto.Cipher import AES
import os, random, sys, pkg_resources

###################################################
#PyCrypto is a python packacge which is used for performing crptographic function
#It is capable of performing symmetric and asymmetric encryption

# Advanced Encryption Standard (AES) - Symmetric cipher, 128 bit block size
# keys can be 128,192 and 256 bit long

# Initialization Vector (IV) - used to produce distinct ciphertext
# Avoid using same IV and same key for encrypting different datasets as it becomes predictable

####################################################


#Skey is the symmetric key which will be used for encryption and decryption of the file
#filename contains the name of the file which need to be encryted or decrypted 
#Performs encryption method
def encrypt(Skey, filename):
	chunksize = 64 * 1024
    #adds (protected) at the beginning of the filename to show that the file is encrypted
	outFile = os.path.join(os.path.dirname(filename), "(protected)"+os.path.basename(filename))
	filesize = str(os.path.getsize(filename)).zfill(16)
    #Initialization Vector (IV)
	IV = ''

	for i in range(16):
		IV += chr(random.randint(0, 0xFF))
	
	encryptor = AES.new(key, AES.MODE_CBC, IV)

	with open(filename, "rb") as infile:
		with open(outFile, "wb") as outfile:
			outfile.write(filesize)
			outfile.write(IV)
			while True:
				chunk = infile.read(chunksize)
				
				if len(chunk) == 0:
					break

				elif len(chunk) % 16 !=0:
					chunk += ' ' *  (16 - (len(chunk) % 16))

				outfile.write(encryptor.encrypt(chunk))

#Performs decryption
def decrypt(Skey, filename):
	outFile = os.path.join(os.path.dirname(filename), os.path.basename(filename[11:]))
	chunksize = 64 * 1024
	with open(filename, "rb") as infile:
		filesize = infile.read(16)
		IV = infile.read(16)

		decryptor = AES.new(key, AES.MODE_CBC, IV)
		
		with open(outFile, "wb") as outfile:
			while True:
				chunk = infile.read(chunksize)
				if len(chunk) == 0:
					break

				outfile.write(decryptor.decrypt(chunk))

			outfile.truncate(int(filesize))
	
def allfiles():
	allFiles = []
	for root, subfiles, files in os.walk(os.getcwd()):
		for names in files:
			allFiles.append(os.path.join(root, names))

	return allFiles

print "Do you want to Encrypt(E) or Decrypt(D) the file?"	
choice = raw_input("Press E or D")
password = raw_input("Enter the key/password: ")

encFiles = allfiles()

if choice == "E":
	for Tfiles in encFiles:	
		if os.path.basename(Tfiles).startswith("(protected)"):
			print "%s is already encrypted" %str(Tfiles)
			pass

		elif Tfiles == os.path.join(os.getcwd(), sys.argv[0]):
			pass 
		else:
			encrypt(SHA256.new(password).digest(), str(Tfiles))
			print "Done encrypting %s" %str(Tfiles)
			os.remove(Tfiles)


elif choice == "D":
	filename = raw_input("Enter the filename to decrypt: ")
	if not os.path.exists(filename):
		print "No such file exists"
		sys.exit(0)
	elif not filename.startswith("(protected)"):
		print "%s is not encrypted" %filename
		sys.exit()
	else:
		decrypt(SHA256.new(password).digest(), filename)
		print "Done decrypting %s" %filename
		os.remove(filename)

else:
	print "Please choose a valid command!"
	sys.exit()