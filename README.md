# Multimedia steganography program

## Requirements 

- numpy
- scipy.io
- cv2
- scikit-video
- flask

## Usage

> to run flask app
- python app.py
    >
> to run via cli
- python audio.py encode type file-to-hide audio-to-hide-in.wav
- python audio.py decode key encoded_file.wav
    >
- python image.py encode file.txt img-to-hide-in
- python image.py decode key encoded.png
    
## Contraints
- .wav format necessary as other formats use lossy compression
- encoded img must be .png or any other lossless compression like .bmp, .raw
- secret file must be smaller than media file  ¯\_(ツ)_/¯

## Coming Soon

- Fix text/image/audio in Video (lossy compression issue)
