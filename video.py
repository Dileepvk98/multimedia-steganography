from scipy.io import wavfile
import numpy as np
import cv2, sys, math

NUM_OF_PIX_TO_ENC_PER_FRAME = 100
FRAME_CTR = 0

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
            self.info_lin = self.info.reshape(-1)
            # total_pixels = len(lin_img)
        
        # incomplete
        else:
            pass

    def hide_info(self):
        print("encoding...")
        # open video file (hideout)
        vidcap = cv2.VideoCapture(self.hideout_file)
        # fps_int = math.ceil(vidcap.get(cv2.CAP_PROP_FPS))
        frame_width = int(vidcap.get(3))
        frame_height = int(vidcap.get(4))
        print(frame_height, frame_width)
        out = cv2.VideoWriter('encoded.mov', cv2.VideoWriter_fourcc('m','p','4','v'), 60, (frame_width, frame_height))

        i = 0
        ret, frame = vidcap.read()
        while vidcap.isOpened() and ret:
            if i<len(self.info_lin):
                enc_frame = self.encode_img_into_frame(frame, self.info_lin[i:i+NUM_OF_PIX_TO_ENC_PER_FRAME])
                i+=NUM_OF_PIX_TO_ENC_PER_FRAME
                self.end_frame+=1
                out.write(enc_frame)
            else:
                out.write(frame)
            ret, frame = vidcap.read()
        vidcap.release()
        out.release()

    def encode_img_into_frame(self, frame, img_piece):
        global FRAME_CTR
        for y in range(len(img_piece)):
            # print("encoding pixel : ",img_piece[y], "into", frame[0][y])
            frame[0][y][2] = frame[0,y,2]//10*10 + img_piece[y]%10
            frame[0][y][1] = frame[0,y,1]//10*10 + img_piece[y]//10%10
            frame[0][y][0] = frame[0,y,0]//10*10 + img_piece[y]//10//10%10
            # print("encoded to     :    ",frame[0][y])
            FRAME_CTR+=1
        return frame

    def decode_data(self, encoded_file, infotype):
        print("decoding...")
        if infotype == "image":
            c = 0
            vidcap2 = cv2.VideoCapture(encoded_file)
            ret, frame = vidcap2.read()
            decoded_img = []
            while vidcap2.isOpened() and ret and c< self.end_frame:
                for ctr in  range(NUM_OF_PIX_TO_ENC_PER_FRAME):
                    print(frame[0][ctr])
                    d1 = frame[0][ctr][0]%10
                    d2 = frame[0][ctr][1]%10
                    d3 = frame[0][ctr][2]%10
                    subpixel = d1*100+d2*10+d3
                    decoded_img.append(subpixel)
                ret, frame = vidcap2.read()
                c+=1
            decoded_img = np.array(decoded_img[:len(self.info_lin)])
            decoded_img = decoded_img.reshape(self.info.shape[0], self.info.shape[1], self.info.shape[2])
            cv2.imwrite('decoded.png', decoded_img)
        
        # incomplete
        elif infotype=="text":
            pass

v_obj = Video("cloudimg.jpeg", "image", "flowers.mp4")
v_obj.read_info()
v_obj.hide_info()
v_obj.decode_data("encoded.mov", "image")