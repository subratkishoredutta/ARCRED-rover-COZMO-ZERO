# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 00:07:33 2020

@author: Asus
"""
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

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
    display = (1000,1000)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    gluPerspective(60, (display[0]/display[1]), 0.1, 500.0)
    
    glTranslatef(0,-2,-20)
    
    glRotatef(0,0,1,0)
    rot=0
    direction=0
    z_change=0
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    direction=1
                    rot=+0.25
                if event.key == pygame.K_RIGHT:
                    direction=-1
                    rot=+0.25
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
        
                                
        glRotatef(rot,0,direction,0)  
        glTranslatef(0,0,z_change)                                
                
        #glRotatef(0.2,0,0,0)##for right and left maneuver use the rotate across the Y axis
        
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        
        #ground()
        
        rover()
        
        if ori_req==1:
            create_origin()
            
        pygame.display.flip()
        pygame.time.wait(10)


main(ori_req=1)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            