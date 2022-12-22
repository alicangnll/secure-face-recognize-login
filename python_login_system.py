import face_recognition, os, pyAesCrypt
from flask import *
from flask import Flask, render_template, request
import base64

app = Flask(__name__)
secret_key = "alicangonullu" # Secret key for decryption

@app.route('/')
def main():
    return render_template("index.html")

@app.route('/login', methods=["POST"])
def face_login():
    image = str(request.form.get("current_image")) #Base64 image from webcam
    email = str(request.form.get("email")) # Email address from database
    
    fh = open("temp.png", "wb")
    fh.write(base64.decodebytes(image.encode('utf-8'))) #Write your temp face file to temp file
    fh.close()

    pyAesCrypt.decryptFile("loginlist/" + email + ".crypt", "loginlist/" + email + ".jpg", secret_key) # Decrypt your verification photo

    yukle_dogrulanacak_resim = face_recognition.load_image_file("temp.png") # Load your temp face file
    yukle_kayitli_resim = face_recognition.load_image_file("loginlist/" + email + ".jpg") # Load your already loaded verification photo

    dogrulanacak_resim_islendi = face_recognition.face_encodings(yukle_dogrulanacak_resim)[0] # Load your temp face file
    kayitli_veri_islendi = face_recognition.face_encodings(yukle_kayitli_resim)[0] # Load your already loaded verification photo

    netice = face_recognition.compare_faces([kayitli_veri_islendi], dogrulanacak_resim_islendi) # Compare both of them

    if(netice[0]):
        verified = "True" # Verified  
    else:
        verified = "False" # Not Verified

    pyAesCrypt.encryptFile("loginlist/" + email + ".jpg", "loginlist/" + email + ".crypt", secret_key) #Encrypt your verification photo
    os.remove("loginlist/" + email + ".jpg") # Cleanup
    os.remove("temp.png") # Cleanup
    return verified

@app.route('/saveimage')
def save():
    return render_template("save.html")

@app.route('/save', methods=["POST"])
def savefile():
    image = str(request.form.get("current_image")) #Base64 image from webcam
    email = str(request.form.get("email")) # Email address from form
    
    fh = open("loginlist/" + email + ".jpg", "wb")
    fh.write(base64.decodebytes(image.encode('utf-8')))# Save your photo
    fh.close()

    pyAesCrypt.encryptFile("loginlist/" + email + ".jpg", "loginlist/" + email + ".crypt", secret_key) # Decrypt your verification photo
    os.remove("loginlist/" + email + ".jpg") # Delete photo
    return "OK"

app.run(host='0.0.0.0', port=81)