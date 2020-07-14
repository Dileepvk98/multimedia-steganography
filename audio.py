from scipy.io import wavfile
import numpy as np
import cv2, sys

class Audio:
    def __init__(self, infofile, infotype, aud_file):
        self.hideout_file = aud_file
        self.hideout = None
        # self.width = None
        # self.height = None
        self.hideout_lin = None
        self.rate = None

        self.infotype = infotype
        self.infofile = infofile
        self.info = None
        self.info_lin = None
        self.end_index = 0;

    def read_audio_hideout(self):
        self.rate, self.hideout = wavfile.read(self.hideout_file)
        # self.width = self.hideout.shape[0]
        # self.height = self.hideout.shape[1]
        self.hideout_lin = self.hideout.reshape(-1)

    def read_info(self):
        if self.infotype == "image":
            self.info = cv2.imread(self.infofile,1)
            self.info_lin = self.info.reshape(-1)
        
        else:
            self.info = []
            with open(self.infofile, "r") as f1:
                data = f1.readlines()
            self.info_lin = self.text_formatter(data)


    def text_formatter(self, data):
        # print(data)

        lines = []
        for line in data:
            words = line.replace("\n","~").split()
            lines.append(words)
        # print(lines)  
        
        words_ascii = []
        for line in lines:
            for word in line:
                for c in word:
                    words_ascii.append(ord(c))
                if ord(c) != ord('~'):
                    words_ascii.append(ord(' '))
        # print(words_ascii)
        return words_ascii
    

    def hide_info(self):
        enc_wav, i = [], 0
        print("encoding...")
        for sub_pixel_ascii in self.info_lin:
            d1, d2, d3 = int(self.hideout_lin[i]/10)*10, int(self.hideout_lin[i+1]/10)*10, int(self.hideout_lin[i+2]/10)*10

            if d1<0:
                d1-=int(sub_pixel_ascii/10/10)%10
            else:
                d1+=int(sub_pixel_ascii/10/10)%10
            if d2<0:
                d2-=int(sub_pixel_ascii/10)%10
            else:
                d2+=int(sub_pixel_ascii/10)%10
            if d3<0:
                d3-=sub_pixel_ascii%10
            else:
                d3+=sub_pixel_ascii%10

            if d1 <= -32768:
                d1+=10
            if d2 <= -32768:
                d2+=10
            if d3 <= -32768:
                d3+=10
            # print(d1, d2, d3)
            enc_wav += [d1,d2,d3]
            i+=3
        enc_wav = np.asarray(enc_wav,dtype='int16')
        self.end_index = i
        # return np.concatenate((enc_wav,self.hideout_lin[i:]))
        enc_wav = np.concatenate((enc_wav,self.hideout_lin[i:]))
        enc_wav = enc_wav.reshape(self.hideout.shape[0], self.hideout.shape[1])
        wavfile.write('encoded.wav', self.rate, enc_wav)
        print("encoded")


    def decode_data(self, encoded_file, infotype):
        print("decoding...")
        _, data = wavfile.read(encoded_file)
        data = data.reshape(-1)
        if infotype == "image":
            img, i = [], 0
            while i < self.end_index:
                sub_pixel = abs(data[i])%10*100 + abs(data[i+1])%10*10 + abs(data[i+2])%10
                img.append(sub_pixel)
                i+=3
            # return img
            img = np.asarray(img)
            cv2.imwrite('decoded.png', img.reshape(self.info.shape[0], self.info.shape[1], self.info.shape[2]))

        
        elif infotype=="text":
            text = []
            i = 0
            while i < self.end_index:
                sub_ascii = abs(data[i])%10*100 + abs(data[i+1])%10*10 + abs(data[i+2])%10
                text.append(chr(sub_ascii))
                i+=3
            text = ''.join(text).replace("~","\n")
            print("\ndecoded data :- \n","-"*50,"\n")
            print(text,"\n\n","-"*50,"\n")

try:
    type_of, secret, aud_file = sys.argv[1], sys.argv[2], sys.argv[3]
except:
    print("usage : python audio.py type file-to-hide audio-to-hide-in.wav")
    print("\ttype -> image or text")
    print("\tfile to hide -> .png/jpg/jpeg or .txt/.csv")
    print("\t.wav format necessary as other formats use compression causing loss of data")
    sys.exit(2)


if type_of == "image":
    a_obj = Audio(secret, "image", aud_file)
    a_obj.read_audio_hideout()
    a_obj.read_info()
    a_obj.hide_info()
    a_obj.decode_data("encoded.wav", "image")
elif type_of == "text":
    a_obj = Audio(secret, "text", aud_file)
    a_obj.read_audio_hideout()
    a_obj.read_info()
    a_obj.hide_info()
    a_obj.decode_data("encoded.wav", "text")
else:
    print("invalid type/format")
    exit()