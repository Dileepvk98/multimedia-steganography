Steganography program for hiding information in an Audio/Video file
===============================================================


Introduction
------------

Read the image/video/audio files as numpy array & split the value of each subpixel/ASCII value into individual digits and use it to modify the last digit of each subpixel/audio sample. 

Eg. consider the pixel [ 234 125 150 ] (R,G,B).
Let the letter to be hidden be "s" with ASCII code of 115.
After modification the pixel value will be [ 231 121 155 ]. 

(Each subpixel/ASCII requires 3 subpixels)

Since only the last digit is being changed there is no visible loss/anomaly in the hidden file.


## Requirements 

- numpy
- scipy.io
- cv2 
- sys
- math

## Usage

- python audio.py text file_name.txt audio_file.wav

- python audio.py image file_name.png/jpeg audio_file.wav
    
## Contraints
- .wav format necessary as other formats use lossy compression

## Coming Soon

- Warn if the file to be hidden does not fit the hideout audio/video/image and give and option to continue with truncation.
- UI
- Video in video
- Audio in audio