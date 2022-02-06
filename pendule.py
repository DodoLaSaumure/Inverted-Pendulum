#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import pygame
from pygame.locals import *
import math
import time

class model(object):
    def __init__(self):
        self.theta = 175.0*math.pi/180.0
        self.x=0.0
        self.vx=0.0
        self.ax=0.0
        self.vTheta=0.0
        self.aTheta = 0.0
        self.g = 9.81
        self.m=0.05 #kg
        self.l = 100*200*0.14/800.0 #m
        self.deltaT = 1.0/30.0
        self.t0 = time.time()
    def ApplyMove(self,newX):
        self.deltaT = time.time()-self.t0
        self.t0 = time.time()
        newX = newX*0.14/800.0*100.0
        vx = (newX-self.x)/self.deltaT
        ax = (vx - self.vx)/self.deltaT
        aTheta = (self.g/2.0*math.sin(self.theta)-0.5*ax*math.cos(self.theta))*3.0/self.l
        self.vTheta = self.deltaT*aTheta+self.vTheta
        self.theta = self.vTheta*self.deltaT+self.theta
        self.vx =vx
        self.ax =ax
        self.x=newX
        self.aTheta=aTheta

class controller(object):
    def __init__(self):
        self.view = view()
        self.model =model()
        
    def mainLoop(self):
        delta = 0
        while self.view.continuer :
            time.sleep(0.01)
            self.view.getposXMouse()

            if self.view.left_button_pressed :
#                 delta = self.view.x_mouse - 
                delta = self.view.x_mouse-400.0
            self.model.ApplyMove(delta)
#                 self.view.action(delta,20.0)
            self.view.action(delta+400,-self.model.theta*180.0/math.pi)
            self.view.processFrame()

            
        self.view.quit()
class view(object):
    def __init__(self):
        pygame.init()
        self.fenetre = pygame.display.set_mode((800, 600))
        self.BLANC = (255,255,255)
        self.perso_surf = self.perso_rotated_surf = pygame.image.load("Baton.png").convert_alpha()
        self.perso_rect = self.perso_surf.get_rect(center=(400, 300))
        self.perso_angle = -175
        self.center_x=400
        self.continuer = True
        self.x_mouse = 0
        self.left_button_pressed =False
    def action(self,x,theta):
        self.center_x = int(x)
        self.perso_angle=int(theta)%360
        self.perso_rotated_surf = pygame.transform.rotate(self.perso_surf, self.perso_angle)
        self.perso_rect = self.perso_rotated_surf.get_rect(center=(self.center_x, 300))
    def processFrame(self):
        for event in pygame.event.get():    #Attente des événements clavier
            if event.type == QUIT:
                self.continuer = False
#         clock = pygame.time.Clock()
        self.fenetre.fill(self.BLANC)
        self.fenetre.blit(self.perso_rotated_surf, self.perso_rect)
        pygame.display.flip()
#         clock.tick(100) # Max 30 FPS
    def getposXMouse(self):
        self.x_mouse = pygame.mouse.get_pos()[0]
        self.left_button_pressed = pygame.mouse.get_pressed()[0]

    def quit(self):
        pygame.quit()


if __name__ == "__main__":
    myController = controller()
    myController.mainLoop()