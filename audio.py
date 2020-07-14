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
        
        # incomplete
        else:
            self.info = []
            words = []
            with open(self.infofile, "r") as f1:
                lines = f1.readlines()
            
            for line in lines:
                words_in_line = line.split()
                self.info.append(line)
                print(words_in_line)
            print(self.info, type(self.info))
            # t = ''.join(str(ord(c)) for c in self.info)
            # print(t)

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
            enc_wav += [d1,d2,d3]
            i+=3
        enc_wav = np.asarray(enc_wav,dtype='int16')
        self.end_index = i
        return np.concatenate((enc_wav,self.hideout_lin[i:]))


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
            pass

# try:
#     pic_file, aud_file = sys.argv[1], sys.argv[2]
# except:
#     print("usage :  python   audio_steg.py    pic-to-hide.jpg/png     audio-to-hide-pic-in.wav")
#     sys.exit(2)

a_obj = Audio("cloudimg.jpeg", "image", "avicii.wav")
# a_obj = Audio("secret.txt", "text", "avicii.wav")
a_obj.read_audio_hideout()
a_obj.read_info()
a_obj.hide_info()
a_obj.decode_data("encoded.wav", "image")
# a_obj.decode_data("encoded.wav", "text")