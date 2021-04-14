import pygame as pg
import time
import random as rd

disp = pg.display.set_mode((500,700))
pg.init()

grid=[]
for i in range(30):
    row=[]
    for j in range(30):
        row.append("0")
    grid.append(row)





colors = [(0,12,0),(255,0,0),(0,255,0),(0,0,255),(255,0,255),(255,255,0),(0,255,255)]
symbols = ["0","r","g","b","m","y","c"]

CURRENT = "0"


clock = pg.time.Clock()

class Block(pg.sprite.Sprite):
    def __init__(self,typ,i,j,x,y):
        super().__init__()
        self.ind = symbols.index(typ)
        self.color = colors[self.ind]
        self.type = typ
        self.x = x
        self.y = y
        self.i = i
        self.j = j
        self.image = pg.Surface((16,16))
        self.imagify()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)


    def imagify(self):
        self.image.fill((255,255,255))
        if self.type!="0":
            self.image.fill(self.color)

        else:
            pg.draw.rect(self.image,(0,12,0),[0,0,16,16],width=1)

        
        grid[self.j][self.i] = self.type
        

    def change(self):
        self.ind = symbols.index(CURRENT)
        self.type = CURRENT
        self.color = colors[self.ind]
        
        self.imagify()
    
    def update(self):
        if self.type!="0":
            self.image.fill(self.color)
        

    
output="PLAYER POSITION\n"

all_sprites = pg.sprite.Group()
blocks = pg.sprite.Group()

disp.fill(-1)
x=10
y=10
for i in range(30):
    x=10
    for j in range(30):
        s=grid[j][i]
        bl = Block(s,j,i,x,y)
        all_sprites.add(bl)
        x+=16
    y+=16
        

x=10
y=500
for i in range(len(symbols)):
    bl = Block(symbols[i],0,0,x,y)
    blocks.add(bl)
    x+=70
    

                
                
        


def clicks():
    global CURRENT
    mouse = pg.mouse.get_pos()
    
    

    for bl in blocks:
        if bl.rect.collidepoint(mouse):
            clicks = pg.mouse.get_pressed()
            if clicks[0]:
                CURRENT = bl.type

    for bl in all_sprites:
        if bl.rect.collidepoint(mouse):
            clicks = pg.mouse.get_pressed()
            if clicks[0]:
                bl.change()
    
    #time.sleep(.1)
    clock.tick(60)
            

def outputyo():
    output="#PLATFORMS x y length direction pixels to move\n"

    plats=""
    pups=""
    doors=""
    n_plats=0
    n_ups = 0
    n_doors = 0
    for i in range(30):
        l=0
        start=[0,0]
        for j in range(30):
            if grid[i][j] =="m":
                plp = "%d %d"%(i,j)
            if grid[i][j]=="b":
                doors+="%d %d %d %d\n"%(i,j,0,5)
                n_doors+=1
            if grid[i][j]=="g":
                pups+="%d %d %d %d\n"%(i,j,rd.choice([0,1]),rd.randint(1,30))
                n_ups+=1

            if grid[i][j]=="r":
                if l==0:
                    start = [i,j]
                l+=1
            elif l>0:
                d=rd.choice([0,1,2])
                if d==0:
                    s=0
                else:
                    s=rd.randint(1,15)
                plats+="%d %d %d %d %d\n"%(start[0],start[1],l,d,s)
                n_plats+=1
                l=0
                start=[0,0]
    
    output+=str(n_plats)+"\n"
    output+=plats
    output+="#POWERUPS x y type power\n"
    output+=str(n_ups)+"\n"
    output+=pups
    output+="#DOOR x y type nextmap\n"
    output+=str(n_doors)+"\n"
    output+=doors
    output+="#PLAYER POSITION\n"
    output+=plp

    print(output)
    
    
    no=4
    f=open(r"C:\Users\bharg\OneDrive\Desktop\pygame\easter\Maps\map%s.txt"%str(no).zfill(3))
    f.write(output)
    f.close()


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.image.save(disp,"Images/level.png")
            pg.quit()
            outputyo()
            

    disp.fill(-1)
    all_sprites.update()
    all_sprites.draw(disp)
    blocks.draw(disp)
    clicks()
    pg.display.flip()


