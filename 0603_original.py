from collections import deque
import numpy as np
import time
import cv2
import random
import math

pts = deque(maxlen=10) # 3 is ok
end=False
hand_direction=""
computer_direction=""
accux=0
accuy=0
cp=(320, 240)

xth=160
yth=120
dist_th=150

def grepObject(t0, t1):
    global pts, end, hand_direction, computer_direction, accux, accuy, cp

    c1 = cv2.cvtColor(t0, cv2.COLOR_BGR2LAB)
    c2 = cv2.cvtColor(t1, cv2.COLOR_BGR2LAB)
    _, grey1, _ = cv2.split(c1)
    _, grey2, _ = cv2.split(c2)
    d = cv2.absdiff(grey1, grey2)
    d = cv2.GaussianBlur(d,(15,15),0)
    # cv2.imshow("Gray", d)
    ret, mask = cv2.threshold( d, 7, 255, cv2.THRESH_BINARY )
    mask = cv2.erode(mask, None, iterations=4)
    mask = cv2.dilate(mask, None, iterations=10)
    # cv2.imshow("Mask", mask)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    areas = [cv2.contourArea(c) for c in cnts]

    if(len(areas)>0):
        max_index = np.argmax(areas)
        cnt=cnts[max_index]
        x,y,w,h = cv2.boundingRect(cnt)
        if(areas[max_index]>500):
            cv2.rectangle(t1, (x,y),(x+w, y+h), (0,255,0), 5)
            center = (int(x+(w/2)), int(y+(h/2)))
            cp=center
            if math.sqrt((center[0]-cp[0])*(center[0]-cp[0])+(center[1]-cp[1])*(center[1]-cp[1]))<dist_th:
                pts.append(center)
            if(len(pts)>2):
                accux=accux+pts[-1][0]-pts[-2][0]
                accuy=accuy+pts[-1][1]-pts[-2][1]
                cv2.line(t1, pts[-1], pts[-2], (0, 250, 253), 10)
                print("accx={}".format(accux) + ", " + "accy={}".format(accuy))
        
                if abs(accux)>xth and abs(accuy)<yth:
                    if accux>xth:
                        hand_direction='right'
                    elif accux<-xth:
                        hand_direction='left'
                    end=True
                elif abs(accux)<xth and abs(accuy)>yth:
                    if accuy>yth:
                        hand_direction='down'
                    elif accuy<-yth:
                        hand_direction='up'
                    end=True
                elif abs(accux)>xth and abs(accuy)>yth:
                    if abs(accux)>abs(accuy):
                        if accux>xth:
                            hand_direction='right'
                        elif accux<-xth:
                            hand_direction='left'
                    elif abs(accux)<abs(accuy):
                        if accuy>yth:
                            hand_direction='down'
                        elif accuy<-yth:
                            hand_direction='up'
                    end=True
                elif abs(accux)<xth and abs(accuy)<yth:
                    pass

def getCameraRead():
    (grabbed, frame) = camera.read()
    return cv2.flip(frame, 1) # 1:水平轉換

# main
camera = cv2.VideoCapture(0)

while True:
    if 0xFF & cv2.waitKey(1) == 27:
        break

    frame1 = getCameraRead()
    frame2 = getCameraRead()
    grepObject(frame1, frame2)
    cv2.imshow("Frame", frame2)
    
    if end==True:
        computer_direction = random.choice(['up', 'down', 'left', 'right'])
        print("Your direction = "+hand_direction+", "+"computer's direction = "+computer_direction+".")
        if computer_direction==hand_direction:
            print("You win!")
        else:
            print("You lose!")
        time.sleep(2)
        pts.clear()
        end=False
        hand_direction=""
        computer_direction=""
        accux=0
        accuy=0
        cp=(320, 240)

camera.release()
cv2.destroyAllWindows()