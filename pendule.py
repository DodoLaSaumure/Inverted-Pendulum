import math
import sys
import time
from random import random,randint
import pygame
from pygame.locals import *

LONGUEUR = 0.5 #m
SCALE = 100./LONGUEUR # 100 px pour le baton de longeur L
DELTAT = 1./100.#seconds
class model(object):
    def __init__(self):
        self.theta = 10.*math.pi/180.0 #radians
        self.x=0.0 #m
        self.vx=0.0
        self.ax=0.0
        self.vTheta=0.0
        self.aTheta = 0.0
        self.g = 9.81
        self.m=1. #kg (50g)
        self.l = LONGUEUR#200*1.4/800.0 #m => 35 cm 200 px
        self.l =0.35 #100 px
        self.deltaT = DELTAT
        self.t0 = time.time()
        self.lastx = 0.0
    def ApplyMove(self,newX,deltaT =True):
        if deltaT :
            self.deltaT = DELTAT
        else :
            self.deltaT = time.time()-self.t0
            self.t0 = time.time()
        vx = (newX-self.x)/self.deltaT
        ax = (vx - self.vx)/self.deltaT
        aTheta = (self.g/2.0*math.sin(self.theta)-0.5*ax*math.cos(self.theta))*3.0/self.l
        self.vTheta = self.deltaT*aTheta+self.vTheta*0.99
        self.theta = self.vTheta*self.deltaT+self.theta
        self.vx =vx
        self.ax =ax
        self.lastx = self.x
        self.x=newX
        self.aTheta=aTheta
    def printState(self):
        print("x",self.x,"deltaX", self.x-self.lastx,"vx",self.vx,"ax",self.ax,"vtheta",self.vTheta)
    def getState(self):
        return [self.x,self.vx,self.ax,self.theta,self.vTheta]
class controller(object):
    def __init__(self):
        self.view = view()
        self.model =model()
        
    def mainLoop(self):
        delta = 0
        max = 0
        while self.view.continuer :
            [x,vx,ax,theta,vtheta]=self.model.getState()
            time.sleep(DELTAT)

            deltax = self.model.theta+0.1*self.model.vx+0.05*self.model.x#+self.model.x*0.2
            print (self.model.theta,self.model.vx,deltax,type(deltax))
#             deltax =0
            lastx = self.model.x
            newx = lastx + deltax*0.1
            self.model.ApplyMove(newx)
            self.view.action(newx,-self.model.theta*180.0/math.pi)
            self.view.processFrame()
        self.view.quit()
        
        

class view(object):
    def __init__(self):
        pygame.init()
        self.fenetre = pygame.display.set_mode((800, 600))
        self.BLANC = (255,255,255)
        self.BLACK = (0,0,0)
        self.myfont = pygame.font.SysFont("Comic Sans MS", 30)
        textToDisp =" "
        self.label = self.myfont.render(textToDisp, 1,self.BLACK)
        self.perso_surf = self.perso_rotated_surf = pygame.image.load("Baton.png").convert_alpha()
        self.perso_rect = self.perso_surf.get_rect(center=(400, 300))
        self.perso_angle = -175
        self.center_x=400
        self.continuer = True
        self.x_mouse = 0
        self.left_button_pressed =False
        self.enterPressed = False
    def action(self,x,theta):
        self.center_x = int(400+x*SCALE)
        self.perso_angle=int(theta)%360
        self.perso_rotated_surf = pygame.transform.rotate(self.perso_surf, self.perso_angle)
        self.perso_rect = self.perso_rotated_surf.get_rect(center=(self.center_x, 300))
    def processFrame(self):
        for event in pygame.event.get():    #Attente des événements clavier
            if event.type == QUIT:
                self.continuer = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.continuer = False
                if event.key == pygame.K_RETURN:
                    self.enterPressed = True
#         clock = pygame.time.Clock()
        self.fenetre.fill(self.BLANC)
        self.fenetre.blit(self.perso_rotated_surf, self.perso_rect)
        self.fenetre.blit(self.label, (10, 10))
        pygame.display.flip()
#         clock.tick(100) # Max 30 FPS
    def getposXMouse(self):
        self.x_mouse = pygame.mouse.get_pos()[0]
        self.left_button_pressed = pygame.mouse.get_pressed()[0]
    def dspText(self,textToDisp):
        self.label = self.myfont.render(textToDisp, 1,self.BLACK)
    def quit(self):
        pygame.quit()

if __name__ == "__main__":
    myController = controller()
    myController.mainLoop()
