
import cv2
import numpy as np
import pygame
from pygame.locals import *
import time
from pyfirmata import Arduino,util

from OpenGL.GL import *
from OpenGL.GLU import *

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_cascade = cv2.CascadeClassifier('haarcascade_fullbody.xml')


board=Arduino('COM3')
iterator = util.Iterator(board)
iterator.start()

E1 = board.get_pin('d:9:p')
E2 = board.get_pin('d:3:p')
in1 = board.get_pin('d:8:o')
in2=board.get_pin('d:7:o')
in3=board.get_pin('d:2:o')
in4=board.get_pin('d:4:o')
time.sleep(1.0)


def forward():
    E1.write(1)
    in1.write(1.0)
    in2.write(0.0)
    E2.write(1)
    in3.write(1.0)
    in4.write(0.0)
    time.sleep(0.1)
    
def backward():
    E1.write(1)
    in1.write(0.0)
    in2.write(1.0)
    E2.write(1)
    in3.write(0.0)
    in4.write(1.0)
    time.sleep(0.1)

    
def right():
    E1.write(1)
    in1.write(0.0)
    in2.write(1.0)
    E2.write(1)
    in3.write(1.0)
    in4.write(0.0)
    time.sleep(0.1)


def left():
    E1.write(1)
    in1.write(1.0)
    in2.write(0.0)
    E2.write(1)
    in3.write(0.0)
    in4.write(1.0)
    time.sleep(0.1)


def stop():
    E1.write(0)
    E2.write(0)

def end():
    board.exit()
    

origins = (
        (0,0,0),#12
        (0,4,0),#y
        (4,0,0),#x
        (0,0,4),#z
        )
axes = (
        (0,1),
        (0,2),
        (0,3)
        )


vertices = (
        (3,-1,-4),
        (3,1,-4),
        (-3,1,-4),
        (-3,-1,-4),
        (-3,-1,4),
        (3,-1,4),
        (3,1,4),
        (-3,1,4),
        (-3,-3,6),
        (-3,-3,-6),##OUR GROUND LEVEL IS AT Y=-4
        (3,-3,-6),
        (3,-3,6),
        )

edges = (
        (0,1),
        (0,3),
        (0,5),
        (2,1),
        (2,3),
        (2,7),
        (4,7),
        (4,5),
        (4,3),
        (6,7),
        (1,6),
        (5,6),
        (4,8),
        (3,9),
        (0,10),
        (5,11)
        )

surfaces= (
        (0,1,2,3),
        (4,5,6,7),
        (0,1,6,5),
        (3,2,7,4),
        (1,2,7,6),
        (0,3,4,5)
        )


colors = (
         (1,0,0),
         (1,0,1),
         (0,0,1),
         (0,1,0),
         (1,0,0),
         (1,0,1),
         (1,0,0),
         (1,0,1),
         (0,0,1),
         (0,1,0),
         (1,0,0),
         (1,0,1),

        )

ground_vertices = (
         (-1000,-4,200),
         (1000,-4,200),
         (-1000,-4,-1000),
         (1000,-4,-1000),
         
        )

def ground():
   
    glBegin(GL_QUADS)
    for vertex in ground_vertices:
        glColor3fv((0.4,0.7,0.7))
        glVertex3fv(vertex)
        
    glEnd()

def create_origin():
    glColor3fv(colors[2])
    glBegin(GL_LINES)
    for axis in axes:
        for origin in axis:
            glVertex3fv(origins[origin])      
    glEnd()



def rover():
   
    glBegin(GL_QUADS)
    for surface in surfaces:
        x = 0
        for vertex in surface:
            x+=1
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
        
    glEnd()
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
            
    glEnd()



def main(automate=0,ori_req=0):
    pygame.init()
    display = (1000,700)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(60, (display[0]/display[1]), 0.1, 500.0)
    
    glTranslatef(0,-2,-20)
    
    glRotatef(0,0,1,0)
    rot=0
    direction=0
    z_change=0
    cap = cv2.VideoCapture(0)
    while True:
        _,frame = cap.read()
        frame=cv2.resize(frame,(804,500))
        bnw =  cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(bnw,1.3,5)
        if faces!=():
            for (x,y,w,h) in faces:    
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),4)
        
            mid=(x+x+w)/2
            print(mid)
        elif faces==():
            mid='X'
        cv2.imshow("frame",frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        if automate == 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        direction=1
                        rot=+0.10
                    if event.key == pygame.K_RIGHT:
                        direction=-1
                        rot=+0.10
                    if event.key == pygame.K_UP:
                        z_change=-0.25   
                    if event.key == pygame.K_DOWN:
                        z_change=+0.25 
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                        direction=0 
                        rot=0
                    if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                        z_change=0   
                
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 4:
                        glTranslatef(0,0,1)
                    if event.button == 5:
                        glTranslatef(0,0,-1)
        elif automate == 1:
                if mid=='X':
                    z_change=-0.0
                    rot=0
                    direction=0
                    stop()

                elif mid<=350:
                    direction=1
                    rot=+0.25
                    z_change=0
                    right()
                    stop()
                
                elif mid>=450:
                    direction=-1
                    rot=+0.25
                    z_change=0
                    left()
                    stop()
                
                elif 350<mid<450:
                    z_change=-0.2
                    rot=0
                    direction=0
                    forward()
                    stop()
                
                                
        glRotatef(rot,0,direction,0)  
        glTranslatef(0,0,z_change)                                
        #glRotatef(0.2,0,0,0)##for right and left maneuver use the rotate across the Y axis
        
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #ground()
        
        rover()
        
        if ori_req==1:
            create_origin()
            
        pygame.display.flip()
        #pygame.time.wait(10)
    cap.release()    
    cv2.destroyAllWindows

main(automate=1,ori_req=1)
end()
            
      