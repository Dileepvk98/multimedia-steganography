from scipy.io import wavfile
import numpy as np
import cv2, sys, math


class Image:
    def __init__(self, infofile, img_file):
        self.hideout_file = img_file
        self.hideout = None
        self.infotype = "text"
        self.infofile = infofile
        self.info = None
        self.info_lin = None
        self.end_pixel = 0

    def read_info(self):
        if self.infotype == "image":
            self.info = cv2.imread(self.infofile,1)
            # self.width, self.height, self.channel = self.info.shape
            self.info_lin = self.info.reshape(-1)
            # total_pixels = len(lin_img)
        
        else:
            self.info = []
            with open(self.infofile, "r") as f1:
                data = f1.readlines()
            self.info_lin = self.text_formatter(data)


    def text_formatter(self, data):
        lines = []
        for line in data:
            words = line.replace("\n","~").split()
            lines.append(words)
        
        words_ascii = []
        for line in lines:
            for word in line:
                for c in word:
                    words_ascii.append(ord(c))
                if ord(c) != ord('~'):
                    words_ascii.append(ord(' '))
        return words_ascii

    def hide_info(self):
        print("encoding...")
        self.hideout = cv2.imread(self.hideout_file, 1)
        # print(self.info_lin)
        for y in range(len(self.info_lin)):
            self.hideout[0][y][2] = self.hideout[0,y,2]//10*10 + self.info_lin[y]%10
            self.hideout[0][y][1] = self.hideout[0,y,1]//10*10 + self.info_lin[y]//10%10
            self.hideout[0][y][0] = self.hideout[0,y,0]//10*10 + self.info_lin[y]//10//10%10
            self.end_pixel += 3
        cv2.imwrite("encoded.png", self.hideout)
        print("encoded")

    def decode_data(self, encoded_file):
        print("decoding...")       
        text = []
        i = 0
        img = cv2.imread(encoded_file, 1).reshape(-1)
        while i < self.end_pixel:
            sub_ascii = abs(img[i])%10*100 + abs(img[i+1])%10*10 + abs(img[i+2])%10
            text.append(chr(sub_ascii))
            i+=3
        text = ''.join(text).replace("~","\n")
        print("\ndecoded data :- \n","-"*50,"\n")
        print(text,"\n\n","-"*50,"\n")
        
try:
    secret, img_file = sys.argv[1], sys.argv[2]
except:
    print("usage : python image.py file.txt img-to-hide-in.png/jpeg")
    sys.exit(2)

i_obj = Image(secret, img_file)
i_obj.read_info()
i_obj.hide_info()
i_obj.decode_data("decoded.png")