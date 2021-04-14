from settings import *

class Spritesheet(pg.sprite.Sprite):
    def __init__(self,file):
        super().__init__()
        self.file =  pg.image.load(file).convert()
        
    
    def get(self,x,y,w,h,color):
        #self.file.set_colorkey()
        surf = pg.Surface((w,h))
        surf.set_colorkey(color)
        surf.blit(self.file,(0,0),[x,y,w,h])
        return surf
    
    def scale(self,x,y,w,h,color,scale=1):
        surf = self.get(x,y,w,h,color)
        surf = pg.transform.scale(surf,(int(w*scale),int(h*scale)))
        return surf




class Player(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        super().__init__()
        
        self.game = game
        self.sheet = Spritesheet('Images/player.png')
        self.image = self.sheet.get(0,0,64,64,(255,0,170))
        self.rect = self.image.get_rect()
        self.rect.topleft = [y*32-32,x*32-32]

        self.pos = vec(x,y)
        self.velx = vec()
        self.velx.from_polar((VEL,0))
        self.vely = vec()
        self.vely.from_polar((GVTM,GVTA))


        self.last_update = pg.time.get_ticks()
        self.last_update2 = pg.time.get_ticks()
        

        self.update_thres = 50
        self.update_thres2 = 200

        self.falling = True

        self.hitrect = self.rect.copy()
        self.hitrect.width = 32
        self.hitrect.center = self.rect.center

        self.hidden = False
        self.jumping = False
        self.vertical = False

        self.dir = 0
        self.ind = 0
        self.type =self.game.type
        

        
    def imagify(self):
        if self.hidden:
            return
        self.image = self.sheet.get(self.ind*64,self.type*64,64,64,(255,0,170))

        if self.dir:
            self.image = pg.transform.flip(self.image,True,False)

    def hide(self):
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))


    def unhide(self):
        self.imagify()

    def update(self):
        

        now = pg.time.get_ticks()
        
        # if self.player.falling:
        #     self.pos+=self.vely

        keys = pg.key.get_pressed()

        if now - self.last_update2 > self.update_thres2:
            if keys[pg.K_h] and self.game.hpbar.health:
                if self.hidden:
                    self.hidden = False
                    self.unhide()
                else:
                    self.hidden = True
                    self.hide()

            self.last_update2 = now

        if now - self.last_update > self.update_thres:
            
            if self.jumping:
                self.jumping = False
                self.falling = True
            

            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.pos+=self.velx
                self.dir = 0
                self.ind = (self.ind+1)%3
                
                
            elif keys[pg.K_LEFT] or keys[pg.K_a]:
                self.pos-=self.velx
                self.dir = 1
                self.ind = (self.ind+1)%3
            
            if keys[pg.K_SPACE] and self.game.jumpbar.health:
                jumpfx.play()
                self.pos-=self.vely * 2
                self.jumping = True
                
                
           
            if self.falling:
                self.pos+=self.vely
            
            if not self.game.hpbar.health:
                self.hidden = False
                self.unhide()

            
           
            self.imagify()
            self.rect.topleft = self.pos
            self.hitrect.center = self.rect.center

            self.last_update = now
            




class Platform(pg.sprite.Sprite):
    def __init__(self,x,y,w,h,game,dir=0,speed=0):
        super().__init__()

        self.image = pg.Surface((w,h))
        self.image.fill((0,255,0))
        self.image.set_colorkey((0,255,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y
        
        self.dir = dir
        self.speed = speed
        self.i = 0
        self.go = 1
        self.last_update = pg.time.get_ticks()
        self.update_thres = 100
        self.sheet = Spritesheet('Images/tiles.png')
        self.w = w
        self.imagify()
        self.playeron = False
        self.game = game

    def imagify(self):
        for i in range(self.w//32-1):
            if i==0:
                self.image.blit(self.sheet.get(rd.choice([0,1,2])*32,2*32,32,32,(255,242,0)),(32*i,0))
            else:
                self.image.blit(self.sheet.get(rd.choice([0,1,2])*32,0*32,32,32,(255,242,0)),(32*i,0))
        
        self.image.blit(self.sheet.get(rd.choice([0,1,2])*32,1*32,32,32,(255,242,0)),(32*(i+1),0))
        



    
    def update(self):
        now = pg.time.get_ticks()
        if not self.dir or now-self.last_update<self.update_thres:
            return

        if self.i ==self.speed:
            self.go -=1
        
        if self.i == -self.speed:
            self.go+=1


        self.i+=self.go
        if self.dir==2 or self.dir==3:
            self.rect.y += self.i
            if self.playeron:
                self.game.player.hitrect.bottom = self.rect.top
                self.game.player.rect.center = self.game.player.hitrect.center
                self.game.player.pos = self.game.player.rect.topleft
                self.game.player.vertical = True
            
        

        elif self.dir==1:
            self.rect.x += self.i

        self.last_update = now


        


    
    
    
    
class Lights(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.color = rd.choice(LIGHTS)
        self.sheet = Spritesheet('Images/laser.png')
        self.w = 32
        self.h = 32*36
        self.imagify()
        self.rect = self.image.get_rect()
        self.rect.x = rd.randint(100,WIDTH-150)
        self.staytime = rd.choice((250,300,350,500,700,900,1000,1500,1200,1700,1900,2000))
        self.last_update = pg.time.get_ticks()
        self.alpha = 0
        
    
    def imagify(self):
       x=rd.choice(range(10))
       y=rd.choice(range(4))

       self.image = self.sheet.get(x*32,y*32,32,32,(255,255,255))


       self.image = pg.transform.scale(self.image,(self.w,self.h))

       self.image = self.image.convert_alpha()


    def update(self):
        if self.alpha!=255:
            self.alpha+=5
            self.image.set_alpha(self.alpha)
        
        else:
            now = pg.time.get_ticks()
            if now-self.last_update>self.staytime:
                self.kill()
            



class HealthBar(pg.sprite.Sprite):
    def __init__(self,game,player,typ=0):
        super().__init__()
        self.health = 100
        self.w=100
        self.h=10
        self.image = pg.Surface((self.w,self.h))
        self.image.fill((0,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        if typ==0:
            self.rect.topleft= 500,100
        else:
            self.rect.topleft= 500,200
        self.color = GREEN
        self.game = game
        self.player = player
        self.type = typ



    def update(self):
        if self.type==0:
            if self.player.hidden:
                self.health-=1
        
        else:
            if self.player.jumping:
                self.health-=1

        if self.health<=0:
            self.health =0

        if self.health<=25:
            self.color = RED
        
        elif self.health<=50:
            self.color = YELLOW

        
        
        else:
            self.color = GREEN

        
        self.image.fill((0,0,0))
        pg.draw.rect(self.image,self.color,[0,0,self.health,self.h])
        if self.type==0:
            self.rect.topleft= WIDTH-120,10
        else:
            self.rect.topleft= WIDTH-120,35


    
class Camera(object):
    def __init__(self, width, height):
        self.state = pg.Rect(0, 0, width, height)
        
    def apply(self, target):
        return target.move(self.state.topleft)
    
    def camera_func(self,camera, target_rect):
        x = -target_rect.center[0] + WIDTH/2 
        y = -target_rect.center[1] + HEIGHT/2


        camera.topleft += (vec((x, y)) - vec(camera.topleft)) * 0.06 

        camera.x = max(-(camera.width-WIDTH), min(0, camera.x))
        camera.y = max(-(camera.height-HEIGHT), min(0, camera.y))

        self.state = camera

        
    def update(self, target):
        self.camera_func(self.state, target.rect)


class Map(pg.sprite.Sprite):
    def __init__(self,game):
        super().__init__()
        self.rows = 30
        self.columns = 30
        self.size = 32
        self.game = game
        self.mapid = self.game.mapid
        self.startpos = 0,0
    
    

    def create_map(self):
        file = open('Maps/map%s.txt'%(str(self.mapid).zfill(3)))
        lines = file.readlines()
        curline = 2
        n_plats = int(lines[1])
        for line in lines[curline:curline+n_plats]:

            r,c,w,d,s = map(int,line.split())
            plat = Platform(c*32,r*32,w*32,32,self.game,d,s)
            self.game.tiles.add(plat)
            self.game.all_sprites.add(plat)

        curline+=n_plats+1
        n_powers=int(lines[curline])
        curline+=1

        for line in lines[curline:curline+n_powers]:
            x,y,t,p = map(int,line.split())
            x,y=x*32+8,y*32+8
            pup = Powerup(x,y,t,p,self.game)
            self.game.powerups.add(pup)
            self.game.all_sprites.add(pup)

        curline+=n_powers+1
        n_doors = int(lines[curline])
        curline+=1

        for line in lines[curline:curline+n_doors]:
            x,y,t,to = map(int,line.split())
            x,y=x*32,y*32
            door = Door(x,y,t,to,self.game)
            self.game.doors.add(door)
            self.game.all_sprites.add(door)

        curline+=n_doors+1
        self.startpos = list(map(int,lines[curline].split()))




        file.close()



class Door(pg.sprite.Sprite):
    def __init__(self,x,y,typ,to,game):
        super().__init__()
        self.pos = y,x
        self.last_update = pg.time.get_ticks()
        self.update_thres = 500
        self.type = typ
        self.sheet = Spritesheet('Images/doors.png')
        self.game = game
        self.to = to
        self.ind = 0

        self.imagify()
        
    
    def imagify(self):
        self.image = self.sheet.get(self.ind*64,self.type*64,64,64,(255,0,119))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.hitrect = self.rect.copy()
        self.hitrect.width = 32
        self.hitrect.center = self.rect.center
    

    def update(self):
        now = pg.time.get_ticks()

        if now - self.last_update > self.update_thres:

            self.ind = (self.ind+1)%3
            self.imagify()

            self.last_update=now
    

    def travel(self):
        doorfx.play()
        self.game.mapid = self.to
        self.game.transition()
        self.game.pass_loop()
        


class Powerup(pg.sprite.Sprite):
    def __init__(self,x,y,typ,power,game):
        super().__init__()

        self.ind = 0
        self.last_update = pg.time.get_ticks()
        self.update_thres = 250
        self.type = typ
        self.sheet = Spritesheet('Images/powerups.png')
        self.pos = y,x
        self.game = game
        self.power = power

        self.imagify()
    
    def imagify(self):
        self.image = self.sheet.get(self.ind*16,self.type*16,16,16,(255,0,119))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos



    def update(self):
        now = pg.time.get_ticks()

        if now - self.last_update > self.update_thres:

            self.ind = (self.ind+1)%3
            self.imagify()

            self.last_update=now


    def collect(self):
        pickupfx[self.type].play()
        if self.type==0:
            self.game.hpbar.health+=self.power
            if self.game.hpbar.health>100:
                self.game.hpbar.health=100
            self.kill()
        
        else:
            self.game.jumpbar.health+=self.power
            if self.game.jumpbar.health>100:
                self.game.jumpbar.health=100
            self.kill()
        


class Image(pg.sprite.Sprite):
    def __init__(self,x,y,r,c):
        super().__init__()
        self.sheet = Spritesheet('Images/powerups.png')
        self.image = self.sheet.scale(c*16,r*16,16,16,(255,0,119),2)
        self.pos = x,y
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos


class Text(pg.sprite.Sprite):
    def __init__(self,x,y,msg,game,size,ind=0,color=BLUE):
        super().__init__()
        self.ind = ind 
        self.game = game
        self.msg = msg
        self.pos = x,y
        self.size = size
        self.color = color
        self.active = False
        

        self.update()

        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
    
    def update(self):
        if self.ind==5:
            self.color = BGCOLOR
        elif self.ind==6:
            self.color = YELLOW

        elif self.active:
                self.color = GRAY
        else:
                self.color = BLUE

        self.font = pg.font.Font(FONT,self.size)
        self.image = self.font.render(self.msg,True,self.color)

        
class Bar(pg.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.recreate()

  def recreate(self):
    w=rd.randint(1,100)
    h=rd.randint(1,200)
    x=rd.randint(0,WIDTH-w)
    y=rd.randint(0,h)
    #col=(rd.randint(0,255),rd.randint(0,255),rd.randint(0,255))
    col=rd.choice(LIGHTS)
    self.image = pg.Surface((w,h))
    self.image.fill(col)
    self.w = w
    self.h = h
    self.x = x
    self.y = y
    self.o = 0 if self.w>self.h else 1
    self.col = col
    self.rect = self.image.get_rect()
    self.last_update = pg.time.get_ticks()
    self.speed = rd.choice(BARSPEEDS)
    self.speed = rd.choice([-self.speed,self.speed])
    self.update_thres = 100
    self.rect.topleft = x,y
    self.image.set_alpha(100)
    

  def update(self):
    now = pg.time.get_ticks()

    if now - self.last_update > self.update_thres:
      
      if self.o:
        self.rect.y+=self.speed
      else:
        self.rect.x+=self.speed

      self.last_update = now

    if self.rect.x<-self.w or self.rect.x>WIDTH:
      self.recreate()

    if self.rect.y<-self.h or self.rect.y>HEIGHT:
      self.recreate()

class Disp(pg.sprite.Sprite):
    def __init__(self,x,y,game):
        super().__init__()
        self.msg = ""
        self.image = pg.Surface((24*32,4*32))
        self.w = 24*32
        self.h = 4*32
        self.rect = self.image.get_rect()
        self.rect.topleft = x,y
        
        self.color = GREEN
        self.size = 32
        self.last_update = pg.time.get_ticks()
        self.update_thres = 250

        self.last_update2 = pg.time.get_ticks()
        self.update_thres2 = 250

        self.game = game

    def update(self):
        self.font = pg.font.Font(FONT,self.size)
        self.image = self.font.render(self.msg,True,self.color)
    

    def yes(self,id):
        global GVTM
        if id==51:
            self.game.type = 1
        elif id==61:
            GVTM = 5
        elif id==62:
            GVTM = 15
        elif id==91:
            self.game.type =  2
    
  


    
    def evaluate(self):
        self.msg = self.msg.upper()
        if self.game.mapid in [51,61,62,91]:
            if self.msg in ["Y","YES","YEAH","YEP","YE","WHY NOT"]:
                self.yes(self.game.mapid)
            
            self.msg = ""

        if self.msg == ANSWERS[self.game.mapid]:
            self.game.passExit = True
            
            self.kill()

            self.game.transition()
            if self.game.mapid==10:
                self.game.success = True
                self.game.gameover()
            self.game.new_game()

            self.game.game_loop()
        
        else:
            self.msg = ""
        