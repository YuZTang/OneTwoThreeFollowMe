import cv2
import numpy as np
import dlib
import queue
import threading
import collections
import time
import random
import pygame

global q
q = queue.Queue(10)

global dx
trackLength = 60

dx = collections.deque(maxlen=trackLength)
dy = collections.deque(maxlen=trackLength)
pygame.mixer.init()
track = pygame.mixer.music.load("男生女生配.mp3")

#載入電腦方向箭頭圖片
RIGHT=cv2.imread("right.jpg")
LEFT=cv2.imread("left.jpg")
UP=cv2.imread("up.jpg")
DOWN=cv2.imread("down.jpg")
#cv2.imshow("Try",UP)

cv2.namedWindow("Computer", 0)
cv2.moveWindow("Computer", 100, 100)
cv2.resizeWindow("Computer", 1200, 600)



#判斷輸贏
def judge():
    #time.sleep(0.5)
    #播放音訊    
    #pygame.mixer.music.play()   
    while True:
        if len(dx)==0:
            time.sleep(0.5)
            pygame.mixer.music.play() 
        if len(dx)>9 and len(dy)>9:
            
            diff_x=dx[9]-dx[4]
            diff_y=dy[9]-dy[4]
            if diff_x >0 and abs(diff_x)>abs(diff_y):
                direction='Left'
                
            elif diff_x<0 and abs(diff_x)>abs(diff_y):
                
                direction='Right'
            elif diff_y>0 and abs(diff_x)<abs(diff_y):
                direction='Down'
    
            else:
                direction='Up'

            computer=random.choice(['Up','Down','Left','Right'])
            return computer

            if computer==direction: 
                result=('Lose')
                print(result)
            
            else:
                result=('Nothing')
                print(result)
            #print('Me is {:s}'.format(direction))
            print("Me is "+direction)
            print('Computer is {:s}'.format(computer))
            #time.sleep(1)
            dx.clear()
            dy.clear()
         
         
            '''
        if q.qsize() >9:
            q.queue.clear()
            '''
 

#建立一個子執行緒
t=threading.Thread(target=judge)



cap = cv2.VideoCapture(0)


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
t.start()
#pygame.mixer.music.play()        

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

        landmarks = predictor(gray, face)
        dx.append(landmarks.part(33).x)
        dy.append(landmarks.part(33).y)
        print(len(dx))
        #print(len(dy))
        
         
        
        #q.put(landmarks.part(33).x)
        #print(q.full())
        #if q.qsize()>15:
            #t.start()
            #q.queue.clear()

        #print(q.qsize())
       
        

        #print(q.get())
        #print(landmarks.part(33).x)
        #print(landmarks.part(33))
        for n in range(0, 68):
            
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)
            
    #frame = cv2.resize(frame, (2400, 2400), interpolation=cv2.INTER_CUBIC)
    #cv2.imshow("Frame", frame)
    if len(dx)>9:
        #cv2.namedWindow("Computer", 0)
        #cv2.moveWindow("Computer", 100, 100)
        #cv2.resizeWindow("Computer", 1200, 600)
        a=judge()
        print(a)
        if a=='Up':
            cv2.imshow('Computer',UP)
        elif a=='Down':
            cv2.imshow('Computer',DOWN)
        elif a=='Left':
            cv2.imshow('Computer',LEFT)
        else:
            cv2.imshow('Computer',RIGHT)

    key = cv2.waitKey(5000)
    if key == 27:
        break


