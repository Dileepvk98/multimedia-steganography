from flask import Flask, render_template, request, send_file
import os
from audio import Audio
from image import Image

audio = Audio()
image = Image()

app = Flask(__name__)
img_formats = ["png", "jpg", "jpeg"]

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/encode', methods = ['POST'])
def encode():
   if request.method == 'POST': 
      # file upload
      f1 = request.files['enc_f1']  
      f2 = request.files['enc_f2']  
      f1.save(os.path.join("uploads",f1.filename))
      f2.save(os.path.join("uploads",f2.filename))

      audio.hideout_file = "./uploads/"+f1.filename
      audio.infofile = "./uploads/"+f2.filename
      if f2.filename.split(".")[1] in img_formats:
         audio.infotype = "image"
      else:
         audio.infotype = "text"
      
      audio.read_audio_hideout()
      audio.read_info()
      audio.hide_info()

      return render_template("index.html",key = audio.decodekey)
      # return send_file("uploads/"+audio.decodekey+".wav", as_attachment=True)
      # return audio.decodekey
   return "Error"


@app.route('/download', methods = ['POST'])
def download():
   if request.method == 'POST':
       

if __name__ == '__main__':
   app.run(debug = True)