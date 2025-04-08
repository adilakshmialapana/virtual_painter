import cv2
import os

import numpy as np

import handTrackmodule as htm

############################
brushThickness=20
eraserThickness=90
xp,yp=0,0
imgCanvas=np.zeros((720,1280,3),np.uint8)


############################


# Load Header Images
folderpath = "header"
mylist = os.listdir(folderpath)
print("Files in header folder:", mylist)

overlayList = []
for imPath in mylist:
    image = cv2.imread(f'{folderpath}/{imPath}')
    if image is None:
        print(f"Error: Could not load image {imPath}")
    else:
        overlayList.append(image)

if len(overlayList) == 0:
    print("Error: No valid header images found!")
    exit()

# Initialize Webcam
cap = cv2.VideoCapture(0)

# Set Resolution to Maximum Available
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Set width to Full HD
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Set height to Full HD

success, img = cap.read()
if not success or img is None:
    print("Error: Webcam frame not captured!")
    exit()

print("Webcam frame shape:", img.shape)

# Set header size dynamically
header = overlayList[0]
header = cv2.resize(header, (img.shape[1], 150))  # Resize to match full width
drawcolor=(255,0,255)

detector = htm.handDetector(detectionCon=0.85)

# Create Full-Screen Window
cv2.namedWindow("Image", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Image", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    success, img = cap.read()
    if not success or img is None:
        print("Error: Frame not captured")
        break

    img = cv2.flip(img, 1)  # Flip for natural view
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]
        x2, y2 = lmList[12][1:]

        fingers = detector.fingersUp()

        if fingers[1] and fingers[2]:  # Selection Mode
            xp,yp=0,0
            print("Selection Mode")
            #checking for the click
            if y1 < 150:
                if 550 < x1 < 750:
                    header = cv2.resize(overlayList[0], (img.shape[1], 150))
                    drawcolor=(255,0,0)
                elif 250 < x1 < 450:
                    header = cv2.resize(overlayList[1], (img.shape[1], 150))
                    drawcolor = (255,0,255)
                elif 800 < x1 < 950:
                    header = cv2.resize(overlayList[2], (img.shape[1], 150))
                    drawcolor = (0, 255, 0)
                elif 1050 < x1 < 1200:
                    header = cv2.resize(overlayList[3], (img.shape[1], 150))
                    drawcolor = (0, 0, 0)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawcolor, cv2.FILLED)
        if fingers[1] and not fingers[2]:  # Drawing Mode
            cv2.circle(img, (x1, y1), 15,drawcolor , cv2.FILLED)
            print("Drawing Mode")
            if xp==0 and yp==0:
               xp,yp=x1,y1
            #for eraser thicknesss
            if drawcolor==(0,0,0):
                cv2.line(img, (xp, yp), (x1, y1), drawcolor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawcolor,brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawcolor, brushThickness)
            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _,imgInv=cv2.threshold(imgGray,50,255,cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img=cv2.bitwise_and(img,imgInv)
    img=cv2.bitwise_or(img,imgCanvas)



    # Apply header
    img[0:150, 0:img.shape[1]] = header
    img=cv2.addWeighted(img,0.5,imgCanvas,0.5,0)

    # Display the full-screen window
    cv2.imshow("Image", img)


    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()
