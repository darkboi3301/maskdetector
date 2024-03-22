import os
print("the path was",os.path.dirname(os.path.realpath(__file__)))
path = (os.path.dirname(os.path.realpath(__file__)))
os.chdir(path)
print ("the directory is now changed to",path)
print ('''
   __  ______   ______ __  
  /  |/  / _ | / __/ //_/  
 / /|_/ / __ |_\ \/ ,<     
/_/  /_/_/ |_/___/_/|_|    

   ___  _____________________________  ___ 
  / _ \/ __/_  __/ __/ ___/_  __/ __ \/ _ )
 / // / _/  / / / _// /__  / / / /_/ / , _/
/____/___/ /_/ /___/\___/ /_/  \____/_/|_| -ELITE-3
                                            ''')
print ('''INSTRUCTIONS: 
1.change the threshold value based on your light available (default 100)
2.remove the playsound function if u dont want the sound to be played
3 press escape in camera output to exit properly
4.be safe and enjoy''')
ent = "1"
ent = input("press enter to start")
print('''MASK DETECTOR WILL START in ''')
print("5")
import time
import cv2
print("4")


time.sleep(1)
face_cascade = cv2.CascadeClassifier('face.xml')
mouth_cascade = cv2.CascadeClassifier('nose2.xml')
# Adjust threshold value in range 80 to 105 based on your light.
bw_threshold = 100
sound = 1
print("3")
font = cv2.FONT_HERSHEY_SIMPLEX
org = (30, 30)
weared_mask_font_color = (0, 255,0)
green = (0, 255,0)

not_weared_mask_font_color = (0, 0, 255)
red = (0, 0, 255)
thickness = 2
font_scale = 1
weared_mask = "all clear"
not_weared_mask = "potential non masked person"
col = (255,255,255)
print("2")

# Read video
cap = cv2.VideoCapture(0)
print("1")
print("starting.......")

while 1:
    # Get individual frame
    ret, img = cap.read()
    img = cv2.flip(img,1)

    # Convert Image into gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Convert image in black and white
    (thresh, black_and_white) = cv2.threshold(gray, bw_threshold, 255, cv2.THRESH_BINARY)
    #cv2.imshow('black_and_white', black_and_white)

    # detect face
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Face prediction for black and white
    faces_bw = face_cascade.detectMultiScale(black_and_white, 1.1, 4)


    if(len(faces) == 0 and len(faces_bw) == 0):
        cv2.putText(img, "all clear", org, font, font_scale, (0,255,0), thickness, cv2.LINE_AA)
    elif(len(faces) == 0 and len(faces_bw) == 1):
        col = (0,225,0)
       
        
        #compensation for white mask covering nose, with gray image face prediction is not happening
        cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
    else:
        # Draw rectangle on face
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), col, 2)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = img[y:y + h, x:x + w]


            # Detect lips counters
            mouth_rects = mouth_cascade.detectMultiScale(gray, 1.5, 5)

        # Face detected but nosee not detected which means person is wearing mask
        if(len(mouth_rects) == 0):
            col = (0,225,0)
            cv2.putText(img, weared_mask, org, font, font_scale, weared_mask_font_color, thickness, cv2.LINE_AA)
        else:
            for (mx, my, mw, mh) in mouth_rects:

                if(y < my < y + h):
                    print("alert!..")
                    time.sleep(0.1)
                    col = (0,0,255)
                    # Face and nose are detected but nose coordinates are within face cordinates which `means nose prediction is true and
                    # person is not waring mask
                    cv2.putText(img, not_weared_mask, org, font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    cv2.putText(img,'no mask', (x,y), font, font_scale, not_weared_mask_font_color, thickness, cv2.LINE_AA)
                    #cv2.rectangle(img, (mx, my), (mx + mh, my + mw), (0, 0, 255), 3)
                    break

    # Show frame with results
    cv2.imshow('Mask Detector', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Release video
cap.release()
cv2.destroyAllWindows()
