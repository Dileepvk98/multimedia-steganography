# Multimedia steganography program

## Requirements 

- numpy
- scipy.io
- cv2 
- sys
- math
- scikit-video
- uuid
- datetime
- os
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

## Coming Soon

- Warn if the file to be hidden does not fit the hideout audio/video/image and give and option to continue with truncation.
- Audio in audio
- Fix text/image in Video (lossy compression issue)
- Video in video
