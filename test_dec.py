import numpy as np
import cv2

num_of_enc_pixels = 100
end_frame_num = 0
frame_ctr = 0
pic_file = 'cloudimg.jpeg'
img = cv2.imread(pic_file,1)
lin_img = img.reshape(-1).tolist()


def decode_video():
    decoded_img = []
    frame = cv2.imread('frame0.png',1)
    print(type(frame))
    for ctr in  range(num_of_enc_pixels):
        d1 = frame[0][:num_of_enc_pixels][ctr][0]%10
        d2 = frame[0][:num_of_enc_pixels][ctr][1]%10
        d3 = frame[0][:num_of_enc_pixels][ctr][2]%10
        subpixel = d1*100+d2*10+d3
        decoded_img.append(subpixel)
    return decoded_img
      
print("linearized input img : ",lin_img[:20])
dec_img = decode_video()
# print("num of pixels*3 in decoded image : ",len(dec_img))
# dec_img = np.array(dec_img)
print(" from encoded frame : ",dec_img[:20])
# dec_img = dec_img.reshape(177,285,3)
# print(dec_img.shape[0])
# print(dec_img.shape[1])
# cv2.imshow('a',dec_img)
# cv2.waitKey()