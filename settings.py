###IMPORTS
import pygame as pg
import pygame.locals
import time
import random as rd
from pygame.math import Vector2 as vec






##SETTINGS
WIDTH,HEIGHT = 832,640
BLOCKSIZE = 32
INTROTEXTPOS = [[WIDTH/2-120,HEIGHT/2-150],[WIDTH/2-150,HEIGHT/2]]
OVERTEXTPOS = [[WIDTH/2-150,HEIGHT/2-150],[WIDTH/2-250,HEIGHT/2],[WIDTH/2+150,HEIGHT/2]]
BARSPEEDS = [10,20,30,5,15,35,45,25,50]
FONT = 'digital-7.italic.ttf'
X = 100
Y = 100
VEL = 10
GVTA = 90
GVTM = 10



###Number of Lights
NOLIGHTS={1:1,2:2,3:3,4:4,51:4,52:4,61:5,62:5,63:5,7:5,8:6,91:7,92:7,10:6

}


####INITIALIZATION
window = pg.display.set_mode((WIDTH,HEIGHT))
pg.display.set_caption('Escapede')
pg.display.set_icon(pg.image.load('Images/icon.png'))
clock = pg.time.Clock()
pg.init()


###COLORS
BLUE = (4,242,255)
GRAY = (2,95,226)
BLACK = (0,0,0)
LIGHTS = [
(175,61,255),
(85,255,225),
(255,59,148),
(166,253,41),
(55,1,58),
 (62, 0, 253),
 (0, 253, 253),
 (255, 255, 50),
 (206, 255, 3),
  (248, 40, 136),
   (227, 3, 3),
    (253, 174, 50),
    (253, 251, 0),
    (	57, 255, 20)
]
BGCOLOR=(	255,255,255)
GREEN = (1,220,111)
RED = (245,24,1)
YELLOW = (245,153,13)


CLUES = {2:"2+2=?",3:"5-12/6=?",4:"Full of holes but still holds water",10:"Theme",51:"Do you want to be Purple?",52:"What gets wet while drying?",
61:"Wanna mess with gravity?",62:"Wanna mess with gravity?",63:"Number of squares in a chessboard",7:"Has many keys but can’t open a single lock",
8:"Most popular ice cream flavour",91:"Wanna be green?",92:"If 11+2=1 Then what is 9+5=?"}
ANSWERS = {2:"4" , 3: "3" , 10:"HIDE" , 4:"SPONGE",51:"",52:"TOWEL",62:"",63:"204",61:"",7:"PIANO",8:"VANILLA",91:"",92:"2"

}


###images


###BGM
pg.mixer.music.load('Audio/introbgm.wav')

##Sound Effects
jumpfx = pygame.mixer.Sound('Audio/jump.wav')
jumpfx.set_volume(0.1)
pickupfx = [pygame.mixer.Sound('Audio/health.wav'),pygame.mixer.Sound('Audio/battery.wav')]
pickupfx[0].set_volume(0.3)
pickupfx[1].set_volume(0.3)
doorfx = pygame.mixer.Sound('Audio/door.wav')
doorfx.set_volume(0.3)
hitfx = pygame.mixer.Sound('Audio/hit.wav')
#hitfx.set_volume(0.1)

