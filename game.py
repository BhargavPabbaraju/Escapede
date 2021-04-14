from sprites import *






class Game:
    def __init__(self):
        self.window = window
        self.passExit = False
        self.success = False

        #####Variables
        self.exitinits()
        self.mapid = 1
        self.type = 0
        

    def exitinits(self):
        self.paused = False
        self.gameExit = False
        self.menuExit = False
        self.introExit = False
        self.overExit = False
        
        
        self.clock = pg.time.Clock()

        

        self.init_groups()


    def new_game(self):
        


        self.init_groups()

        self.last_update = pg.time.get_ticks()


        #####Map Creation
        self.map = Map(self)
        self.map.create_map()





        ####Player Creation
        self.player = Player(self,*self.map.startpos)
        self.all_sprites.add(self.player)
        self.hpbar = HealthBar(self,self.player)
        self.jumpbar = HealthBar(self,self.player,1)
        jmpimg = Image(WIDTH-155,20,2,0)
        hltimg = Image(WIDTH-155,-5,2,1)
        self.sticky_sprites.add(jmpimg)
        self.sticky_sprites.add(hltimg)
        self.sticky_sprites.add(self.hpbar)
        self.sticky_sprites.add(self.jumpbar)

        self.camera = Camera(32*30,32*30)
        
    
    def init_groups(self):
        #self.players = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.sticky_sprites = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.lights = pg.sprite.Group()
        self.aliens = pg.sprite.Group()
        self.doors = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.bars = pg.sprite.Group()


    def intro_draw(self):
        
        self.bars.update()
        self.bars.draw(self.window)
        self.all_sprites.draw(self.window)
    

    def gen_bars(self):
        for i in range(100):
            bar = Bar()
            self.bars.add(bar)

    def display_text(self,msg,x,y,color,size):
        font = pg.font.Font(FONT,size)
        text = font.render(msg,True,color)
        textRect = text.get_rect()
        textRect.topleft = x,y

        self.window.blit(text,textRect)
    

    def transition(self):
        for i in range(0,255,15):
            self.window.set_alpha(i)
            pg.display.update()
            self.clock.tick(60)
    

    def intro_loop(self):
        self.gen_bars()
        txts = ['ESCAPEDE',"Press a Key to Continue"]
        txt = Text(*INTROTEXTPOS[0],txts[0],self,72,5,BGCOLOR)
        self.all_sprites.add(txt)
        txt = Text(*INTROTEXTPOS[1],txts[1],self,32,1)

        self.all_sprites.add(txt)
        pg.mixer.music.play(-1)
        while not self.introExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.type == pg.KEYUP:
                    self.introExit = True
                    self.new_game()
                    self.game_loop()
            
            self.window.fill(1)
            self.intro_draw()
            pg.display.update()
    
    def update(self):
        
        self.all_sprites.update()
        self.sticky_sprites.update()
        self.camera.update(self.player)
    
    def lights_draw(self):
        now = pg.time.get_ticks()
        if not len(self.lights) and now-self.last_update>  1000:
            for i in range(rd.randint(1,NOLIGHTS[self.mapid])):
                l = Lights()
                self.lights.add(l)
                self.all_sprites.add(l)
            
            self.last_update = now



    def draw(self):
        self.lights_draw()
        
        for sprite in self.all_sprites:
            self.window.blit(sprite.image,self.camera.apply(sprite.rect))
        
        self.sticky_sprites.draw(self.window)

       
        
    

    def collide_rects(self,rec1,rec2):
        # if rec1.colliderect(rec2):
        #     return True

        if rec1.bottom>=rec2.top and rec1.bottom<=rec2.bottom and rec1.left>=rec2.left and rec1.right<=rec2.right:
            return True
        
        return False

    def check_bounds(self):
        #if self.player.hitrect.
        x = self.player.hitrect.x
        y = self.player.hitrect.y
        if x//32>36 or y//32>36 or x<-30 or y<-64:
            self.gameExit = True
            self.transition()
            self.gameover()

    
    def check_collisions(self):
        found = False
        self.player.vertical = False
        for tile in self.tiles:
            tile.playeron = False
            if self.collide_rects(self.player.hitrect,tile.rect):
                found = True
                self.player.hitrect.bottom = tile.rect.top
                self.player.rect.center = self.player.hitrect.center
                self.player.pos = self.player.rect.topleft
                self.player.falling = False  
                tile.playeron = True
                break

        if not found and not self.player.jumping and not self.player.vertical:
            self.player.falling = True
        
        
        if not self.player.hidden:
            for light in self.lights:
                if light.alpha==255 and self.player.hitrect.colliderect(light.rect):
                    hitfx.play()
                    self.transition()
                    self.gameExit = True
                    self.gameover()
                    break
            
        for powerup in self.powerups:
            if self.player.hitrect.colliderect(powerup):
                powerup.collect()
            

        for door in self.doors:
            if self.player.hitrect.colliderect(door.hitrect):
                door.travel()
        
        

        
    def overclicks(self):
        mouse = pg.mouse.get_pos()
        
        for txt in self.all_sprites:
            if txt.rect.collidepoint(mouse):
                txt.active = True
                clicks = pg.mouse.get_pressed()
                if clicks[0]:
                    if txt.ind==1:
                        self.mapid = 1
                        self.exitinits()
                        self.new_game()
                        self.game_loop()
                    elif txt.ind==2:
                        pg.quit()
                        quit()
            else:
                txt.active = False
                    

    def overdraw(self):
        
        self.bars.draw(self.window)
        self.all_sprites.draw(self.window)
        pg.display.flip()

    def gameover(self):
        self.init_groups()
        pg.mixer.music.stop()
        pg.mixer.music.load('Audio/overbgm.wav')
        pg.mixer.music.play(-1)

        txts=["Game Over","New Game","Quit"]
        txtss = ["Success","Play Again","Quit"]

        for i in range(len(txts)):
            if i==0:
                s=72
                if self.success:
                    txts = txtss
                txt = Text(*OVERTEXTPOS[i],txts[i],self,72,5)
            else:
                txt = Text(*OVERTEXTPOS[i],txts[i],self,48,i)
            
            self.all_sprites.add(txt)
        
        self.gen_bars()

        while not self.overExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
            
            
            self.window.fill(1)
            self.all_sprites.update()
            self.bars.update()
            self.overdraw()
            self.overclicks()

    


   

    def game_loop(self):
        self.passExit = False
        pg.mixer.music.stop()
        pg.mixer.music.load('Audio/bgm.wav')
        pg.mixer.music.play(-1)
        while not self.gameExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                
            
            self.window.fill(1)
            self.check_collisions()
            self.check_bounds()
            self.update()
            self.draw()

            pg.display.flip()
            self.clock.tick(60)
    
    def pass_draw(self):
        self.all_sprites.update()
        self.disp.update()
        self.all_sprites.draw(self.window)

    
    def pass_clicks(self):
        mouse = pg.mouse.get_pos()
        for let in self.all_sprites:
            if let.rect.collidepoint(mouse):
                let.active = True
                clks = pg.mouse.get_pressed()
                
        
                if clks[0]:
                    now = pg.time.get_ticks()
                    if now - self.disp.last_update > self.disp.update_thres:

                        if let.msg == "Enter":
                            self.disp.evaluate()
                        
                        elif let.msg == ">":
                            self.disp.msg = self.disp.msg[:-1]
                        
                        else:
                            self.disp.msg+=let.msg
                        self.disp.last_update = now
            
            else:
                let.active = False
    
    def pass_keys(self,event):
        if event.key == pg.K_RETURN or event.key == pg.K_KP_ENTER:
            self.disp.evaluate()
        elif event.key == pg.K_BACKSPACE:
            self.disp.msg = self.disp.msg[:-1]
        else:
            self.disp.msg += event.unicode.upper()
    
    def pass_loop(self):
        self.init_groups()

        pg.mixer.music.stop()
        pg.mixer.music.load('Audio/passbgm.wav')
        pg.mixer.music.play(-1)

        lets='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789>'
        x=288
        y=256
        for c in lets:
            let = Text(x,y,c,self,32,0)
            self.all_sprites.add(let)
            x+=32
            if x>512:
                x=288
                y+=32
        
        self.all_sprites.add(Text(x,y,"Enter",self,32,5))
        self.all_sprites.add(Text(64,512,"QUES: "+CLUES[self.mapid],self,32,6))
        self.disp = Disp(64,128,self)

        while not self.passExit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                
                if event.type == pg.KEYDOWN:
                    self.pass_keys(event)
                
            
            self.window.fill(1)
            pg.draw.rect(self.window,BGCOLOR,[32,64,24*32,4*32],width=3)
            self.window.blit(self.disp.image,self.disp.rect)
            self.pass_draw()
            self.pass_clicks()

            pg.display.flip()
            self.clock.tick(60)


            







game = Game()
game.intro_loop()



        
