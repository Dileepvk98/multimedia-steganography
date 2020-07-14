from scipy.io import wavfile
import numpy as np
import cv2, sys, math
import skvideo.io

NO_OF_SUB_PIX_ASCII_PER_FRAME = 100

class Video:
    def __init__(self, infofile, infotype, vid_file):
        self.hideout_file = vid_file
        # self.hideout = None
        # self.width = None
        # self.height = None
        # self.channel = None
        # self.hideout_lin = None
        # self.rate = None

        self.infotype = infotype
        self.infofile = infofile
        self.info = None
        self.info_lin = None
        self.end_frame = 0

    def read_info(self):
        if self.infotype == "image":
            self.info = cv2.imread(self.infofile,1)
            # self.width, self.height, self.channel = self.info.shape
            print(self.info.shape)
            self.info_lin = self.info.reshape(-1)
            print(self.info_lin[:10])
            print(len(self.info_lin))
            # total_pixels = len(lin_img)
        
        # incomplete
        else:
            pass

    def hide_info(self):
        print("encoding...")
        # open video file (hideout)
        global NO_OF_SUB_PIX_ASCII_PER_FRAME
        vidcap = cv2.VideoCapture(self.hideout_file)
        # fps_int = math.ceil(vidcap.get(cv2.CAP_PROP_FPS))
        frame_width = int(vidcap.get(3))
        frame_height = int(vidcap.get(4))
        # print(frame_height, frame_width)
        if len(self.info_lin) < NO_OF_SUB_PIX_ASCII_PER_FRAME:
            NO_OF_SUB_PIX_ASCII_PER_FRAME = len(self.info_lin)

        # out = cv2.VideoWriter('encoded.mov', cv2.VideoWriter_fourcc('m','p','4','v'), 60, (frame_width, frame_height))
        out = skvideo.io.FFmpegWriter("encoded.mov", outputdict={
  '-vcodec': 'libx264',  #use the h.264 codec
  '-crf': '0',           #set the constant rate factor to 0, which is lossless
  '-preset':'veryslow'   #the slower the better compression, in princple, try 
                         #other options see https://trac.ffmpeg.org/wiki/Encode/H.264
}) 

        i = 0
        ret, frame = vidcap.read()
        while vidcap.isOpened() and ret:
            if i<len(self.info_lin):
                enc_frame = self.encode_into_frame(frame, self.info_lin[i:i+NO_OF_SUB_PIX_ASCII_PER_FRAME])
                i+=NO_OF_SUB_PIX_ASCII_PER_FRAME
                self.end_frame+=1
                # out.write(enc_frame)
                out.writeFrame(enc_frame)
            else:
                out.writeFrame(frame)
            ret, frame = vidcap.read()
        vidcap.release()
        # out.release()
        out.close()

    def encode_into_frame(self, frame, img_piece):
        for y in range(len(img_piece)):
            # print("encoding pixel : ",img_piece[y], "into", frame[0][y])
            frame[0][y][2] = frame[0,y,2]//10*10 + img_piece[y]%10
            frame[0][y][1] = frame[0,y,1]//10*10 + img_piece[y]//10%10
            frame[0][y][0] = frame[0,y,0]//10*10 + img_piece[y]//10//10%10
            # print("encoded to     :    ",frame[0][y])
        return frame

    def decode_data(self, encoded_file, infotype):
        print("decoding...")
        if infotype == "image":
            fc = 0
            vidcap2 = cv2.VideoCapture(encoded_file)
            ret, frame = vidcap2.read()
            decoded_img = []
            while vidcap2.isOpened() and ret and fc < self.end_frame:
                ctr = 0
                i = 0
                while i < NO_OF_SUB_PIX_ASCII_PER_FRAME:
                    d1 = frame[0][ctr][0]%10
                    d2 = frame[0][ctr][1]%10
                    d3 = frame[0][ctr][2]%10
                    subpixel = d1*100+d2*10+d3
                    decoded_img.append(subpixel)
                    ctr+=3
                    i+=1
                ret, frame = vidcap2.read()
                fc+=1
            print(decoded_img[:10])
            print(len(decoded_img))
            decoded_img = np.asarray(decoded_img[:len(self.info_lin)])
            decoded_img = decoded_img.reshape(self.info.shape[0], self.info.shape[1], self.info.shape[2])
            cv2.imwrite('decoded.png', decoded_img)
        
        # incomplete
        elif infotype=="text":
            pass

v_obj = Video("cloudimg.jpeg", "image", "flowers.mp4")
v_obj.read_info()
v_obj.hide_info()
v_obj.decode_data("encoded.mov", "image")