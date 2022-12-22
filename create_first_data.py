import pyAesCrypt, os
email = "demo@demo.com"
pyAesCrypt.encryptFile("loginlist/" + email + ".jpg", "loginlist/" + email + ".crypt", "alicangonullu")
os.remove("loginlist/" + email + ".jpg")
#For decrypt : pyAesCrypt.decryptFile("loginlist/" + email + ".crypt", "loginlist/" + email + ".jpg", "alicangonullu")