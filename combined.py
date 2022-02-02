import face_recognition
import cv2
import numpy as np
import pychromecast
import serial
import time
import requests
import RPi.GPIO as GPIO
import qrcode


# This is a demo of running face recognition on live video from your webcam. It's a little more complicated than the
# other example, but it includes some basic performance tweaks to make things run a lot faster:
#   1. Process each video frame at 1/4 resolution (though still display it at full resolution)
#   2. Only detect faces in every other frame of video.

# PLEASE NOTE: This example requires OpenCV (the `cv2` library) to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library. It's only required if you want to run this
# specific demo. If you have trouble installing it, try any of the other demos that don't require it instead.

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
julian_image = face_recognition.load_image_file("julian.jpg")
julian_face_encoding = face_recognition.face_encodings(julian_image)[0]


scott_image = face_recognition.load_image_file("scott.jpg")
scott_face_encoding = face_recognition.face_encodings(scott_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
   julian_face_encoding,
    scott_face_encoding
]
known_face_names = [
   "julian",
    "scott"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

GPIO.setmode(GPIO.BOARD)
ser1 = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=0.5)

services, browser = pychromecast.discovery.discover_chromecasts()

t = 0
a = 0
b = 5

while t < 1 and a < b:
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Julian Dorm"])
    print([cc.device.friendly_name for cc in chromecasts])
    print('a')
    if len(chromecasts) > 0:
        cast = chromecasts[0]
        cast.wait()
        mc = cast.media_controller
        pychromecast.discovery.stop_discovery(browser)
        t = 1
        print('s')
        continue
    else:
        a = a + 1
        t = 0
        print('f')
        print(a)

t = 0
a = 0

while t < 1 and a < b:
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Julian Dorm display"])
    print([cc.device.friendly_name for cc in chromecasts])
    print('a2')
    if len(chromecasts) > 0:
        cast2 = chromecasts[0]
        cast2.wait()
        mc2 = cast2.media_controller
        pychromecast.discovery.stop_discovery(browser)
        t = 1
        print('s2')
        continue
    else:
        a = a + 1
        t = 0
        print('f2')
        print(a)


def search():
    f = 0
    c = 0

    while f < 1 and c < b:
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Julian Dorm"])
        print([cc.device.friendly_name for cc in chromecasts])
        print('a')
        if len(chromecasts) > 0:
            cast = chromecasts[0]
            cast.wait()
            mc = cast.media_controller
            pychromecast.discovery.stop_discovery(browser)
            f = 1
            print('s')
            continue
        else:
            c = c + 1
            f = 0
            print('f')
            print(c)

    f = 0
    c = 0

    while f < 1 and c < b:
        chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=["Julian Dorm display"])
        print([cc.device.friendly_name for cc in chromecasts])
        print('a2')
        if len(chromecasts) > 0:
            cast2 = chromecasts[0]
            cast2.wait()
            mc2 = cast2.media_controller
            pychromecast.discovery.stop_discovery(browser)
            f = 1
            print('s2')
            continue
        else:
            c = c + 1
            f = 0
            print('f2')
            print(c)

    return mc, mc2

counter = 0

while True:
   # Grab a single frame of video
   ret, frame = video_capture.read()

   # Resize frame of video to 1/4 size for faster face recognition processing
   small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

   # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
   rgb_small_frame = small_frame[:, :, ::-1]

   # Only process every other frame of video to save time
   if process_this_frame:

       # Find all the faces and face encodings in the current frame of video
       face_locations = face_recognition.face_locations(rgb_small_frame)
       face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

       face_names = []
       for face_encoding in face_encodings:
           # See if the face is a match for the known face(s)
           matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
           name = "Unknown"

           # # If a match was found in known_face_encodings, just use the first one.
           # if True in matches:
           #     first_match_index = matches.index(True)
           #     name = known_face_names[first_match_index]

           # Or instead, use the known face with the smallest distance to the new face
           face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
           best_match_index = np.argmin(face_distances)
           if matches[best_match_index]:
               name = known_face_names[best_match_index]

           face_names.append(name)

           if name == "julian":
               ser1.write('s'.encode())
           elif name == "scott":
               ser1.write('x'.encode())
           else:
               ser1.write('n'.encode())

   '''detector = cv2.QRCodeDetector()
   data, bbox, straight_qrcode = detector.detectAndDecode(small_frame)
   if bbox is not None:
       print(f"QRCode data:\n{data}")
       n_lines = len(bbox)
       for i in range(n_lines):
           point1 = tuple(bbox[i][0])
           point2 = tuple(bbox[(i + 1) % n_lines][0])
           cv2.line(small_frame, point1, point2, color=(255, 0, 0), thickness=2)'''

   process_this_frame = not process_this_frame


   # Display the results
   for (top, right, bottom, left), name in zip(face_locations, face_names):
       # Scale back up face locations since the frame we detected in was scaled to 1/4 size
       top *= 4
       right *= 4
       bottom *= 4
       left *= 4

       # Draw a box around the face
       cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

       # Draw a label with a name below the face
       cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
       font = cv2.FONT_HERSHEY_DUPLEX
       cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

   if ser1.inWaiting():
       if ser1.readline().decode('utf-8').rstrip() == 'd':
           print('d')
           counter = counter + 1
           directory = "images/door_{}.jpg".format(counter)
           cv2.imwrite(directory, frame)
           try:
               mc.play_media("http://10.151.74.214:8000/doorbell-sound-effect.mp3", content_type="audio/mpeg")
               print('ding dong')
           except:
               mc, mc2 = search()
               time.sleep(.2)
               mc.play_media("http://10.151.74.214:8000/doorbell-sound-effect.mp3", content_type="audio/mpeg")
               print('ding dong')
           # img = np.array(img)
           try:
               mc2.play_media("http://10.151.74.214:8000/images/door_{}.jpg".format(counter), 'image/jpg')
               print('image')
           except:
               mc, mc2 = search()
               time.sleep(.2)
               mc2.play_media("http://10.151.74.214:8000/images/door_{}.jpg".format(counter), 'image/jpg')
               print('image')

           try:
               requests.post('https://maker.ifttt.com/trigger/doorbell/with/key/lhHHJEOXAxwmKXgD-AYLpSotXdzSAey79YFbT7LpgbX')
               print('ding')
           except:
               continue

   # Display the resulting image
   cv2.imshow('Video', frame)

   """if ser1.readline().decode('utf-8').rstrip() == 'd':
       print('d')
       mc.play_media('https://storage.googleapis.com/pychromecast/Doorbell%20sound%20effect.mp3', 'audio/mpeg')
       mc.block_until_active()
       continue
   else:
       continue """

   # Hit 'q' on the keyboard to quit!
   if cv2.waitKey(1) & 0xFF == ord('q'):
       break


# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

