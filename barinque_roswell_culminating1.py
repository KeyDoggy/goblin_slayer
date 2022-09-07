#Kai Barinque & Jordan Roswell
#01/19/2020
#barinque_roswell_culminating.py
#2D Survival Shooter
import pygame
import random
pygame.init()
pygame.display.set_caption("Goblin Slayer")
screen = pygame.display.set_mode((1000,1000))
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('download.png')
char = pygame.image.load('standing.png')
screenwidth = 950
screenheight = 1000
hitcount = 0
bulletcount = 1

#button colours
red = (150,0,0)
green = (0,150,0)
brightred = (255,0,0)
brightgreen = (0,255,0)
white = (255,255,255)
black = (0,0,0)





#Music and Sounds 
impactSound = pygame.mixer.Sound('goblindeath.wav')
deathSound = pygame.mixer.Sound('playerdeath.wav')
music = pygame.mixer.music.load('bgmusic.mp3')
pygame.mixer.music.play(-1) #-1 loops music infinitely

class player(object):
          
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpcount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)

        
    
        
    def draw(self,screen):
        if self.walkCount + 1 >= 27: #If greater than 27, will cause index error
            self.walkCount = 0
        if not(self.standing):
        
            if self.left:
                screen.blit(walkLeft[self.walkCount//3], (self.x,self.y))#// means integer division
                self.walkCount += 1
            elif self.right:
                screen.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.right:
                screen.blit(walkRight[0], (self.x, self.y))
            else:
                screen.blit(walkLeft[0], (self.x, self.y))
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)

    def hit(self):
        self.isJump = False #Fixes glitch where character resets into the ground after dying while in a jump
        self.jumpcount = 10
        self.x = 500 #Resets character to start after dying
        self.y = 605
        self.walkCount = 0
        
        #gameover
        pygame.draw.rect(screen,black,(0, 0, 1000, 950))
        font1 = pygame.font.SysFont('Pokemon GB.ttf', 200, True)
        text = font1.render ('GAME OVER', 1, (255,0,0))
        screen.blit(text, (500 - (text.get_width()/2),200))#text.get_width is built in pygame method
        pygame.display.update()
        


class PowerUp(object):
    gun = pygame.image.load('power.png')
    
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = 1
        self.visible = True
        self.hitbox = (self.x + 4, self.y + 11, 42, 52)

    def draw(self, screen):
        if self.visible == True:
            self.hitbox = (self.x + 4, self.y + 11, 42, 52)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)
            screen.blit(self.gun, (self.x, self.y))

    def hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health == 0:
                self.visible = False
                bulletcount = 2
        else:
            self.visible = False

         

       
        
   

class projectile(object):
    def __init__(self,x,y,radius,colour,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,screen):
        pygame.draw.circle(screen, self.colour, (self.x,self.y), self.radius)


class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):#Function for enemy
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = 900
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 1
        self.visible = True
        
        
    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))

                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)

    def hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health == 0:
                self.visible = False
        else:
            self.visible = False
        
        
        pass

        

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

class boss(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):#Function for enemy
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = 900
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 10
        self.visible = True
        
        
    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))

                self.walkCount += 1
            pygame.draw.rect(screen, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(screen, (0,255,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            #pygame.draw.rect(screen, (255,0,0), self.hitbox,2)

    def hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health == 0:
                self.visible = False
        else:
            self.visible = False
        
        
        pass

        

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

class FlyingGoblin(object):
    
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    def __init__(self, x, y, width, height, end):#Function for enemy
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = 900
        self.walkCount = 0
        self.vel = 3
        self.path = [self.x, self.end]
        self.hitbox = (self.x + 17, self.y + 11, 29, 52)
        self.health = 2
        self.visible = True

    def draw(self, screen):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                screen.blit(self.walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            else:
                screen.blit(self.walkLeft[self.walkCount//3], (self.x,self.y))

                self.walkCount += 1
            self.hitbox = (self.x + 17, self.y + 11, 29, 52)
            if self.health == 2:
                pygame.draw.rect(screen, (0,0,255), self.hitbox,2)

    def hit(self):
        if self.health > 0:
            self.health -= 1
            if self.health == 0:
                self.visible = False
        else:
            self.visible = False
        
        
        pass

        

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0


class Button(object):

    def __init__(self, colour, x,y,width,height, text=""):
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

def johnkey():
        #restart
        keydoggy = True
        pygame.draw.rect(screen,green,(150,400,250,150))
        mouse = pygame.mouse.get_pos()
        while keydoggy:
            for event in pygame.event.get():
                mouse = pygame.mouse.get_pos()
                if (150+250) > mouse[0] > 150 and (400+150) > mouse[1] > 400:
                    pygame.draw.rect(screen,brightgreen,(150,400,250,150))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameLoop()
                else:
                    pygame.draw.rect(screen,green,(150,400,250,150))
                text1 = pygame.font.SysFont('Pokemon GB.ttf', 65)
                text = text1.render ("RESTART",1,(255,255,255))
                screen.blit(text, (273 - (text.get_width()/2),450))
                pygame.display.update()

        #quit
                if (600+250) > mouse[0] > 600 and (400+150) > mouse[1] > 400:
                    pygame.draw.rect(screen,brightred,(600,400,250,150))
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        raise SystemExit
                else:
                    pygame.draw.rect(screen,red,(600,400,250,150))
                text2 = pygame.font.SysFont('Pokemon GB.ttf', 70)
                text = text2.render ("QUIT",1,(255,255,255))
                screen.blit(text,((600+(140/2)),450))
                pygame.display.update()


def redrawGameWindow():
    screen.blit(bg, (0,0))
    text = font.render("Score: " + str(hitcount), 1, (255, 255, 255))
    screen.blit(text, (850,36))
    guy.draw(screen)
    #PF.draw(screen)
    #bossMonster.draw(screen)
    #monster.draw(screen)

    for goblin in enemies:
        goblin.draw(screen)

    for future in scientists:
        future.draw(screen)

    for bullet in bullets:
        bullet.draw(screen)

def drawPowerUp():
    for powers in powerups:
        powers.draw(screen)


    pygame.display.update()
clock = pygame.time.Clock()
bulletnum = 0
bulletnum2 = 0
if bulletnum > 0:
    bulletnum +=1
if bulletnum > 3:
    bulletnum = 0




#Main loop. Program ends when this loop does. Should only have main character
font = pygame.font.SysFont('Pokemon GB.ttf', 32, True)#True for bold, second true for italicize
guy = player(500, 605, 64, 64) #x, y, dimensions of character
monster = enemy(random.randint(100,300),605,64,64,300)
bossMonster = boss(random.randint(100,200),605,64,64,300)
flying = FlyingGoblin(100,605,64,64,800)
DoubleShot = PowerUp(random.randint(100,800), 605, 64, 64)
bullets = []#List to append objects for spawning
enemies = []
scientists = []
powerups = []
pygame.time.set_timer(pygame.USEREVENT, random.randrange(3000,5000)) #Timer works in miliseconds so 1 second = 1000
pygame.time.set_timer(pygame.USEREVENT+2, 10000)
pygame.time.set_timer(pygame.USEREVENT+3, random.randint(45000, 60000))

def gameLoop():
    #Global variables so they don't have to be set as parameters
    global font
    global bulletnum
    global guy
    global monster
    global bossMonster
    global flying
    global PF
    global bullets
    global enemies
    global scientists
    global powerups
    global hitcount
   
    run = True
    while run:
        clock.tick(27) #27 FPS
        redrawGameWindow()
        drawPowerUp()



        keys = pygame.key.get_pressed()


            
        if keys[pygame.K_SPACE] and bulletnum == 0:
            if guy.left:
                facing = -1
            else:
                facing = 1
            if len(bullets) < 1: #How many bullets player can shoot at a time
                bullets.append(projectile(round(guy.x + guy.width//2), round(guy.y + guy.height//2), 6, (0,0,0), facing))#Use round because decimal number would mess up drawing. (0, 0, 0) means colour is black


            bulletnum = 1
        
            
        if keys[pygame.K_LEFT] and guy.x > guy.vel:#Moving left
            guy.x -= guy.vel
            guy.left = True #Use so that program doesn't get confused
            guy.right = False
            guy.standing = False
        elif keys[pygame.K_RIGHT] and guy.x < screenwidth - guy.width - guy.vel:#Moving right
            guy.x += guy.vel
            guy.left = False
            guy.right = True
            guy.standing = False
        else:#Not moving
            guy.standing = True 
            guy.walkCount = 0
        if not(guy.isJump):
            if keys[pygame.K_UP]:
                guy.isJump = True
                guy.right = False
                guy.left = False
                guy.walkCount = 0
        else:
            if guy.jumpcount >= -10:
                neg = 1
                if guy.jumpcount < 0:
                    neg = -1
                guy.y -= (guy.jumpcount ** 2) * 0.5 * neg
                guy.jumpcount -= 1
            else:
                guy.isJump = False
                guy.jumpcount = 10

            
        
        for goblin in enemies: #Collision for enemies in list
            if goblin.visible == True:
                if guy.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and guy.hitbox[1] + guy.hitbox[3] > goblin.hitbox[1]:#Collision
                    if guy.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2] and guy.hitbox[0] + guy.hitbox[2] > goblin.hitbox[0]:
                       deathSound.play()
                       guy.hit()
                       enemies = [] #Resets the list so when player chooses to restart game, there will be no enemies or bullets on screen
                       scientists = []
                       bullets = []
                       powerups = []
                       hitcount = 0 #In place so that when user wants to restart the game, the score goes back to 0
                       johnkey()
        #This one is relevant
        for future in scientists:
            if future.visible == True:
               if guy.hitbox[1] < future.hitbox[1] + future.hitbox[3] and guy.hitbox[1] + guy.hitbox[3] > future.hitbox[1]:#Collision
                        if guy.hitbox[0] < future.hitbox[0] + future.hitbox[2] and guy.hitbox[0] + guy.hitbox[2] > future.hitbox[0]:
                           deathSound.play()
                           guy.hit()
                           scientists = []
                           enemies = []
                           bullets = []
                           powerups=[]
                           hitcount = 0
                           johnkey()

        for powers in powerups:
            if powers.visible == True:
               if guy.hitbox[1] < powers.hitbox[1] + powers.hitbox[3] and guy.hitbox[1] + guy.hitbox[3] > powers.hitbox[1]:#Collision
                        if guy.hitbox[0] < powers.hitbox[0] + powers.hitbox[2] and guy.hitbox[0] + guy.hitbox[2] > powers.hitbox[0]:
                            powers.hit()
                            scientists = []
                            enemies = []
                            hitcount += 10



        if bulletnum > 0: #Used to stop bullets from sticking when fired
            bulletnum += 1
        if bulletnum > 3:
            bulletnum = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.USEREVENT:
                r = random.randint(0,5)
                spawnPointx = random.randint(0,700)
                if guy.x - 100 <= spawnPointx <= guy.x or guy.x <= spawnPointx <= guy.x + 100 and spawnPointx > 100:
                    spawnPointx -= 100 #Adjusts spawnpoint so goblin does not spawn on top of player
                elif guy.x - 100 <= spawnPointx <= guy.x or guy.x <= spawnPointx <= guy.x + 100 and spawnPointx < 700:
                    spawnPointx += 100
                    
                if r == 0:
                    enemies.append(boss(spawnPointx,605,64,64,950)) #Boss has a 1 in 5 chance to spawn
                else:
                    enemies.append(enemy(spawnPointx,605,64,64,950))
            if event.type == pygame.USEREVENT+2:
                Xspawn = random.randint(0,700)
                Yspawn = 430
                if guy.x - 50 <= Xspawn <= guy.x or guy.x <= Xspawn <= guy.x + 50 and Xspawn > 100:
                    Xspawn -= 100
                elif guy.x - 50 <= Xspawn <= guy.x or guy.x <= Xspawn <= guy.x + 50 and Xspawn < 700:
                    Xspawn += 100
                scientists.append(FlyingGoblin(Xspawn, Yspawn, 64, 64, 800))

            if event.type == pygame.USEREVENT+3:
                powerups.append(PowerUp(random.randint(100,800), 605, 42, 52))

        for bullet in bullets:
            for goblin in enemies:
                if goblin.visible == True:
                    if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:#Collision
                        if bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2] and bullet.x + bullet.radius > goblin.hitbox[0]:
                           impactSound.play()
                           goblin.hit()
                           hitcount += 1
                           bullets.pop(bullets.index(bullet))

            if bullet.x < 1000 and bullet.x > 0:
                bullet.x += bullet.vel 
            else:
                bullets.pop(bullets.index(bullet))#Deletes bullets if they go off screen
            if bullet.x > 1000 and bullet.x < 0:
                bullets.pop(bullets.index(bullet)) #Use to prevent error of code not finding bullet in list

            for future in scientists:
                if future.visible == True:
                    if bullet.y - bullet.radius < future.hitbox[1] + future.hitbox[3] and bullet.y + bullet.radius > future.hitbox[1]:#Collision
                        if bullet.x - bullet.radius < future.hitbox[0] + future.hitbox[2] and bullet.x + bullet.radius > future.hitbox[0]:
                           impactSound.play()
                           future.hit()
                           hitcount += 1
                           bullets.pop(bullets.index(bullet))

            if bullet.x > 1000 and bullet.x < 0:
                bullets.pop(bullets.index(bullet))

            

           

    


                     
gameLoop()
pygame.quit()
raise SystemExit
