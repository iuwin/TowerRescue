import pygame as pg
from variables import *
from sprites import *
import random


def convert(image):
    return image.convert_alpha()

class Game:
    def __init__(self):
        pg.init()
        self.window = pg.display.set_mode((width, height))
        pg.display.set_caption('TowerRescue')
        self.clock = pg.time.Clock()
        self.running = True
        self.floor_num = 0
        self.boss_kill = False
        self.screen_move = True
        self.jump_music = pg.mixer.Sound('music/jump5.wav')
        self.font_name = 'ARCADECLASSIC.ttf'
        self.waiting = True
        self.bg = convert(bg)
        self.mouse = pg.mouse.get_pos()
        self.player_list = []
        self.highest_score = 0
        
    def new(self):
        self.score = 0
        self.show_health = False
        self.break_tile = None
        #GROUPS
        self.sprites = pg.sprite.Group()
        self.mob1 = pg.sprite.Group()
        self.health_up = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.boss_fires = pg.sprite.Group()
        self.bosses = pg.sprite.Group()
        self.bats = pg.sprite.Group()
        self.minions = pg.sprite.Group()
        self.boss_platforms = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.boss = Boss(self)
        self.boss.kind = 'boss1'
        self.player = Player(self)
        self.php = self.player.health()
        self.bossh = self.boss.health()
        self.boss_p = BossTiles(0, height/2+268)
        
       
        for plat in platform_list:
            p = Tiles(self, *plat, 'normal')
            self.floor_num += 1

        self.run()


    def run(self):
        music = pg.mixer.music.load('music/final2.wav')
        pg.mixer.music.play(-1)
        self.gaming = True
        while self.gaming:
            self.clock.tick(30)
            self.events()
            self.update()
            self.draw()

    def update(self): #GAME UPPDATES
        self.sprites.update()
            
        #SECOND BOSS APPERANCE
        if self.floor_num in (60,61,62,63,64,65):
            self.boss_kill = False
            self.boss.kind = 'boss2'
            self.boss.time = 30
            self.floor_num += 1

        #BOSS APPERANCE
        if self.boss_kill == False:
            if self.floor_num >= 30:
                self.screen_move = False
                self.sprites.add(self.boss_p)
                self.boss_platforms.add(self.boss_p)
                self.show_health = True
                self.sprites.add(self.boss)
                self.bosses.add(self.boss)
                self.boss.movement()


        #GAME SCREEN MOVEMENT
        if self.screen_move == True:
            if self.player.rect.top <= height/4+22:
                self.player.pos.y += max(abs(self.player.vel.y), 2)
                for plat in self.platforms:
                    plat.rect.y += max(abs(self.player.vel.y), 2)
                    if plat.rect.top >= height:
                        plat.kill()
                        self.score += 10

                for m1 in self.mob1:
                    m1.rect.y += max(abs(self.player.vel.y), 2)
                    if m1.rect.top >= height:
                        m1.kill()

                        
                for b in self.boss_platforms:
                    b.kill()

        if self.player.rect.bottom > height:
            for boss in self.bosses:
                boss.kill()
                
            for platform in self.boss_platforms:
                platform.kill()
                
            for sprite in self.sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()

        #PLAYER FALLS DOWN      
        if len(self.platforms) == 0:
            self.floor_num = -5
            self.boss_kill = False
            self.screen_move = True
            self.gaming = False
            

        #ADD RANDOM PLATFORM TO THE GAME
        kind = 'normal'
        y = 0
        while len(self.platforms) < 6:
            if self.floor_num in (list(range(35,60))) or self.floor_num in (list(range(75, 100))) or self.floor_num in (list(range(150, 175))):
                kind = 'moving'
            else:
                if random.randrange(100) < 30:
                    kind = 'moving'
                elif 90 > random.randrange(100) > 30:
                    kind = 'normal'
                elif random.randrange(100) > 90:
                    kind = 'break'
            w = random.randrange(100,150)
            p = Tiles(self, random.randrange(40, width - (w*2)), platform_y[y], kind)
            self.floor_num += 1
            y += 1
    
    

    def events(self):#SOME IN-GAME EVENTS 
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.gaming:
                    self.gaming = False
                self.running = False
                self.waiting = False
                
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.jump_music.play()
                    self.player.jump()
            
                    
                if event.key == pg.K_DOWN:
                    self.player.shoot()
                   
    def draw(self):#MAIN BLITTING AND DRAWING
        self.window.blit(self.bg, (0,0))
        self.sprites.draw(self.window)
        self.drawText(str(self.score), 22, (255,255,255), width/2, 15)
        self.drawText('HI SCORE '+str(self.highest_score), 22, (255,255,255), 645, 15)
        self.window.blit(self.php, (0,-65))
        if self.player.rect.y < height:
            if self.show_health:
                self.window.blit(self.bossh, (520, 0))
        self.window.blit(self.player.image, self.player.rect)
        pg.display.flip()

    
    def Button(self,text,tcolor, color, hcolor, x, y, w, h, action):#GAME BUTTON
        self.mouse = pg.mouse.get_pos()
        self.click = pg.mouse.get_pressed()
        if x + w > self.mouse[0] > x and y + h > self.mouse[1] > y:
            pg.draw.rect(self.window, hcolor, (x, y, w, h))
            if self.click[0] == 1 and action != None:
                if action != None:
                    if action == False:
                        self.waiting = False
                    elif action == 'quit':
                        self.waiting = False
                        self.gaming = False
                        self.running = False

                    elif action != 'textfield' and action != False:
                        action()
        else:
            pg.draw.rect(self.window, color, (x, y, w, h))

        if action != 'textfield' and self.waiting == True:
            self.drawText(text, 25, tcolor, x+(w/2), y + (h/2)-10)

    #DATA STRUCTURE (FOR PLAYER SCORE MANAGEMENT)     
    def binSearch(self):#Binary Search
        if len(self.player_list) == 0:
            return 'add'
        else:
            self.player_list.sort()
            low, high = 0, len(self.player_list)-1
            while low <= high:
                mid = (low+high)//2
                midval = self.player_list[mid][0]

                if midval == hero_name:
                    return (True, mid)
                else:
                    if hero_name < midval:
                        high = mid - 1
                    elif hero_name > midval:
                        low = mid + 1
            return (False, None)
        
    def selectionSort(self):#Selection Sort
        if len(self.player_list) == 1:
            return
        
        for i in range(len(self.player_list)):
            max_index = i
            for j in range(i+1, len(self.player_list)):
                if self.player_list[max_index][1] < self.player_list[j][1]:
                    max_index = j
            self.player_list[i], self.player_list[max_index] = self.player_list[max_index], self.player_list[i]
    
    def quitEvent(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        
    def startScreen(self):#START SCREEN
        pg.mixer.music.stop()
        self.menu = True
        pg.display.update()
        while self.waiting:
            self.window.fill((200,255,75))
            self.drawText('Tower Jump!', 48, (100,150,120), width/2 +23, height/4+60)
            self.mouse = pg.mouse.get_pos()
            self.click = pg.mouse.get_pressed()
            self.clock.tick(30)
            self.quitEvent()
            #PLAY  BUTTON
            self.Button('New Game', (100,150,120), (230, 230, 230), (255,0,100), width/2-65, height/2-20, 150,40, self.addPlayer)

            if self.waiting == True:
                #HIGHSCORES BUTTON
                self.Button('High Score', (100,150,120),(230, 230, 230),(255,0,100),width/2-65,height/2+30, 150,40, self.scoreBoard)

                #CREDITS BUTTON
                self.Button('Credits',(100,150,120),(230, 230, 230),(255,0,100),width/2-65,height/2+80, 150,40, self.creditScreen)

                #EXIT BUTTON
                self.Button('Exit', (100,150,120),(230, 230, 230),(255,0,100),width/2-65,height/2+130, 150,40, 'quit')
            if self.menu:
                self.window.blit(logo, (270,10))
            pg.display.update()
            
    def addPlayer(self):#ADDING PLAYER SCREEN
        self.menu = False
        self.waiting = True
        global hero_name
        hero_name = ''
        past_heroname = list()
        d_count = 0
        while self.waiting:
            pg.display.flip()
            self.window.fill((200,255,75))
            self.drawText('Name Your Wizard!', 52, (100,150,120), width/2+25, height/4)
            self.mouse = pg.mouse.get_pos()
            self.click = pg.mouse.get_pressed()
            self.clock.tick(30)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        del past_heroname[len(past_heroname)-1:]
                        if len(past_heroname) == 0:
                            hero_name = ''
                        else:    
                            hero_name = past_heroname[-1]
                    else:   
                        hero_name += event.unicode
                        past_heroname.append(hero_name)

            self.drawText('Name ', 25, (100,150,120), width/2-90, height/2-75)
            self.Button(None, None, (255,255,255), (255,255,255), width/2-10, height/2-80, 180,35, 'textfield')
            self.drawText(hero_name, 20, (0,0,0), width/2+14 + (130/2), height/2-80 + (35/2)-10)
            self.Button('Jump!',(100,150,120),(230, 230, 230),(255,0,100),width/2-40, height/2+30, 120,60, False)
            pg.display.update()
            
    def creditScreen(self):#CREDIT SCREEN
        self.menu = False
        while self.waiting:
            pg.display.flip()
            self.window.fill((200,255,75))
            self.drawText('Developed by', 20, (100,150,120), width/2, height/2-200)
            self.drawText('Lourey James Dinolan', 20, (100,150,120), width/2, height/2-170)
            self.drawText('Erwin Canoy Amper', 20, (100,150,120), width/2, height/2-140)
            self.drawText('Special Thanks To', 20, (100,150,120), width/2, height/2-50)
            self.drawText('KidsCanCode', 20, (100,150,120), width/2, height/2-20)
            self.drawText('CraftPix', 20, (100,150,120), width/2, height/2+10)
            self.Button('Menu',(100,150,120),(230, 230, 230),(255,0,100), width/2-47, height*3/3.8, 100, 40, self.startScreen)
            self.quitEvent()
        
    def gameOver(self):#GAME OVER SCREEN
        music = pg.mixer.music.load('music/gameover.wav')
        pg.mixer.music.play(-1)
        found = self.binSearch()
        if found == 'add':
            self.player_list.append((hero_name, self.score))
            self.highest_score = self.score
        elif found[0] == True:
            if self.score >= self.player_list[found[1]][1]:
                self.player_list[found[1]] = (hero_name, self.score)
        elif found[0] == False:
            self.player_list.append((hero_name, self.score))
        self.selectionSort()
        self.highest_score = self.player_list[0][1]
        with open('scores.txt', 'w') as wf:
            for player in self.player_list:
                wf.write(str(player)+'\n')
                
        self.window.fill((200,255,75))
        while self.waiting:
            pg.display.flip()
            self.drawText(str(self.score), 48, (100,150,120), width/2 , height/3)
            self.drawText('You  Fail', 48, (100,150,120), width/2 , height/4.3)
            self.drawText('However try again! Life is full of challenges', 24, (100,150,120), width/2, height*3/6)
            self.drawText('You just need to bust through them to reach the top', 24, (100,150,120), width/2, height*3/5.4)
            self.Button('Play Again',(100,150,120),(230, 230, 230),(255,0,100), width/2-210, height*3/4.5, 140, 40, False)
            self.Button('Menu',(100,150,120),(230, 230, 230),(255,0,100), width/2+90, height*3/4.5, 140, 40, self.startScreen)
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    self.waiting = False
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

    def drawText(self, text, size, color, x,y):#MAKING TEXTS
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x,y)
        self.window.blit(text_surface, text_rect)

    def scoreBoard(self):#SCOREBOARD SCREEN
        self.menu = False
        ygap = 50
        xgap = 100
        printed = False
        self.waiting = True
        self.window.fill((200,255,75))
        while self.waiting:
            pg.display.flip()
            self.quitEvent()
            self.drawText('Score Board', 48, (100,150,120), width/2 , height/4-100)
            if printed == False:
                for player in self.player_list:
                    self.drawText(player[0], 20, (100,150,120), width/2 -xgap, height/7+ygap)
                    self.drawText(str(player[1]), 20, (100,150,120), width/2+xgap , height/7+ygap)
                    ygap += 40
                    printed = True
            self.Button('Menu',(100,150,120),(230, 230, 230),(255,0,100), width/2-55, height*3/3.5, 100, 40, self.startScreen)


            
def main():#MAIN
    game = Game()
    with open('scores.txt', 'r') as rf:
        for player in rf.readlines():
            game.player_list.append(eval(player))
        if len(game.player_list) != 0:
            game.highest_score = game.player_list[0][1]
##    game.startScreen()
    while game.running:
        game.startScreen()
        game.waiting = True
        game.new()
        game.gameOver()
        
    pg.quit()
main()
