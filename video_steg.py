import numpy as np
import cv2
import math

num_of_enc_pixels = 100
end_frame_num = 0
frame_ctr = 0

def decode_video():
    c = 0
    vidcap2 = cv2.VideoCapture('output.mov')
    ret, frame = vidcap2.read()
    decoded_img = []
    while vidcap2.isOpened() and ret and c<end_frame_num:
        for ctr in  range(num_of_enc_pixels):
            d1 = frame[0][ctr][0]%10
            d2 = frame[0][ctr][1]%10
            d3 = frame[0][ctr][2]%10
            subpixel = d1*100+d2*10+d3
            decoded_img.append(subpixel)
        ret, frame = vidcap2.read()
        c+=1
    return decoded_img

def encode_img_into_frame(frame, img_piece):
    ctr = 0
    global frame_ctr
    for y in range(len(img_piece)):
        # print("encoding pixel : ",img_piece[ctr], "into", frame[0][y])
        frame[0][y][2] = frame[0,y,2]//10*10 + img_piece[ctr]%10
        frame[0][y][1] = frame[0,y,1]//10*10 + img_piece[ctr]//10%10
        frame[0][y][0] = frame[0,y,0]//10*10 + img_piece[ctr]//10//10%10
        ctr+=1
        # print("encoded to     :    ",frame[0][y])
        frame_ctr+=1
    return frame
        
pic_file, v_file = 'cloudimg.jpeg', 'flowers.mp4'
img = cv2.imread(pic_file,1)
width, height, channels = img.shape
lin_img = img.reshape(-1).tolist()
total_pixels = len(lin_img)

vidcap = cv2.VideoCapture(v_file)
fps_int = math.ceil(vidcap.get(cv2.CAP_PROP_FPS))
frame_width = int(vidcap.get(3))
frame_height = int(vidcap.get(4))
out = cv2.VideoWriter('output.mov', cv2.VideoWriter_fourcc('m','p','4','v'), 60, (frame_width, frame_height))

i, ctr = 0, 0
ret, frame = vidcap.read()
while vidcap.isOpened() and ret:
    if i<total_pixels:
        enc_frame = encode_img_into_frame(frame, lin_img[i:i+num_of_enc_pixels])
        i+=num_of_enc_pixels
        end_frame_num+=1
        out.write(enc_frame)
    else:
        out.write(frame)
    ctr+=1
    ret, frame = vidcap.read()
# print("end frame no : ",end_frame_num)
vidcap.release()
out.release()

dec_img = decode_video()
dec_img = np.array(dec_img[:total_pixels])
print("num of pixels*3 in decoded image : ",len(dec_img))
print(dec_img)
print(type(dec_img))
dec_img = dec_img.reshape(width, height, channels)
print(dec_img.shape[0])
print(dec_img.shape[1])
cv2.imwrite('aaa.png', dec_img)
# cv2.waitKey(0)