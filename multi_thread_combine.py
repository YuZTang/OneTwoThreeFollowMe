import cv2
import numpy as np
import dlib
import queue
import threading
import collections
import time
import random
import pygame

#設定deque的最大長度跟設定deque
trackLength = 60
dx = collections.deque(maxlen=trackLength)
dy = collections.deque(maxlen=trackLength)

#初始化pygame音訊播放
pygame.mixer.init()
track = pygame.mixer.music.load("男生女生配.mp3")



#先開啟第二個視窗
#cv2.namedWindow("Computer", 0)
#cv2.moveWindow("Computer", 100, 100)
#cv2.resizeWindow("Computer", 600, 600)
#b=cv2.startWindowThread()



#判斷輸贏
def judge():
    global img
    global result
    global computer
    time.sleep(0.5)
    #播放音訊    
    pygame.mixer.music.play()   
    while True:
        if len(dx)>10 and len(dy)>10:
            
            diff_x=dx[10]-dx[4]
            diff_y=dy[10]-dy[4]
            if diff_x >0 and abs(diff_x)>abs(diff_y):
                direction='Left'
                
            elif diff_x<0 and abs(diff_x)>abs(diff_y):
                
                direction='Right'
            elif diff_y>0 and abs(diff_x)<abs(diff_y):
                direction='Down'
    
            else:
                direction='Up'

            computer=random.choice(['Up','Down','Left','Right'])

            if computer=='Up':

                img=cv2.imread("up.jpg")
                
            elif computer=='Down':
                img=cv2.imread("down.jpg")
                
            elif computer=='Left':

                img=cv2.imread("left.jpg")
               
            else:
                img=cv2.imread("right.jpg")
                
            if computer==direction: 
                result=('Lose')
                print(result)
            
            else:
                result=('Nothing')
                print(result)
        
            print("Me is "+direction)
            print('Computer is {:s}'.format(computer))
            time.sleep(1)
            dx.clear()
            dy.clear()
 

#螢幕繪圖指令
def plot():
    while True:
        if len(dx)>10:
            time.sleep(0.1)
            #right
            if computer == 'Right':
                cv2.line(frame, (460, 360),(820,360), (255,255,255), 3)
                cv2.line(frame,(580,431) , (460,360), (255,255,255), 3)
                cv2.line(frame, (580,289), (460,360), (255,255,255), 3)
                    
            #left
            if computer == 'Left' :
                cv2.line(frame, (460, 360),(820,360), (255,255,255), 3)
                cv2.line(frame,(700,431) , (820,360), (255,255,255), 3)
                cv2.line(frame, (700,289), (820,360), (255,255,255), 3)
                    
            #down
            if computer == 'Down' :
                cv2.line(frame, (640, 180),(640,540), (255,255,255), 3)
                cv2.line(frame,(640, 540) , (711,420), (255,255,255), 3)
                cv2.line(frame, (640, 540), (569,420), (255,255,255), 3)
                    
            #up
            if computer == 'Up' :
                cv2.line(frame, (640, 540),(640,180), (255,255,255), 3)
                cv2.line(frame,(640, 180) , (569,300), (255,255,255), 3)
                cv2.line(frame, (640, 180), (711,300), (255,255,255), 3)
            #time.sleep(0.5)
            cv2.putText(frame, result , (10, 600), cv2.FONT_HERSHEY_SIMPLEX,5, (0, 255, 255), 10, cv2.LINE_AA) 


#建立一個子執行緒
t=threading.Thread(target=judge)
t2=threading.Thread(target=plot)

#開啟相機
cap = cv2.VideoCapture(0)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
t.start()
t2.start()       

while True:
    _, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
        
        if x2 - x1 < 350:
            #print("x2-x1 < 300")
            continue
            
        
        
        landmarks = predictor(gray, face)
        dx.append(landmarks.part(33).x)
        dy.append(landmarks.part(33).y)
        print(len(dx))
                    
        for n in range(0, 68):
            
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
            #中央定位框
            #cv2.rectangle(frame, (460,540), (820,180), (0, 255, 0), 3)

            
 

    # if result=='Lose':

    cv2.imshow("Frame", frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break


