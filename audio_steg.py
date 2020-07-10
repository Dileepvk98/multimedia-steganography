from scipy.io import wavfile
import numpy as np
import cv2, sys

def decode_data():
    print("decoding...")
    _, data = wavfile.read('encoded.wav')
    data = data.reshape(-1)
    img, i = [], 0
    while i < end_index:
        subpixel = abs(data[i])%10*100 + abs(data[i+1])%10*10 + abs(data[i+2])%10
        img.append(subpixel)
        i+=3
    return img

def encode_data():
    enc_wav, i = [], 0
    print("encoding...")
    for subpixel in lin_img:
        d1, d2, d3 = int(wav_data[i]/10)*10, int(wav_data[i+1]/10)*10, int(wav_data[i+2]/10)*10

        if d1<0:
            d1-=int(subpixel/10/10)%10
        else:
            d1+=int(subpixel/10/10)%10
        if d2<0:
            d2-=int(subpixel/10)%10
        else:
            d2+=int(subpixel/10)%10
        if d3<0:
            d3-=subpixel%10
        else:
            d3+=subpixel%10

        if d1 <= -32768:
            d1+=10
        if d2 <= -32768:
            d2+=10
        if d3 <= -32768:
            d3+=10
        enc_wav += [d1,d2,d3]
        i+=3
    enc_wav = np.asarray(enc_wav,dtype='int16')
    return np.concatenate((enc_wav,wav_data[i:])), i

# read image to hide
# pic_file, aud_file = 'cloudimg.jpeg', 'fmab4.wav'

try:
    pic_file, aud_file = sys.argv[1], sys.argv[2]
except:
    print("usage :  python   audio_steg.py    pic-to-hide.jpg/png     audio-to-hide-pic-in.wav")
    sys.exit(2)

img = cv2.imread(pic_file,1)
width, height, channels = img.shape
lin_img = img.reshape(-1)
total_subpixels = len(lin_img)

# read audio file to hide image in
rate, data = wavfile.read(aud_file)
wav_data = data.reshape(-1)

# encode
enc_wav, end_index = encode_data()
enc_wav = enc_wav.reshape(data.shape[0], data.shape[1])
wavfile.write('encoded.wav', rate, enc_wav)
print("encoded...")

# decode
dec_img = decode_data()
print("decoded")
dec_img = np.asarray(dec_img)
dec_img = dec_img.reshape(width, height, channels)
cv2.imwrite('decoded.png', dec_img)