from flask import Flask, render_template, request, send_file
import os
from audio import Audio
from image import Image
from datetime import datetime

app = Flask(__name__)
img_formats = ["png", "jpg", "jpeg"]

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/encode', methods = ['POST'])
def encode():
   delete_old_files()
   # check if wav or imf file --- incomplete
   if request.method == 'POST': 
      
      # file upload
      f1 = request.files['f1']  
      f2 = request.files['f2']  
      f1.save(os.path.join("uploads",f1.filename))
      f2.save(os.path.join("uploads",f2.filename))

      if f1.filename.split(".")[1] == "wav":
         audio = Audio()
         audio.hideout_file = "./uploads/"+f1.filename
         audio.infofile = "./uploads/"+f2.filename
         if f2.filename.split(".")[1] in img_formats:
            audio.infotype = "image"
         else:
            audio.infotype = "text"
         
         audio.read_audio_hideout()
         audio.read_info()
         fn = audio.hide_info()

         os.remove("uploads/"+f1.filename)
         os.remove("uploads/"+f2.filename)

         if fn == "SizeError":
            return render_template("index.html",key="Secret File too large to be hidden in given Audio/Image file", file2down=fn)   
         
         return render_template("index.html",key=audio.decodekey, file2down=fn)
      
      elif f1.filename.split(".")[1] in img_formats:
         image = Image()
         image.hideout_file = "./uploads/"+f1.filename
         image.infofile = "./uploads/"+f2.filename
         image.read_info()
         fn = image.hide_info()

         os.remove("uploads/"+f1.filename)
         os.remove("uploads/"+f2.filename)

         if fn == "SizeError":
            return render_template("index.html",key="Secret File too large to be hidden in given Media file", file2down=fn) 

         return render_template("index.html",key=image.end_pixel, file2down=fn)
         
   return "Error"


@app.route('/download', methods = ['POST'])
def download():
   if request.method == 'POST':
      fn = request.form["fn2down"]
      return send_file("uploads/"+fn, as_attachment=True)


@app.route('/decode', methods = ['POST'])
def decode():
   delete_old_files()
   audio = Audio()
   image = Image()

   if request.method == 'POST': 
      # file upload
      f1 = request.files['f1']  
      f1.save(os.path.join("uploads",f1.filename))
      key = request.form["dec_key"]
      
      if f1.filename.split(".")[1] == "wav":
         audio = Audio()
         fn = audio.decode_data("./uploads/"+f1.filename, key)
      
      elif f1.filename.split(".")[1] in img_formats:
         image = Image()
         fn = image.decode_data("./uploads/"+f1.filename, int(key))
      
      return send_file("uploads/"+fn, as_attachment=True)

   return "error"


def delete_old_files():
   
   files = os.listdir("uploads/")
   print(files)
   for f in files:
      ts = os.path.getmtime("uploads/"+f)
      d = datetime.fromtimestamp(ts).strftime("%H:%M:%S")
      d = datetime.strptime(d,"%H:%M:%S")
      now = datetime.now().strftime("%H:%M:%S")
      now = datetime.strptime(now,"%H:%M:%S")

      if (now - d).total_seconds() > 150:
         os.remove("uploads/"+f)
         print("deleted : ",f)

if __name__ == '__main__':
   app.run(debug = True)