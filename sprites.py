import pygame as pg
from variables import *
import random
BOOST_POWER = 90

def convert(image):
    return image.convert_alpha()
    
class Player(pg.sprite.Sprite):
    def __init__(self, g):
        self.group = g.sprites
        pg.sprite.Sprite.__init__(self, self.group)
        self.g = g
        self.image = convert(main[0])
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = (width/2, height/2)
        self.pos = vec(width/2, height/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.m_count = 0
        self.facing_right = True
        self.mobhit_num = 0
        self.boost_mode = False
        self.hp_up = 24
        self.idle_count = 0
        self.attack_count = 0
    def update(self):
        hits = pg.sprite.spritecollide(self.g.player, self.g.platforms, False)
        if self.facing_right:
            self.image = convert(main[self.idle_count//3])
        else:
            self.image = convert(lmain[self.idle_count//3])
            
        self.idle_count += 1
        if self.idle_count == 12:
            self.idle_count = 0
        self.acc = vec(0, 3.6)

        self.keys = pg.key.get_pressed()
        if self.keys[pg.K_LEFT]:
            self.acc.x = -1.6
            if hits:
                self.image = convert(main_l[self.m_count//3])
            self.facing_right = False
            
        if self.keys[pg.K_RIGHT]:
            self.acc.x = 1.6
            if hits:
                self.image = convert(main_r[self.m_count//3])
            self.facing_right = True


        self.m_count += 1
        if self.m_count >= 6:
            self.m_count = 0

        self.acc.x += self.vel.x * friction
        self.vel += self.acc
        self.pos += self.vel + 0.5 *self.acc

        if self.pos.x > width:
            self.pos.x = 0

        if self.pos.x < 0:
            self.pos.x = width

        self.rect.midbottom = self.pos
        self.mask = pg.mask.from_surface(self.image)
        
        #PLAYER COLLISION WITH BOSSES AND MOBS
        playerboss_hit = pg.sprite.spritecollide(self.g.player, self.g.bosses, False, pg.sprite.collide_mask)
        playermob_hit = pg.sprite.spritecollide(self.g.player, self.g.mob1, False, pg.sprite.collide_mask)
        p_boss1hit = pg.sprite.spritecollide(self.g.player, self.g.boss_fires, False, pg.sprite.collide_mask)
        if self.boost_mode == False:
            if p_boss1hit or playermob_hit or playerboss_hit:
                self.g.player.pos.x += 10
                self.g.php = healths[self.mobhit_num //12]
                self.mobhit_num += 1
                
                if self.mobhit_num >= 60:
                    self.g.floor_num = -5
                    self.g.screen_move = True
                    self.g.gaming = False
        #BOOST HIT     
        boost_hit = pg.sprite.spritecollide(self.g.player, self.g.power_ups, True)
        if boost_hit:
            self.g.player.vel.y = -BOOST_POWER
            self.g.player.boost_mode = True

        #HEALTHUP HIT
        healthup_hit = pg.sprite.spritecollide(self.g.player, self.g.health_up, True)
        if healthup_hit:
            self.mobhit_num = 0
            self.g.php = healths[0]

        #PLAYER PLATFORM INTERACTION
        if self.vel.y > 0:
            hits = pg.sprite.spritecollide(self.g.player, self.g.platforms, False)
            if hits:
                if self.rect.bottom-40 <= hits[0].rect.top:
                    self.pos.y = hits[0].rect.top
                    self.vel.y = 0
                    self.boost_mode = False
                    if hits[0].kind == 'break':
                        self.g.break_tile = hits[0]
          
            bplat_hits = pg.sprite.spritecollide(self.g.player, self.g.boss_platforms, False)
            if bplat_hits:
                self.pos.y = bplat_hits[0].rect.top
                self.vel.y = 0
                self.boost_mode = False
                
        if self.g.break_tile is not None:
            self.g.break_tile.rect.y += 20
            if self.g.break_tile.rect.y > height:
                self.g.break_tile.kill()
        

    def jump(self):
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.g.platforms, False)
        self.rect.x -= 1
        if hits:
            if self.rect.bottom-40 < hits[0].rect.top:
                self.vel.y = -40

        bplat_hits = pg.sprite.spritecollide(self, self.g.boss_platforms, False)
        if bplat_hits:
            self.vel.y = -40

    def health(self):
        return healths[0]

    def shoot(self):
        Bullet(self.g, self.rect.centerx, self.rect.top, self.facing_right)
        
       
class Bullet(pg.sprite.Sprite):
    def __init__(self,game, x, y, facing_right):
        self.group = game.sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.group)
        self.g = game
        self.image = convert(bullet[0])
        self.rect = self.image.get_rect()
        self.rect.centerx = x+ 40
        self.rect.y = self.g.player.pos.y -105
        self.right = facing_right
        if self.right:
            self.speedx = 15
        else:
            self.image = convert(bullet[1])
            self.rect.centerx = x- 40
            self.speedx = -15

    def update(self):
        self.rect.x += self.speedx
    
        if self.right:
            if self.rect.x >= width:
                self.kill()
        else:
            if self.rect.x <= 0:
                self.kill()
        

class Boss(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.g = game
        self.image = convert(enem2)
        self.image.set_colorkey((0,0,0))
        self.pos = vec(width/2, height/2)
        self.rect = self.image.get_rect()      
        self.rect.x = width/2-60
        self.rect.y = 0
        self.boss_move = self.boss_move2 = 0
        self.portal = True
        self.change_pace = False
        self.move2 = False
        self.boss1_clock = pg.time.Clock()
        self.time = 150
        self.time2 = 270
        self.kind = ''
        self.hit_num = 0
        self.boss_music_playing = False
    def movement(self):
        if self.kind == 'boss1':
            if self.change_pace == False and self.move2 == False:
                self.rect.y += 3
                if self.rect.y >= height/2 -200 and self.portal == True:
                    self.change_pace = True
                    self.portal1 = FirePortal(self.g, self,- 70, self.rect.y)
                    self.portal2 = FirePortal(self.g, self,140, self.rect.y)
                    self.g.sprites.add(self.portal1)
                    self.g.sprites.add(self.portal2)
                    self.portal = False
                
            elif self.change_pace:
                self.rect.x += -3
                self.rect.y += 3
                if self.rect.y >= height/2 -100:
                    self.change_pace = False
                    self.move2 = True

            elif self.move2:
                if self.rect.x <= width/2 - 50:
                    self.rect.x += 3
                    
                else:
                    self.boss1_clock.tick(30)
                    self.time -= 1
                    self.time2 -= 1
            if self.time <= 0:
                self.image = convert(b1rest1)
                self.rect.y += 40
                bossplat_hit = pg.sprite.spritecollide(self.g.boss, self.g.platforms, False, pg.sprite.collide_mask)
                if bossplat_hit:
                    if self.rect.bottom-40 <= bossplat_hit[0].rect.top:
                        self.rect.bottom = bossplat_hit[0].rect.top


                bossplat_hit2 = pg.sprite.spritecollide(self.g.boss, self.g.boss_platforms, False, pg.sprite.collide_mask)
                if bossplat_hit2:
                    if self.rect.bottom-40 <= bossplat_hit2[0].rect.top:
                        self.rect.bottom = bossplat_hit2[0].rect.top
                        
                        
            if self.time2 <= 0:
                self.image = convert(enem2)
                self.time = 30
                if self.rect.y >= height/2 -200:
                    self.rect.y -= 3
                else:
                    self.time2 = 270
        
        elif self.kind == 'boss2':
            if self.time > 0:
                self.image = convert(boss2_move[self.boss_move//3])

            if self.boss_move == 21:
                self.boss_move = 0
            if self.boss_move2 == 6:
                self.boss_move2 = 0
            if self.rect.y < height/2-200:
                self.rect.y += 3
            else:
                self.boss1_clock.tick(30)
                self.time -= 1

            if self.time <= 0:
                if self.rect.y < self.g.player.rect.y-60:
                    self.rect.y += 35
                else:
                    self.image = convert(boss2_attack[self.boss_move//3])
                    
                if self.time <= -10:
                    if self.rect.x in list(range(-300,50)):
                        self.image = convert(boss2_finalattack)
                        self.rect.x -= 20
                    else:
                        self.image = convert(boss2_attack2[self.boss_move2//3])
                        self.boss_move2 += 1
                        self.rect.x -= 20

                    if self.rect.x < -450:
                        self.rect.x = width/2
                        self.rect.y = 0
                        self.time = 60
            self.boss_move += 1      

        hits = pg.sprite.groupcollide(self.g.bullets,self.g.bosses, True, False)
        if hits:
            self.g.bossh = bosshealth[self.hit_num//6]
            self.hit_num += 1

            if self.hit_num >= 30:
                self.g.show_health = False
                self.g.boss.rect.y = 0
                self.g.boss_kill = True
                self.g.screen_move = True
                self.hit_num = 0
                self.g.bossh = bosshealth[0]
                self.kill()
        self.mask = pg.mask.from_surface(self.image)
    def health(self):
        return bosshealth[0]
    
class FirePortal(pg.sprite.Sprite):
    def __init__(self, game, boss, x, y):
        pg.sprite.Sprite.__init__(self)
        self.boss = boss
        self.g = game
        self.x = x
        self.image = convert(b1_fireportal[0])
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = self.boss.rect.x + x
        self.rect.y = y
        Fire(self.g, self)
        Fire(self.g, self)
        
    def update(self):
        if self.boss.time <= 0:
            self.image = convert(prest)
        else:
            self.image = convert(b1_fireportal[1])
            if len(self.g.boss_fires)-2 <= 10:
                Fire(self.g, self)
                
        self.rect.x = self.boss.rect.x + self.x
        self.rect.y = self.boss.rect.y
        if self.g.boss_kill:
            self.kill()

class Fire(pg.sprite.Sprite):
    def __init__(self, game, portal):
        self.group = game.sprites, game.boss_fires
        pg.sprite.Sprite.__init__(self, self.group)
        self.portal = portal
        self.g = game
        self.image = convert(boss1_fire)
        self.rect = self.image.get_rect()
        self.rect.x = self.portal.rect.x
        self.rect.y = self.portal.rect.y
        self.xrand = random.randrange(-1500, 1500)
        
    def update(self):
        if self.xrand < 0:
            if self.rect.x > self.xrand:
                self.rect.x -= 3
        else:
            if self.rect.x < self.xrand:
                self.rect.x += 5
        self.rect.y += 5

        self.mask = pg.mask.from_surface(self.image)
        fireplat_hit = pg.sprite.groupcollide(self.g.platforms, self.g.boss_fires, False, True)
        fireplat_hit2 = pg.sprite.groupcollide(self.g.boss_platforms, self.g.boss_fires, False, True)
        

        
class Mob1(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.group = game.sprites, game.mob1
        pg.sprite.Sprite.__init__(self, self.group)
        self.mob1_mcount = 0
        self.g = game
        self.plat = plat
        self.image = convert(mob1_idle)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top+5
        self.left = False
        self.right = True
        

    def update(self):
        

        if self.rect.x < self.plat.rect.right - 150 and self.right:
            self.rect.x += 3
            self.image = convert(mob1r[self.mob1_mcount // 3])
            if self.rect.x >= self.plat.rect.right - 150:
                self.right = False
                self.left = True

        elif self.plat.rect.left - 100 < self.rect.x and self.left:
            self.rect.x -= 3
            self.image = convert(mob1l[self.mob1_mcount // 3])
            if self.plat.rect.left - 100 >= self.rect.x:
                self.left = False
                self.right = True

       
                        
        self.mask = pg.mask.from_surface(self.image)
        self.mob1_mcount += 1
        if self.mob1_mcount >= 60:
            self.mob1_mcount = 0


        #BUlLET HIT THE MOBS   
        mob1hit = pg.sprite.groupcollide(self.g.bullets, self.g.mob1, True, True)
        
            
class Tiles(pg.sprite.Sprite):
    def __init__(self, game, x, y, kind):
        self.group = game.sprites, game.platforms
        pg.sprite.Sprite.__init__(self,self.group)
        self.g = game
        self.kind = kind
        self.bo_p = False
        self.image = convert(panel1)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.reached = False
        self.break_tile = None
        if kind == 'normal':
            if random.randrange(100) < BOOST_PCT:
                Pow(self.g, self)

            if random.randrange(100) < mob1_pct:
                Mob1(self.g, self)

            if random.randrange(100) < healthup_pct:
                HealthUp(self.g, self)
        self.start = random.choice(['left', 'right'])

    def update(self):
        if self.g.floor_num >= 140:
            self.image = convert(panel2)
        if self.kind == 'moving':
            if self.start == 'left':
                if self.rect.x > 0 and self.reached == False:
                    self.rect.x -= 12
                    if self.rect.x <= 0:
                        self.reached = True
                else:
                    self.rect.x += 12
                    if self.rect.x >= width-100:
                        self.reached = False
        elif self.kind == 'break':
            self.image = convert(panel_break)
class BossTiles(pg.sprite.Sprite):
    def __init__(self, x, y): 
        pg.sprite.Sprite.__init__(self)
        self.image = convert(boss_panel)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
            
        
class Pow(pg.sprite.Sprite):
    def __init__(self, g, plat):
        self.group = g.sprites, g.power_ups
        pg.sprite.Sprite.__init__(self, self.group)
        self.g = g
        self.plat = plat
        self.image = convert(boost_up)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
        self.g.sprites.add(self)

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.g.platforms.has(self.plat):
            self.kill()

            
     
class HealthUp(pg.sprite.Sprite):
    def __init__(self, g, plat):
        self.group = g.sprites, g.health_up
        pg.sprite.Sprite.__init__(self, self.group)
        self.g = g
        self.plat = plat
        self.image = convert(health_up)
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5
        self.g.sprites.add(self)

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.g.platforms.has(self.plat):
            self.kill()

 
