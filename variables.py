import pygame as pg
#GEOMETRY
width = 720
height = 600

platform_y = [-30,-44,-56,-71,-85,-97]

bg = pg.image.load('img/bg11.png')
#PLAYER NAME
hero_name = ''

friction = -0.12

vec = pg.math.Vector2


#STARTING PLATFORMS
platform_list = [(0, height - 40),
                 (width/2-50, height *3/4),
                 (width/2, 350),
                 (width/2-100, 250),(100, 150),(170, 50)
                 ]

logo = pg.image.load('img/logo.png')

movingtile_prob = 24

stand = pg.image.load('img/idle2.png')
enem = pg.image.load('img/stand1.png')

#Platform1
panel1 = pg.image.load('img/Panel2.png')
panel_break = pg.image.load('img/break_plat.png')
panel2 = pg.image.load('img/Panel3.png')
#BOSS 1                           
enem2 = pg.image.load('img/boss1/Boss1.png')
boss_panel = pg.image.load('img/boss_plat4.png')
boss1_movement = [pg.image.load('img/boss1/Boss1.png'), pg.image.load('img/boss1/Boss2.png'),pg.image.load('img/boss1/Boss3.png'),pg.image.load('img/boss1/Boss4.png'),pg.image.load('img/boss1/Boss5.png'),pg.image.load('img/boss1/Boss6.png'),pg.image.load('img/boss1/Boss7.png'),pg.image.load('img/boss1/Boss8.png'),pg.image.load('img/boss1/Boss9.png'),pg.image.load('img/boss1/Boss10.png'),pg.image.load('img/boss1/Boss11.png'),pg.image.load('img/boss1/Boss12.png'),pg.image.load('img/boss1/Boss13.png'),pg.image.load('img/boss1/Boss14.png'),pg.image.load('img/boss1/Boss15.png'),pg.image.load('img/boss1/Boss16.png'),pg.image.load('img/boss1/Boss17.png'),pg.image.load('img/boss1/Boss18.png')]
b1_fireportal = [pg.image.load('img/boss1/fire1.png'), pg.image.load('img/boss1/fire1v2.png')]
bullet = [pg.image.load('img/Projectile2.png'), pg.image.load('img/Projectile3.png')]
boss1_clock = pg.time.Clock()
b1rest1 = pg.image.load('img/boss1/b1rest1.png')
b1rest2 = pg.image.load('img/boss1/b1rest2.png')
prest = pg.image.load('img/boss1/firerest.png')
boss1_fire = pg.image.load('img/boss1/fire2.png')

#BOSS'S HEALTH
bosshealth = [pg.image.load('img/bosshealthbar/bosshealth1.png'),pg.image.load('img/bosshealthbar/bosshealth2.png'),pg.image.load('img/bosshealthbar/bosshealth3.png'),pg.image.load('img/bosshealthbar/bosshealth4.png'),pg.image.load('img/bosshealthbar/bosshealth5.png'),pg.image.load('img/bosshealthbar/bosshealth6.png')]

#BOSS 2
boss2_move = [pg.image.load('img/boss2/GemBat1.png'),pg.image.load('img/boss2/GemBat2.png'),pg.image.load('img/boss2/GemBat3.png'),pg.image.load('img/boss2/GemBat4.png'),pg.image.load('img/boss2/GemBat5.png'),pg.image.load('img/boss2/GemBat6.png'),pg.image.load('img/boss2/GemBat7.png'),pg.image.load('img/boss2/GemBat8.png')]
boss2_attack = [pg.image.load('img/boss2/GemBat_Attack4.png'),pg.image.load('img/boss2/GemBat_Attack5.png'),pg.image.load('img/boss2/GemBat_Attack6.png'),pg.image.load('img/boss2/GemBat_Attack7.png'),pg.image.load('img/boss2/GemBat_Attack8.png'),pg.image.load('img/boss2/GemBat_Attack9.png'),pg.image.load('img/boss2/GemBat_Attack10.png')]
boss2_attack2 = [pg.image.load('img/boss2/GemBat_Attack11.png'),pg.image.load('img/boss2/GemBat_Attack12.png')]
boss2_finalattack = pg.image.load('img/boss2/GemBat_Attack18.png')
ngbat = [pg.image.load('img/boss2/ngbat1.png'),pg.image.load('img/boss2/ngbat2.png')]

#CHARACTER
main = [pg.image.load('img/main/Idle1.png'), pg.image.load('img/main/Idle2.png'),pg.image.load('img/main/Idle3.png'),pg.image.load('img/main/Idle4.png')]
lmain = [pg.image.load('img/main/leftIdle1.png'), pg.image.load('img/main/leftIdle2.png'),pg.image.load('img/main/leftIdle3.png'),pg.image.load('img/main/leftIdle4.png')]
main_r = [pg.image.load('img/main/R1.png'),pg.image.load('img/main/R2.png')]#,pg.image.load('img/main/R3.png'),pg.image.load('img/main/R4.png')]
main_l = [pg.image.load('img/main/L1.png'),pg.image.load('img/main/L2.png')]#,pg.image.load('img/main/L3.png'),pg.image.load('img/main/L4.png')]
main_attack = [pg.image.load('img/main/Attack_Hero_Final1.png'),pg.image.load('img/main/Attack_Hero_Final2.png'),pg.image.load('img/main/Attack_Hero_Final3.png'),pg.image.load('img/main/Attack_Hero_Final4.png'),pg.image.load('img/main/Attack_Hero_Final5.png'),pg.image.load('img/main/Attack_Hero_Final6.png'),pg.image.load('img/main/Attack_Hero_Final7.png')]
main_fhp = pg.image.load('img/healthbar/full.png')

#MOB1
mob1r = [pg.image.load('img/mobs/mob1/m1r (1).png'),pg.image.load('img/mobs/mob1/m1r (2).png'),pg.image.load('img/mobs/mob1/m1r (3).png'),pg.image.load('img/mobs/mob1/m1r (4).png'),pg.image.load('img/mobs/mob1/m1r (5).png'),pg.image.load('img/mobs/mob1/m1r (6).png'),pg.image.load('img/mobs/mob1/m1r (7).png'),pg.image.load('img/mobs/mob1/m1r (8).png'),pg.image.load('img/mobs/mob1/m1r (9).png'),pg.image.load('img/mobs/mob1/m1r (10).png'),pg.image.load('img/mobs/mob1/m1r (11).png'),pg.image.load('img/mobs/mob1/m1r (12).png'),pg.image.load('img/mobs/mob1/m1r (13).png'),pg.image.load('img/mobs/mob1/m1r (14).png'),pg.image.load('img/mobs/mob1/m1r (15).png'),pg.image.load('img/mobs/mob1/m1r (16).png'),pg.image.load('img/mobs/mob1/m1r (17).png'),pg.image.load('img/mobs/mob1/m1r (18).png'),pg.image.load('img/mobs/mob1/m1r (19).png'),pg.image.load('img/mobs/mob1/m1r (20).png')]
mob1l = [pg.image.load('img/mobs/mob1/m1l (1).png'),pg.image.load('img/mobs/mob1/m1l (2).png'),pg.image.load('img/mobs/mob1/m1l (3).png'),pg.image.load('img/mobs/mob1/m1l (4).png'),pg.image.load('img/mobs/mob1/m1l (5).png'),pg.image.load('img/mobs/mob1/m1l (6).png'),pg.image.load('img/mobs/mob1/m1l (7).png'),pg.image.load('img/mobs/mob1/m1l (8).png'),pg.image.load('img/mobs/mob1/m1l (9).png'),pg.image.load('img/mobs/mob1/m1l (10).png'),pg.image.load('img/mobs/mob1/m1l (11).png'),pg.image.load('img/mobs/mob1/m1l (12).png'),pg.image.load('img/mobs/mob1/m1l (13).png'),pg.image.load('img/mobs/mob1/m1l (14).png'),pg.image.load('img/mobs/mob1/m1l (15).png'),pg.image.load('img/mobs/mob1/m1l (16).png'),pg.image.load('img/mobs/mob1/m1l (17).png'),pg.image.load('img/mobs/mob1/m1l (18).png'),pg.image.load('img/mobs/mob1/m1l (19).png'),pg.image.load('img/mobs/mob1/m1l (20).png')]
mob1_idle = pg.image.load('img/mobs/mob1/m1idle.png')
mob1_pct = 10

#HEALTH SPRITES
healths = [pg.image.load('img/healthbar/full.png'),pg.image.load('img/healthbar/h3.png'),pg.image.load('img/healthbar/h4.png'),pg.image.load('img/healthbar/h5.png'),pg.image.load('img/healthbar/h6.png'),pg.image.load('img/healthbar/h7.png'),]

#Boost Powerup
BOOST_POWER = 60
BOOST_PCT  = 7 
boost_up = pg.image.load('img/powerups/boost2.png')
#HEALTH POWERUP
healthup_pct =  8
health_up = pg.image.load('img/powerups/healthup.png')

