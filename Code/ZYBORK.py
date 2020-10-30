import pygame
import time
import pyglet
import sys

# Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (29, 203, 107)
RED = (234, 9, 14)
GREY = (23, 23, 23)
# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
jumpedHowManyTimes=0
bouncingOffWall=False
boosting=False
positionYouAreFacing="right"
clock=clock = pyglet.clock.Clock()
pygameClock = pygame.time.Clock()
deathCounter=0
background=""


#Loading images quickly
image_cache = {}
def get_image(key):
  if not key in image_cache:
    image_cache[key] = pygame.image.load(key).convert_alpha()
  return image_cache[key]
def get_image_not_transparent(key):
  if not key in image_cache:
    image_cache[key] = pygame.image.load(key).convert()
  return image_cache[key]


#Changing scenes
def enterToContinue():
    global done
    pygame.event.clear()
    enterPressed=False
    while enterPressed==False:
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
                    enterPressed=True
            if event.type == pygame.QUIT:
                    done = True
                    pygame.quit()
                    sys.exit()

def levels(currentLevelNumber,xPositionOfPlayer,yPositionOfPlayer,levelToAppend,levelBackground):
  global current_level_no
  global level_list
  global active_sprite_list
  global jumpedHowManyTimes
  global bouncingOffWall
  global boosting
  global gravity
  global background
  global current_level
  global level_end_sound
  if current_level_no == currentLevelNumber and player.rect.x == xPositionOfPlayer and player.rect.y == yPositionOfPlayer:
    level_end_sound.play()
    background=get_image_not_transparent(levelBackground)
    
    level_list.append( levelToAppend(player) )
    current_level_no =currentLevelNumber+1
    current_level = level_list[current_level_no]
    player.rect.x = 0
    player.rect.y = 400
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
    pygame.init()
    player.rect.x = 0
    player.rect.y = 400
    active_sprite_list.add(player)
    jumpedHowManyTimes=2
    bouncingOffWall=False
    boosting=False
    gravity=True

class Player(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    width = 40
    height = 60
    self.image = get_image("images/mainGuyRight.png")
    self.rect = self.image.get_rect()
    self.change_x = 0
    self.change_y = 0
    self.level = None
  def update(self):
    global keys
    global jumpedHowManyTimes
    global movingDirection
    global bouncingOffWall
    global boosting
    global positionYouAreFacing
    global deathCounter
    global gravity
    # Gravity
    self.calc_grav()
    # Moving left and right
    self.rect.x += self.change_x
    if self.change_x>0:
      positionYouAreFacing="right"
    elif self.change_x<0:
        positionYouAreFacing="left"
    if bouncingOffWall==True:
            self.image = get_image("images/mainGuyBall.png")
    elif boosting==True:
            self.image = get_image("images/mainGuyBall.png")
    elif self.change_y>=0:
      if self.change_x>0:
        self.image = get_image("images/mainGuyMovingRight.png")
      elif self.change_x<0:
        self.image = get_image("images/mainGuyMovingLeft.png")
      elif positionYouAreFacing=="left":
        self.image = get_image("images/mainGuyLeft.png")
      elif positionYouAreFacing=="right":
          self.image = get_image("images/mainGuyRight.png")
    else:
      if positionYouAreFacing=="right":
          self.image = get_image("images/mainGuyJumpRight.png")
      else:
          self.image = get_image("images/mainGuyJumpLeft.png")
    spike_hit_list = pygame.sprite.spritecollide(self, self.level.spike_list, False)
    for spike in spike_hit_list:
        if self.change_x > 0:
            death_sound.play()
            self.rect.right = spike.rect.left
            player.rect.x = 0
            player.rect.y = 400
            self.change_y=0
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            deathCounter=deathCounter+1
            gravity=True
        elif self.change_x < 0:
            death_sound.play()
            self.rect.left = spike.rect.right
            player.rect.x = 0
            player.rect.y = 400
            self.change_y=0
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            deathCounter=deathCounter+1
            gravity=True
        else:
            death_sound.play()
            player.rect.x = 0
            player.rect.y = 400
            self.change_y=0
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            deathCounter=deathCounter+1
            gravity=True
    block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    booster_hit_list = pygame.sprite.spritecollide(self, self.level.booster_list, False)
    spike_hit_list = pygame.sprite.spritecollide(self, self.level.spike_list, False)
    for block in block_hit_list:
        for spike in spike_hit_list:
            if self.change_x > 0:
                death_sound.play()
                self.rect.right = spike.rect.left
                player.rect.x = 0
                player.rect.y = 400
                self.change_y=0
                jumpedHowManyTimes=2
                bouncingOffWall=False
                boosting=False
                deathCounter=deathCounter+1
                gravity=True
            elif self.change_x < 0:
                death_sound.play()
                self.rect.left = spike.rect.right
                player.rect.x = 0
                player.rect.y = 400
                self.change_y=0
                jumpedHowManyTimes=2
                bouncingOffWall=False
                boosting=False
                deathCounter=deathCounter+1
                gravity=True
            else:
                death_sound.play()
                player.rect.x = 0
                player.rect.y = 400
                self.change_y=0
                jumpedHowManyTimes=2
                bouncingOffWall=False
                boosting=False
                deathCounter=deathCounter+1
                gravity=True
        for booster in booster_hit_list:
            if positionYouAreFacing=="left":
                booster_sound.play()
                bouncingOffWall=False
                boosting=True
                self.change_x=-12
                self.change_y=0
                jumpedHowManyTimes=0
                gravity=False
            elif positionYouAreFacing=="right":
                booster_sound.play()
                bouncingOffWall=False
                boosting=True
                self.change_x=12
                self.change_y=0
                jumpedHowManyTimes=0
                gravity=False
        if self.change_x > 0:
            wall_bounce_sound.play()
            self.rect.right = block.rect.left
            bouncingOffWall=True
            self.change_x=-10
            self.change_y=-17.5
            jumpedHowManyTimes=0
            gravity=True
        elif self.change_x < 0:
            wall_bounce_sound.play()
            self.rect.left = block.rect.right
            bouncingOffWall=True
            self.change_x=10
            self.change_y=-17.5
            jumpedHowManyTimes=0
            gravity=True
    self.rect.y += self.change_y
    block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    for block in block_hit_list:
        spike_hit_list = pygame.sprite.spritecollide(self, self.level.spike_list, False)
        for spike in spike_hit_list:
            if self.change_y > 0:
                death_sound.play()
                self.rect.bottom = spike.rect.top
                jumpedHowManyTimes=2
                bouncingOffWall=False
                self.change_y=0
                player.rect.x = 0
                player.rect.y = 400
                self.change_y=0
                deathCounter=deathCounter+1
                gravity=True
            elif self.change_y < 0:
                death_sound.play()
                jumpedHowManyTimes=2
                bouncingOffWall=False
                self.rect.top = spike.rect.bottom
                self.change_y=0
                player.rect.x = 0
                player.rect.y = 400
                self.change_y=0
                deathCounter=deathCounter+1
                gravity=True
            else:
                death_sound.play()
                jumpedHowManyTimes=2
                bouncingOffWall=False
                self.change_y=0
                player.rect.x = 0
                player.rect.y = 400
                self.change_y=0
                deathCounter=deathCounter+1
                gravity=True
        if self.change_y > 0:
            self.rect.bottom = block.rect.top
            jumpedHowManyTimes=0
            bouncingOffWall=False
            self.change_y = 0
            gravity=True
        elif self.change_y < 0:
            self.rect.top = block.rect.bottom
    spike_hit_list = pygame.sprite.spritecollide(self, self.level.spike_list, False)
    for spike in spike_hit_list:
        if self.change_y > 0:
            death_sound.play()
            self.rect.bottom = spike.rect.top
            jumpedHowManyTimes=2
            bouncingOffWall=False
            self.change_y=0
            player.rect.x = 0
            player.rect.y = 400
            deathCounter=deathCounter+1
            gravity=True
        elif self.change_y < 0:
            death_sound.play()
            jumpedHowManyTimes=2
            bouncingOffWall=False
            self.rect.top = spike.rect.bottom
            self.change_y=0
            player.rect.x = 0
            player.rect.y = 400
            deathCounter=deathCounter+1
            gravity=True
        else:
            death_sound.play()
            jumpedHowManyTimes=2
            bouncingOffWall=False
            self.change_y=0
            player.rect.x = 0
            player.rect.y = 400
            deathCounter=deathCounter+1
            gravity=True
        self.change_y = 0
    spring_hit_list = pygame.sprite.spritecollide(self, self.level.spring_list, False)
    for spring in spring_hit_list:
        if self.change_y > 0:
            bounce_sound.play()
            self.rect.bottom = spring.rect.top
            bouncingOffWall=False
            jumpedHowManyTimes=2 #so you can't jump
            self.change_y=-25
        elif self.change_y < 0:
            self.rect.top = spring.rect.bottom
        else:
            pass
    booster_hit_list = pygame.sprite.spritecollide(self, self.level.booster_list, False)
    for booster in booster_hit_list:
      if positionYouAreFacing=="left":
          booster_sound.play()
          bouncingOffWall=True
          self.change_x=-12
          self.change_y=0
          jumpedHowManyTimes=0
          gravity=False
      elif positionYouAreFacing=="right":
          booster_sound.play()
          bouncingOffWall=True
          self.change_x=12
          self.change_y=0
          jumpedHowManyTimes=0
          gravity=False
  def calc_grav(self):
    global gravity
    if gravity==True:
      if self.change_y == 0:
          self.change_y = 0.5
      else:
          self.change_y += 1.3
    # See if we are on the ground. Not including the platforms
    if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
        self.change_y = 0
        self.rect.y = SCREEN_HEIGHT - self.rect.height
  def jump(self):
    global jumpedHowManyTimes
    global bouncingOffWall
    global gravity
    global jump_sound
    
    self.rect.y += 2
    platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
    self.rect.y -= 2
    gravity=True
    if jumpedHowManyTimes==0:
        jump_sound.play()
        
        self.change_y = -17.5
        jumpedHowManyTimes=jumpedHowManyTimes+1
        bouncingOffWall=False
        movingDirection="none"
        

        
        
        
    elif jumpedHowManyTimes==1:
        

        jump_sound.play()
        
      
        self.change_y = -17.5
        jumpedHowManyTimes=2
        bouncingOffWall=False
        movingDirection="none"
        
        
    elif len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
        jumpedHowManyTimes=0
        bouncingOffWall=False
        movingDirection="none"
  def go_left(self):
    self.change_x = -8
  def go_right(self):
    self.change_x = 8
  def stop(self):
    self.change_x = 0

class Platform(pygame.sprite.Sprite):
  def __init__(self, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(GREY)
    self.rect = self.image.get_rect()

class Spike(pygame.sprite.Sprite):
  def __init__(self, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
    self.image.fill(RED)
    self.rect = self.image.get_rect()

class Spring(pygame.sprite.Sprite):
  def __init__(self, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
  
    self.rect = self.image.get_rect()

class Booster(pygame.sprite.Sprite):
  def __init__(self, width, height):
    super().__init__()
    self.image = pygame.Surface([width, height])
  
    self.rect = self.image.get_rect()

class Level(object):
    def __init__(self, player):
        self.platform_list = pygame.sprite.Group()
        self.booster_list=pygame.sprite.Group()
        self.spike_list=pygame.sprite.Group()
        self.spring_list=pygame.sprite.Group()
        self.player = player
    #Update everything on this level
    def update(self):
        
        self.platform_list.update()
       
        self.spike_list.update()
        self.spring_list.update()

        
        
        
        
        
        
 
    def draw(self, screen):
        global background
        screen.blit(background,(0,0))
        """
        self.platform_list.draw(screen)
        self.booster_list.draw(screen)
        
        self.spike_list.draw(screen)
        self.spring_list.draw(screen)
        #"""
        
 
 


class Tutorial_01(Level):
    
 
    def __init__(self, player):
        
 
      
        Level.__init__(self, player)
 
 
        level = [
                 
                 [1000, 20, 0, 560]
                 
                 
                 
               
                 
                 
                 ]
 

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
       

        spikes = [[50, 40, 300, 520],
                  [50, 40, 600, 520],
               
                  
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
class Tutorial_02(Level):
    
 
    def __init__(self, player):
        
 
        
        Level.__init__(self, player)
 
        level = [
                 
                 [1000, 20, 0, 560]
                 
                 
                 
               
                 
                 
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
       

        spikes = [[250, 40, 350, 520],
                  
                  
                  
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
class Tutorial_03(Level):
    
 
    def __init__(self, player):
        
 
        
        Level.__init__(self, player)
 

        level = [
                 
                 [1000, 20, 0, 560],
                 [80, 55, 920, 395],
                 [720, 20, 0, 380]
                 
                 
                 
               
                 
                 
                 ]
 
       
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
       

        spikes = [
                  [80,20,720,380],
                  [80, 395, 920, 0],
                  
                 
                  
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
class Level_01(Level):
 
 
    def __init__(self, player):
    
 
        
        Level.__init__(self, player)
 

        level = [[1000, 20, 0, -10],
                 [400, 100, 900, 260],
                 [300, 20, 0, 250],
                 
                 [1000, 20, 0, 560]
                 
                 
                 
               
                 
                 
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
       

        spikes = [[240, 40, 300, 520],
                  [420, 20, 300, 250],
                  [400, 10, 900, 250],
                  [400,10,900,350]
                  
                 
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
        

        
        
class Level_02(Level):
    

 
    def __init__(self, player):

 
        
        Level.__init__(self, player)
 
        # Width, height, x and y
        level = [[1000, 20, 0, 590],
                 [20, 70, 100, 180],
                 [20, 20, 300, 350],
                 [65, 20, 320, 180],
                 [200, 20, 800, 180],
                 [1000, 20, 0, -19]
                 
                 
                
                
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[20,390,320,180],
                  [10, 20, 790, 180],
                  [100, 70, 0, 180],
                  [300, 80, 400, 0],
                  
                  
                  [700, 20, 320, 570]
                 
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
class Level_03(Level):

 
    def __init__(self, player):
  
 
        
        Level.__init__(self, player)
 
        # Width, height, x and y
        level = [[1000, 20, 300, 590],
                 [320, 60, 0, 570],
                 [20, 100, 300, 250],
                 [90, 20, 310, 200],
                 [80, 275, 550, 200],
                 [95, 20, 910, 290],
                  
                 
                 
                
                 [1000, 20, 0, -19]
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[1000, 20, 320, 570],
                  [10,50,300,200],
                 
                  [10, 20, 400, 200],
                  [10, 285, 540, 190],
                  [90, 10, 540, 190],
                  [90, 10, 540, 475],
                  
                 
                  [10, 20, 900, 290]
                  
                 
                 
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)

class Level_04(Level):
    
 
    def __init__(self, player):
  
 
        
        Level.__init__(self, player)
 
    
        level = [[1000, 20, 0, 590],
                 [20, 70, 200, 400],
                 [20, 100, 200, 150],
                 [200, 20, 800, 100],
                 
                 
                 
                 
                
                 [1000, 20, 0, -10]
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[20,460,180,10],
                  [20, 140, 200, 10],
                  [20, 160, 200, 250]
                  
                  
                 
                 
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
class Level_05(Level):

 
    def __init__(self, player):

 
        
        Level.__init__(self, player)
 
    
        level = [
                 [100, 20, 0, 480],
                 [5, 80 ,310, 340],
                 [150, 150 ,520, 10],
                 [100, 20, 900, 90],
                 
                 
                 
                 
                 
                
                 [1000, 20, 0, -10]
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[1000, 50, 0, 550],
                  [25, 80 ,280, 340],
                  
                  [20,150, 500, 10],
                  [20, 200, 500, 350],
                  [10, 20, 890, 90],
                
                  
                  
                 
                 
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
        springs=[]

        for spring in springs:
            block = Spring(spring[0], spring[1])
            block.rect.x = spring[2]
            block.rect.y = spring[3]
            block.player = self.player
            self.spring_list.add(block)
class Level_06(Level):
 
 
    def __init__(self, player):
        """ Create level 5. """
 
        
        Level.__init__(self, player)
 

        level = [[1000, 20, 0, 590],
                 [10, 20, 190, 400],
                 [150, 140, 300, 0],
                 [150, 140, 550, 0],
                 #[50, 140, 700, 0],
                 [200,140,800,0],
                 [50, 20, 950, 400],
                 
                 
                 
                 
                 
                
                 [1000, 20, 0, -10]
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [
                
                  [100, 140, 200, 0],
                  [100, 140, 450, 0],
                  [100, 140, 700, 0],
                  
                  
                  
                 
                 
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
        springs=[[750, 20, 200, 400]]

        for spring in springs:
            block = Spring(spring[0], spring[1])
            block.rect.x = spring[2]
            block.rect.y = spring[3]
            block.player = self.player
            self.spring_list.add(block)

class Level_07(Level):
    
 
    def __init__(self, player):
       
 
        
        Level.__init__(self, player)
 

        level = [[300, 20, 0, 590],
                 #[20, 150, 100, 150],
                 [10, 30, 200, 370],
                 [105, 170, 180, 0],
                 #[150, 20, 850, 150]
                 #[150, 10, 850, 590]
                 [60, 20, 940, 400],
                 [1000, 20, 0, -19]
                
                 
                 
                
                
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[510,50,200, 550],
                  [20, 400 ,180 ,0],
                  [20,50,285,0],
                  [80, 790, 500, 110],
                  [20, 350, 820, 0]
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
        springs=[[290, 20, 710, 570]]

        for spring in springs:
            block = Spring(spring[0], spring[1])
            block.rect.x = spring[2]
            block.rect.y = spring[3]
            block.player = self.player
            self.spring_list.add(block)
class Level_08(Level):
    def __init__(self, player):
        """ Create level 6. """
 
      
        Level.__init__(self, player)
 
   
        level = [
                 [1000, 10, 0, 590],
                 [150, 20, 530, 340],
                 
                 
                
                 
                 [1000, 20, 0, -19]
                
                 
                 
                
                
                 ]
 
      
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[10, 20, 205, 550],
                  [20, 240, 300, 0],
                  [20, 330, 300, 360],
                  [20, 80, 520, 0],
                  [20, 400, 520, 200],
                  [20, 150, 680, 0],
                  [20, 370, 680, 270],
                  [180, 30, 700, 580],
                  [20, 270, 880, 0],
                  [20, 230, 880, 420],
               
                 
                  ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
        springs=[[85, 20, 215, 550],
                 [200, 20, 320, 380],


                 ]

        for spring in springs:
            block = Spring(spring[0], spring[1])
            block.rect.x = spring[2]
            block.rect.y = spring[3]
            block.player = self.player
            self.spring_list.add(block)
    
 
    
class Level_09(Level):
    """ Definition for level 6. """
 
    def __init__(self, player):
        """ Create level 6. """
 
       
        Level.__init__(self, player)
 
     
        level = [
                 [300, 10, 0, 590],
                 [300, 10, 700, 590],
                 [550, 50, 200, 450],
                 [50, 60, 950, 175],
                
                 [20, 50, 300, 60],
                 [100, 20, 0, 70],
                 
                 [1000, 20, 0, -19]
                
                 
                 
                
                
                 ]
 
     
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[200, 10, 300, 590],
                  [10, 70, 190, 450],
                  [560, 10, 190, 440],
                  [10, 20, 870, 450],
                  [10, 20, 200, 500],
                  [100, 10, 600, 590],
                  [20, 200, 550, 0],
                  [10, 20, 190, 350],
                  [10, 20, 300, 350],
                  [10, 50, 320, 60],
                  [10, 20, 100, 70],
                  
                 
                 
                  ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
        springs=[[100, 10, 500, 590],
                 [120, 20, 750, 450],
                 [100, 20, 200, 350],

                ]

        for spring in springs:
            block = Spring(spring[0], spring[1])
            block.rect.x = spring[2]
            block.rect.y = spring[3]
            block.player = self.player
            self.spring_list.add(block)

class Level_10(Level):
    def __init__(self, player):
    
 
        
        Level.__init__(self, player)
 

        level = [[220, 20, 0, 590],
                 [600, 20, 400, 590],
                 [20, 120, 400, 280],
                 [100, 20, 420, 100],
                 [80, 20, 920, 120],
                 [1000, 20, 0, -19]
                
                 
                 
                
                
                 ]
 
        
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        spikes = [[20, 470, 190, 10],
                  [20, 190, 400, 400],
                  [20,180,400,100],
                  [170, 100, 630, 0],
                  [580,50,420,550],
                  [10,20,910,120],
                 
               
                 
                 
                 ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
        springs=[[180, 10, 220, 590]]

        for spring in springs:
            block = Spring(spring[0], spring[1])
            block.rect.x = spring[2]
            block.rect.y = spring[3]
            block.player = self.player
            self.spring_list.add(block)

 
    
class Level_11(Level):

 
    def __init__(self, player):

 
      
        Level.__init__(self, player)
 
        # Width, height, x and y
        level = [
                 [1000, 10, 0, 590],
               
                 [20,50,960,200],
                 [150, 20, 0, 230],
                 
                
                 
                 [1000, 20, 0, -19]
                
                 
                 
                
                
                 ]
        spikes = [[500, 20, 200, 380],
                 [500, 80, 200, 510],
                 [20, 120, 600, 0],
                 [20,80 ,600,300],
                 [20, 600, 980, 0],
                 [20, 150, 0, 0]
               
                 
                  ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
 

        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        boosters = [[1, 1, 200, 460],
                    [1, 1, 300, 100],
               
                 
                  ]
        for booster in boosters:
            block = Booster(booster[0], booster[1])
            block.rect.x = booster[2]
            block.rect.y = booster[3]
            block.player = self.player
            self.booster_list.add(block)
class Level_12(Level):

 
    def __init__(self, player):
  
 
 
        Level.__init__(self, player)
 
        # Width, height, x and y
        level = [
                 [1000, 10, 0, 590],
                 
                 [20, 30, 150, 430],
                 [150, 20, 700, 100],
                
                 
                
                 
                 [1000, 20, 0, -19]
                
                 
                 
                
                
                 ]
        spikes = [[5, 30, 145, 430],
                  [220, 200, 300, 0],
                  [20, 500, 680, 100],
                  [200, 20, 800, 400],
                  [300,20, 700, 580],
               
                 
                  ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
 
       
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        boosters = [[1, 1, 480, 260],
                    [1, 1, 750, 500]
             
                   
                    
               
                 
                  ]
        for booster in boosters:
            block = Booster(booster[0], booster[1])
            block.rect.x = booster[2]
            block.rect.y = booster[3]
            block.player = self.player
            self.booster_list.add(block)
class Level_13(Level):
 
 
    def __init__(self, player):
   
 
     
        Level.__init__(self, player)
 
       
        level = [
                 [1000, 10, 0, 590],
                 [200,20,650,100],

                 
                
                 
                
                 
                 [1000, 20, 0, -19]
                
                 
                 
                
                
                 ]
        spikes = [[20,480,650,120],
                  [20,500,980,0],
                  [150, 20, 830,300],
                  [180, 20, 670,580],

                  [200,20,200,325],
                  [150,50,250,550],
                  [20,300,0,0],
               
                 
                  ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
 
     
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        boosters = [[1, 1, 500, 400],
                    [1,1,150,200],
                    #[2,2,400,50],
                    
                    
               
                 
                  ]
        for booster in boosters:
            block = Booster(booster[0], booster[1])
            block.rect.x = booster[2]
            block.rect.y = booster[3]
            block.player = self.player
            self.booster_list.add(block)
        
class Level_14(Level):
  
 
    def __init__(self, player):
   
 
     
        Level.__init__(self, player)
 
   
        level = [[1000, 20, 0, 590],
                 [20, 50, 0, 300],
                 [20,120,700, 280],
                 [60, 20, 940, 100],
                 
                
                 
                 
                
                 [1000, 20, 0, -19]
                 ]
        spikes = [[20, 450,280,150],
                  [700,40,300, 560],
                  [20,130,520,0],
                  [20,300,0,0],
                  [300, 130,700,150],
               
                 
                  ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
 
     
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        boosters = [[1,1, 230, 100],
                    [1,1, 700, 30],
                    
                    
               
                 
                   ]
        for booster in boosters:
            block = Booster(booster[0], booster[1])
            block.rect.x = booster[2]
            block.rect.y = booster[3]
            block.player = self.player
            self.booster_list.add(block)
class Level_15(Level):
    
 
    def __init__(self, player):
        
 
     
        Level.__init__(self, player)
 

        level = [[400, 20, 0, 590],
                 [60,20, 940, 100],
                 
                 
                 
                 
                 [20, 100, 980, 400],
                 [1000, 20, 0, -19]
                 ]
        spikes = [[20, 310, 400, 290],
                  [20,450, 700, 0],
                  [580,20,420,590]
                  ]
        for spike in spikes:
            block = Spike(spike[0], spike[1])
            block.rect.x = spike[2]
            block.rect.y = spike[3]
            block.player = self.player
            self.spike_list.add(block)
 
     
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        boosters = [[1,1,200,450],
                    [1,1, 500,450],
                    [1,1, 680,500],
                    
                    
               
                 
                   ]
        for booster in boosters:
            block = Booster(booster[0], booster[1])
            block.rect.x = booster[2]
            block.rect.y = booster[3]
            block.player = self.player
            self.booster_list.add(block) 
def main():
    global bouncingOffWall
    global boosting
    global background
    global jumpedHowManyTimes
    global deathCounter
    global current_level_no
    global level_list
    global active_sprite_list
    global current_level
    global gravity
    global done
    global keys
    global player
    global jump_sound
    global wall_bounce_sound
    global bounce_sound
    global booster_sound
    global death_sound
    global level_end_sound
    #Main code
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.init()
    boosting=False
    
    movingDirection="left"
    gravity=True
    
 
 
  
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
    image=pygame.image.load("images/zyborkCaptionLogo.png")
    pygame.display.set_icon(image)
    pygame.mouse.set_visible(False)
 
    pygame.display.set_caption("ZYBORK")
    
   
    player = Player()
 
  
    level_list = []
    level_list.append( Tutorial_01(player) )
    medals={"gold_1":"no\n","no_death_1":"no\n","gold_2":"no\n","no_death_2":"no\n","gold_3":"no\n","no_death_3":"no\n"}
    creating_medal_data_file=open("medal_data.txt","a+")
    
    creating_medal_data_file.close()
    medal_data=open("medal_data.txt","r")
    medal_data_read=medal_data.readlines()

    
     
    if not medal_data_read:
      print("yo")
      medal_data.close()
      medal_data=open("medal_data.txt","w")
      
      
      
      for medal in medals:
        medal_data.write(medals[medal])
        
      medal_data.close()
    elif medal_data_read[0]=="yes\n" or medal_data_read[0]=="no\n":
       print("hello")
       medals["gold_1"]=medal_data_read[0]
       medals["no_death_1"]=medal_data_read[1]
       medals["gold_2"]=medal_data_read[2]
       medals["no_death_2"]=medal_data_read[3]
       medals["gold_3"]=medal_data_read[4]
       medals["no_death_3"]=medal_data_read[5]
       medal_data.close()
       print(medals)
    else:
      print("yoyo")
      medal_data.close()
      medal_data=open("medal_data.txt","w")
      
      
      
      for medal in medals:
        medal_data.write(medals[medal])
        
      medal_data.close()
      
    
      
  
    
 

    current_level_no = 0
    current_level = level_list[current_level_no]
    
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 0
    player.rect.y = 400
    active_sprite_list.add(player)
 
  
    done = False
 
  
    clock=clock = pyglet.clock.Clock()
    pygameClock = pygame.time.Clock()
    movingDirection="none"
    dt=0
    enterAppeared=True
    timeSinceEnterChanged=0
    passedTitleScreen=False
   
    passed_show_screen=False
    screen_one=False
    timeSinceScreenChanged=0
    jump_sound= pygame.mixer.Sound("Sounds/jump.wav")
    wall_bounce_sound= pygame.mixer.Sound("Sounds/wall_bounce.wav")
    text_sound=pygame.mixer.Sound("Sounds/text.wav")
    bounce_sound=pygame.mixer.Sound("Sounds/bounce.wav")
    booster_sound=pygame.mixer.Sound("Sounds/boost.wav")
    death_sound=pygame.mixer.Sound("Sounds/death.wav")
    level_end_sound=pygame.mixer.Sound("Sounds/level_end.wav")
    
    get_image("images/mainGuyLeft.png")
    get_image("images/mainGuyRight.png")
    get_image("images/mainGuyJumpRight.png")
    get_image("images/mainGuyJumpLeft.png")
    get_image("images/mainGuyBall.png")
    get_image("images/mainGuyMovingRight.png")
    get_image("images/mainGuyMovingLeft.png")
    logoEnter=pygame.image.load("images/logoEnter.png")
    logoNoEnter=pygame.image.load("images/logoNoEnter.png")
    enterToContinueImage=pygame.image.load("images/enterToContinue.png")
    
    time_medal=pygame.image.load("images/timeMedal.png")
    no_death_medal=pygame.image.load("images/noDeathMedal.png")
    background=get_image_not_transparent("images/backgroundTutorial1.png")
    get_image_not_transparent("images/backgroundTutorial2.png")
    get_image_not_transparent("images/backgroundTutorial3.png")
    get_image_not_transparent("images/level1.png")
    get_image_not_transparent("images/level2.png")
    get_image_not_transparent("images/level3.png")
    get_image_not_transparent("images/level4.png")
    get_image_not_transparent("images/level5.png")
    get_image_not_transparent("images/level6.png")
    get_image_not_transparent("images/level7.png")
    get_image_not_transparent("images/level8.png")
    get_image_not_transparent("images/level9.png")
    get_image_not_transparent("images/level10.png")
    get_image_not_transparent("images/level11.png")
    get_image_not_transparent("images/level12.png")
    get_image_not_transparent("images/level13.png")
    get_image_not_transparent("images/level14.png")
    screenOne=pygame.image.load("images/prolouge.png")
    screenTwo=pygame.image.load("images/prolouge0.5.png")
    
    prolouge1=pygame.image.load("images/prolouge1.png")
    prolouge2=pygame.image.load("images/prolouge2.png")
    prolouge3=pygame.image.load("images/prolouge3.png")
    prolouge4=pygame.image.load("images/prolouge4.png")
    prolouge5=pygame.image.load("images/prolouge5.png")
    prolouge6=pygame.image.load("images/prolouge6.png")
    prolouge7=pygame.image.load("images/prolouge7.png")
    prolouge8=pygame.image.load("images/prolouge8.png")
    prolouge9=pygame.image.load("images/prolouge9.png")
    prolouge10=pygame.image.load("images/prolouge10.png")
    prolouge11=pygame.image.load("images/prolouge11.png")
    cutscene1=pygame.image.load("images/cutscene1.png")
    cutscene2=pygame.image.load("images/cutscene2.png")
    cutscene3=pygame.image.load("images/cutscene3.png")
    cutscene4=pygame.image.load("images/cutscene4.png")
    cutscene5=pygame.image.load("images/cutscene5.png")
    cutscene55=pygame.image.load("images/cutscene5.5.png")
    cutscene6=pygame.image.load("images/cutscene6.png")
    cutscene7=pygame.image.load("images/cutscene7.png")
    cutscene8=pygame.image.load("images/cutscene8.png")
    cutscene9=pygame.image.load("images/cutscene9.png")
    cutscene10=pygame.image.load("images/cutscene10.png")
    cutscene11=pygame.image.load("images/cutscene11.png")
    ending=pygame.image.load("images/ending.png")
    ending1=pygame.image.load("images/ending1.png")
    ending2=pygame.image.load("images/ending2.png")
    ending3=pygame.image.load("images/ending3.png")
    ending35=pygame.image.load("images/ending35.png")
    
    zone_one=pygame.image.load("images/zoneOne.png")
    zone_two=pygame.image.load("images/zoneTwo.png")
    zone_three=pygame.image.load("images/zoneThree.png")
    zone_one_complete=pygame.image.load("images/zoneOneComplete.png")
    zone_two_complete=pygame.image.load("images/zoneTwoComplete.png")
    zone_three_complete=pygame.image.load("images/zoneThreeComplete.png")
    dable_featuring=pygame.image.load("images/dableFeaturing.png")
    dable_featuring_2=pygame.image.load("images/dableFeaturing2.png")
    chin_featuring=pygame.image.load("images/chinFeaturing.png")
    chin_featuring_2=pygame.image.load("images/chinFeaturing2.png")
    scientists_featuring=pygame.image.load("images/scientistsFeaturing.png")
    scientists_featuring_2=pygame.image.load("images/scientistsFeaturing2.png")
    cafrig_featuring=pygame.image.load("images/cafrigFeaturing.png")
    cafrig_featuring_2=pygame.image.load("images/cafrigFeaturing2.png")
    
    
    dialouge_box=pygame.image.load("images/dialougeBox.png")
    def quit_check():
      global done
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          done = True
          pygame.quit()
          sys.exit()
      
    
    def narratorDialouge(dialouge, yOfDialouge):
      
    
        myFont = pygame.font.Font("kadable-font/kadable-font.ttf", 40)
        for letter in range(len(dialouge)):
            text = myFont.render(dialouge[letter], True, (0,0,0))
            screen.blit(text,(150+ (myFont.size(dialouge[:letter])[0]), yOfDialouge))
            pygame.display.flip()
            pygameClock.tick(60)
            quit_check()
    def levelEndText(dialouge, yOfDialouge):
        myFont = pygame.font.Font("kadable-font/kadable-font.ttf", 40)
        for letter in range(len(dialouge)):
            text = myFont.render(dialouge[letter], True, (255,255,255))
            screen.blit(text,(50+ (myFont.size(dialouge[:letter])[0]), yOfDialouge))
            pygame.display.flip()
            pygameClock.tick(60)
            quit_check()
    def whiteText(dialouge,xOfDialouge,yOfDialouge,fontSize):
        text_sound.play()
       
        myFont = pygame.font.Font("kadable-font/kadable-font.ttf", fontSize)
        for letter in range(len(dialouge)):
            
            text = myFont.render(dialouge[letter], True, (255,255,255))
            screen.blit(text,(xOfDialouge+ (myFont.size(dialouge[:letter])[0]), yOfDialouge))
            pygame.display.flip()
            pygameClock.tick(50)
            quit_check()
    def blackText(dialouge,xOfDialouge,yOfDialouge,fontSize):
        text_sound.play()
        myFont = pygame.font.Font("kadable-font/kadable-font.ttf", fontSize)
        for letter in range(len(dialouge)):
            
            text = myFont.render(dialouge[letter], True, (0,0,0))
            screen.blit(text,(xOfDialouge+ (myFont.size(dialouge[:letter])[0]), yOfDialouge))
            pygame.display.flip()
            pygameClock.tick(60)
            quit_check()
    def two_image_switching(image_one,image_two,time):
        global pygameClock
        
        screen_one_is_on=True
        time_since_screens_changed=0
        passed_screens=False
        dt=0
        while passed_screens==False:
              time_since_screens_changed+=dt
              dt = pygameClock.tick()
              
              
              if time_since_screens_changed>=time:
                  if screen_one_is_on==True:
                      screen_one_is_on=False
                      time_since_screens_changed=0
                  else:
                      screen_one_is_on=True
                      time_since_screens_changed=0
              if screen_one_is_on==True:
                  
                  screen.blit(image_one,(0,0))
                  
              else:
                  
                  screen.blit(image_two,(0,0))
              pygame.display.flip()
              for event in pygame.event.get():
                if event.type==pygame.QUIT:
                  pygame.quit()
                  sys.exit()
                  
               
                  
                  
       
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                      passed_screens=True
                      
                      pygame.event.clear()
                      timeBeforeLevelsStart=pygame.time.get_ticks()
                      #print("now")
    
    
    
 
  
    myFont = pygame.font.Font("kadable-font/kadable-font.ttf", 40)
    image=pygame.image.load("images/kaddykinsLogo.png")
    screen.blit(image,(0,0))
    pygame.display.flip()
    whiteText("A game by",80,200,60)
    whiteText("Kadable",80,300,100)

    

    
    pygameClock.tick(0.5)
    screen.blit(enterToContinueImage,(0,0))
    whiteText("Press enter to advance dialouge, cutscenes",10,250,50)
    whiteText("and screens.",10,300,50)
    pygameClock.tick(5)
    whiteText("(Including this one)",380,400,30)
    enterToContinue()
    screen.blit(enterToContinueImage,(0,0))
    whiteText("Do you want to play cutscenes throughout ",50,50,50)
    whiteText("the game?",50,100,50)
    pygameClock.tick(5)
    whiteText("Y (Yes) or N (No)",100,300,100)
    play_cutscenes=True
    cutscene_question_answered=False

    
    
    
    while cutscene_question_answered==False:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
          
          if event.key==pygame.K_y:
            text_sound.play()
            play_cutscenes=True
            cutscene_question_answered=True
            
          elif event.key==pygame.K_n:
            text_sound.play()
            play_cutscenes=False
            cutscene_question_answered=True
          
            
    
    
    if play_cutscenes==True:
      while passed_show_screen==False:
            timeSinceScreenChanged+=dt
            dt = pygameClock.tick()
            
            
            if timeSinceScreenChanged>=350:
                if screen_one==True:
                    screen_one=False
                    timeSinceScreenChanged=0
                else:
                    screen_one=True
                    timeSinceScreenChanged=0
            if screen_one==True:
                
                screen.blit(screenOne,(0,0))
                pygame.display.flip()
            else:
                
                screen.blit(screenTwo,(0,0))
                pygame.display.flip()
            
            for event in pygame.event.get():
              if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
                

              if event.type == pygame.KEYDOWN:
                  if event.key==pygame.K_RETURN:
                      passed_show_screen=True
                      pygame.event.clear()

      screen.blit(prolouge1,(0,0))
      blackText("Welcome to The Chin Biggins show!!!!!",70, 165,40)
      #pygame.quit()
      pygameClock.tick(5)
      blackText("In today's episode I am going",70, 215,40)
      blackText("to demonstrate an...",70, 265,40)
      enterToContinue()
      pygame.display.flip()
      screen.blit(prolouge2,(0,0))
      blackText("INCREDIBLE!!",10, 140,40)
      #pygameClock.tick(5)
      blackText("REVOLUTIONARY!!!!!",10, 290,40)
      #pygameClock.tick(5)
      blackText("INGENIOUS!!!",600, 140,40)
      #pygameClock.tick(5)
      blackText("AMAZING!!!!!!!!!!",600, 290,40)
      #pygameClock.tick(5)
      blackText("BLOODY BRILLIANT!!!",600,440,40)
      #pygameClock.tick(5)
      blackText("FANTASTIC!!!!",10, 440,40)
      enterToContinue()
      screen.blit(prolouge3,(0,0))
      pygame.display.flip()
      blackText("...invention!!!!!!!!!!!!",300, 65,40)
      pygameClock.tick(5)
      blackText("ZYBORK!!!!!:",300, 115,40)
      blackText("the robot mechanic!!!",300, 165,40)
      enterToContinue()
      
      screen.blit(prolouge4,(0,0))
      blackText("\"Yesterday I recieved a mysterious package!!!!\"",10, 10,40)
      pygame.display.flip()
      enterToContinue()
      
      screen.blit(prolouge5,(0,0))
      pygame.display.flip()
      blackText("\"Inside of it was this slightly unnerving message!!!!!!!!!!\"",10, 10,40)
      pygameClock.tick(5)
      blackText("In this package you will find an incredible invention by me,",100,110,30)
      blackText("Professor Cafrig: ZYBORK, the robot mechanic!",100,160,30)
      pygameClock.tick(2)
      blackText("Broadcast this incredible demonstration of man's (my)",100,210,30)
      blackText("ingenuity on your show tommorrow and you'll be rewarded!",100,260,30)
      pygameClock.tick(2)
      blackText("Do NOT ignore this opportunity.",100,310,30)
      pygameClock.tick(2)
      blackText("Thanks! :) ",100,360,35)
      pygameClock.tick(2)
      blackText("From the ever beautiful, handsome, genius, mangnifecent, benevolent,",100,410,30)
      blackText("ncredible, witty, popular, likeable, lovable, sexy,awe-inspiring, compassionate,",0,460,30)
      blackText("uragous, all-knowing, all-powerful, Professor Cafrig.",0,510,30)
      #all-knowing, all-powerful,
      enterToContinue()
      
      screen.blit(prolouge6,(0,0))
      pygame.display.flip()
      blackText("\"It also contained a ZYBORK blueprint!!!!!!!!!!\"",70, 90,40)
      enterToContinue()
      
      screen.blit(prolouge7,(0,0))
      pygame.display.flip()
      blackText("Why did I accept this",300, 65,40)
      blackText("very-suspiciously-scam-sounding",300, 115,40)
      blackText("request??!!!!!!!!??!??",300, 165,40)
      pygameClock.tick(5)
      blackText("My reasoning is very simple.!..!!!.....!...",300, 215,40)
      enterToContinue()
      
      screen.blit(prolouge8,(0,0))
      pygame.display.flip()
      whiteText("RATINGS ARE DROPPING",400, 60,40)
      whiteText("THE CHANNEL IS THREATENING",70, 500,40)
      whiteText("TO CANCEL MY SHOW",70, 550,40)
      whiteText("I'M DESPERATE",10,240,40)
      #pygameClock.tick(5)
      enterToContinue()
      
      screen.blit(prolouge9,(0,0))
      pygame.display.flip()
      whiteText("I HAVE NO EMPLOYABLE SKILLS",10, 560,40)
      whiteText("I SPENT ALL MY SAVINGS ON A STUPID",170, 350,40)
      whiteText("DELIVERY DRONE THAT LOOKS LIKE MY FACE",170, 400,40)
      whiteText("MY RENT IS TWO MONTHS OVERDUE",100, 40,40)
      enterToContinue()
      #pygameClock.tick(2)
      
      screen.blit(prolouge10,(0,0))
      pygame.display.flip()
      whiteText("PLEASE DON'T STOP WATCHING",70, 215,50)
      enterToContinue()
    while passedTitleScreen==False:
        timeSinceEnterChanged+=dt
        dt = pygameClock.tick()
        
        
        if timeSinceEnterChanged>=350:
            if enterAppeared==True:
                enterAppeared=False
                timeSinceEnterChanged=0
            else:
                enterAppeared=True
                timeSinceEnterChanged=0
        if enterAppeared==True:
            
              
            
            screen.blit(logoEnter,(0,0))
            if medals["no_death_1"]=="yes\n":
              screen.blit(no_death_medal,(20,83))
            if medals["gold_1"]=="yes\n":
              screen.blit(time_medal,(132,83))
            if medals["no_death_2"]=="yes\n":
              screen.blit(no_death_medal,(809,83))
            if medals["gold_2"]=="yes\n":
              screen.blit(time_medal,(921,83))
            if medals["no_death_3"]=="yes\n":
              screen.blit(no_death_medal,(213,473))
            if medals["gold_3"]=="yes\n":
              screen.blit(time_medal,(699,473))
            pygame.display.flip()
        else:
            
            
            screen.blit(logoNoEnter,(0,0))
            if medals["no_death_1"]=="yes\n":
              screen.blit(no_death_medal,(20,83))
            if medals["gold_1"]=="yes\n":
              screen.blit(time_medal,(132,83))
            if medals["no_death_2"]=="yes\n":
              screen.blit(no_death_medal,(809,83))
            if medals["gold_2"]=="yes\n":
              screen.blit(time_medal,(921,83))
            if medals["no_death_3"]=="yes\n":
              screen.blit(no_death_medal,(213,473))
            if medals["gold_3"]=="yes\n":
              screen.blit(time_medal,(699,473))
            pygame.display.flip()
        for event in pygame.event.get():
          if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            
         
            
            
 
          if event.type == pygame.KEYDOWN:
              if event.key==pygame.K_RETURN:
                passedTitleScreen=True
                
                pygame.event.clear()
                timeBeforeLevelsStart=pygame.time.get_ticks()
                #print("now")
        
                
            
           
            
        
        
        
                                
    screen.blit(background,(0,0))
    screen.blit(dialouge_box,(100,20))
    blackText("ZYBORK can move using the arrow keys or W and",240,25,30)
    blackText("D!!!!!!!!!!!!!!!",240,75,30)
    enterToContinue()
    screen.blit(dialouge_box,(100,20))
    blackText("It can avoid obsacles by JUMPING to reach",240,25,30)
    blackText("anything in need of repair using the spacebar!!!!",240,75,30)
    enterToContinue()
    while not done:
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and movingDirection!="right":
            movingDirection="left"
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            movingDirection="right"
        else:
            movingDirection="none"
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                
                    
                if event.key == pygame.K_UP or event.key==pygame.K_SPACE or event.key==pygame.K_w:
                    
                    
                    player.jump()
             
            
                
                    
 
            
                
        if bouncingOffWall==True or boosting==True:
            pass
        elif movingDirection=="left":
            player.go_left()
        elif movingDirection=="right":
            player.go_right()
        elif movingDirection=="none":
            player.stop()
        else:
            pass
        
 
   
        active_sprite_list.update()
 
   
        current_level.update()

        
 
    
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH
 
 
        if player.rect.left < 0:
            player.rect.left = 0
   
        

        if current_level_no == 0 and player.rect.x == 945 and player.rect.y == 512:
            background=get_image_not_transparent("Images/backgroundTutorial2.png")
            level_list.append( Tutorial_02(player) )
            current_level_no =1
            current_level = level_list[current_level_no]
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list = pygame.sprite.Group()
            player.level = current_level
            pygame.init()
            player.rect.x = 0
            player.rect.y = 400
            
            active_sprite_list.add(player)
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            gravity=True
            screen.blit(background,(0,0))
            screen.blit(dialouge_box,(100,20))
            
            blackText("The ZYBORK can double-jump to avoid large",240,25,30)
            blackText("obstacles!!!!!",240,75,30)
            enterToContinue()
        if current_level_no == 1 and player.rect.x == 945 and player.rect.y == 512:
            background=get_image_not_transparent("Images/backgroundTutorial3.png")
            level_list.append( Tutorial_03(player) )
            current_level_no =2
            current_level = level_list[current_level_no]
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list = pygame.sprite.Group()
            player.level = current_level
            pygame.init()
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list.add(player)
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            gravity=True
            screen.blit(background,(0,0))
            screen.blit(dialouge_box,(100,20))
            blackText("It's agile frame allows it to bounce off of walls,",240,25,30)
            blackText("which also resets its double jump!!!!!",240,75,30)
            enterToContinue()
        
        if current_level_no == 2 and player.rect.x == 0 and player.rect.y == 332:
            
            
            
            deathCounter=0
            
            
            level_list.append( Level_01(player) )
            current_level_no =3
            current_level = level_list[current_level_no]
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list = pygame.sprite.Group()
            player.level = current_level
 
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list.add(player)
            background=get_image_not_transparent("Images/level1.png")
            if play_cutscenes==True:
              screen.blit(prolouge11,(0,0))
              blackText("WOW isn't that an incredible invention",300, 65,40)
              blackText("oh crap the channel has shortened",300, 115,40)
              blackText("my time slot I don't have enough",300, 165,40)
              blackText("time for a proper outro",300, 215,40)
              blackText("what do I do why didn't I plan",300, 265,40)
              blackText("for this please watch my next episod-",300, 315,40)
              enterToContinue()
              screen.blit(enterToContinueImage,(0,0))
              
              whiteText("Three years after this episode aired...",20,250,50)
              
              
              enterToContinue()
              
              
              screen.blit(cutscene1,(0,0))
              blackText("A space ship mysteriously appeared in a car park...",10,5,40)
              enterToContinue()
              
              screen.blit(cutscene2,(0,0))
              blackText("Stuck to the front of it was written this message...",10,5,40)
              pygameClock.tick(5)
              blackText("Remember me? It is I, Professor Cafrig,",190,120,30)
              blackText("the GREATEST inventor of all time! ",190,160,30)
              pygameClock.tick(2)
              blackText("This ship is my latest (and greatest)",190,200,30)
              blackText("invention. It is fully equipped to go to Mars,",190,240,30)
              blackText("featuring the now kinda famous ZYBORKs as",190,280,30)
              blackText("mechanics should anything go wrong.",190,320,30)
              pygameClock.tick(2)
              blackText("Imagine the glory! The power it will bring you!",190,360,30)
              pygameClock.tick(2)
              blackText("To be the first country to land on",190,400,30)
              blackText("Mars, through little effort of your own.",190,440,30)
              pygameClock.tick(2)
              blackText("Thank me later! :)",190,480,30)
              
              enterToContinue()
              screen.blit(cutscene3,(0,0))
              blackText("Two (possibly suicidal) scientists boarded the ship!",10,5,40)
              enterToContinue()
              text_sound.play()
              screen.blit(cutscene4,(0,0))
              pygame.display.flip()
              enterToContinue()
              text_sound.play()
              two_image_switching(cutscene5,cutscene55,350)
              
              
              screen.blit(cutscene6,(0,0))
              blackText("A scientist sent a ZYBORK to repair the engine.",10,5,40)
              pygame.display.flip()
              enterToContinue()
              text_sound.play()
              screen.blit(cutscene7,(0,0))
              
              pygame.display.flip()
              enterToContinue()
              text_sound.play()
              screen.blit(cutscene8,(0,0))
              
              pygame.display.flip()
              
              enterToContinue()
              text_sound.play()
              screen.blit(cutscene9,(0,0))
              pygame.display.flip()
              enterToContinue()
              text_sound.play()
              screen.blit(cutscene10,(0,0))
              pygame.display.flip()
              enterToContinue()
              screen.blit(cutscene11,(0,0))
              text_sound.play()
              pygame.display.flip()
              enterToContinue()
              
              screen.blit(enterToContinueImage,(0,0))
              whiteText("Can the last remaining ZYBORK reach the",20,250,50)
              whiteText("engine before the ship explodes?",20,300,50)
               
              enterToContinue()
              
            text_sound.play()  
            screen.blit(zone_one,(0,0))
            
            pygame.display.flip()
            enterToContinue()
            text_sound.play() 
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            timeBeforeWorldOneStarts=pygame.time.get_ticks()
        
        levels(3,0,202,Level_02,"Images/level2.png")
        levels(4,945,132,Level_03,"Images/level3.png")
        levels(5,945,242,Level_04,"Images/level4.png")
        levels(6,945,52,Level_05,"Images/level5.png")
       
        
        
        if current_level_no == 7 and player.rect.x == 945 and player.rect.y == 42:
            background=get_image_not_transparent("Images/level6.png")
            #screen.fill(BLACK)
            screen.blit(zone_one_complete,(0,0))
            timeForWorldOne=round((pygame.time.get_ticks()-(timeBeforeWorldOneStarts))/1000,2)
            #print(timeForWorldOne)
            worldOneDeaths=deathCounter
            #print("world one deaths:",worldOneDeaths)
            deathCounter=0
            
            #levelEndText("WORLD 1 COMPLETED",100)
            #time.sleep(0.2)
            blackText("Deaths: "+str(worldOneDeaths),50,170,55)
            pygameClock.tick(5)
            blackText("Time: "+str(timeForWorldOne)+" seconds",50,270,55)
            pygameClock.tick(5)
            medal_data=open("medal_data.txt","w")
            if worldOneDeaths==0:
              #pygameClock.tick(5)
              screen.blit(no_death_medal,(250,420))
              blackText("No Deaths Medal EARNED",350,420,55)
              medals["no_death_1"]="yes\n"
            else:
              blackText("No Deaths Medal MISSED",250,420,55)
            if timeForWorldOne<=15:
              #pygameClock.tick(5)
              screen.blit(time_medal,(250,500))
              blackText("Time Medal EARNED",350,500,55)
              
              medals["gold_1"]="yes\n"
            else:
              blackText("Time Medal MISSED: 15 secs",250,500,55)
            
              
            
            for medal in medals:
              medal_data.write(medals[medal])
              
            medal_data.close()
            
              
            pygame.display.update()
          
            
            
            
            
            
            
            
       
            level_list.append( Level_06(player) )
            current_level_no =8
            current_level = level_list[current_level_no]
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list = pygame.sprite.Group()
            player.level = current_level
 
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list.add(player)
            enterToContinue()
            text_sound.play() 
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            screen.blit(zone_two,(0,0))
            pygame.display.flip()
            enterToContinue()
            text_sound.play() 
            timeBeforeWorldTwoStarts=pygame.time.get_ticks()
            
        
        levels(8,945,352,Level_07,"Images/level7.png")
        levels(9,945,352,Level_08,"Images/level8.png")
        levels(10,945,542,Level_09,"Images/level9.png")
        levels(11,0,22,Level_10,"Images/level10.png")
        
        
        
 
     
        if current_level_no == 12 and player.rect.x == 945 and player.rect.y == 72:
            background=get_image_not_transparent("Images/level11.png")
            screen.blit(zone_two_complete,(0,0))
            timeForWorldTwo=round((pygame.time.get_ticks()-(timeBeforeWorldTwoStarts))/1000,2)
            print(timeForWorldTwo)
            #screen.fill(BLACK)
            #pygame.display.update()
            worldTwoDeaths=deathCounter
          
            deathCounter=0
            blackText("Deaths: "+str(worldTwoDeaths),50,170,55)
            pygameClock.tick(5)
            
            blackText("Time: "+str(timeForWorldTwo)+" seconds",50,270,55)
            pygameClock.tick(5)
            medal_data=open("medal_data.txt","w")
            if worldTwoDeaths==0:
              #pygameClock.tick(5)
              screen.blit(no_death_medal,(250,420))
              blackText("No Deaths Medal EARNED",350,420,55)
              medals["no_death_2"]="yes\n"
            else:
              blackText("No Deaths Medal MISSED",250,420,55)
            if timeForWorldTwo<=20:
              #pygameClock.tick(5)
              screen.blit(time_medal,(250,500))
              blackText("Time Medal EARNED",350,500,55)
              
              medals["gold_2"]="yes\n"
            else:
              blackText("Time Medal MISSED: 20 secs",250,500,55)
            medal_data=open("medal_data.txt","w")
            for medal in medals:
              medal_data.write(medals[medal])
              
            medal_data.close()
            
            
            
            
            
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
    
            level_list.append( Level_11(player) )
            current_level_no =13
            current_level = level_list[current_level_no]
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list = pygame.sprite.Group()
            player.level = current_level
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list.add(player)
            enterToContinue()
            text_sound.play() 
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            screen.blit(zone_three,(0,0))
            pygame.display.flip()
            enterToContinue()
            text_sound.play() 
            timeBeforeWorldThreeStarts=pygame.time.get_ticks()
        levels(13,0,182,Level_12,"Images/level12.png")
       
        if current_level_no == 14 and player.rect.x == 945 and 420<= player.rect.y <=580:
            level_end_sound.play()
            background=get_image_not_transparent("Images/level13.png")
            level_list.append( Level_13(player) )
            current_level_no =15
            current_level = level_list[current_level_no]
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list = pygame.sprite.Group()
            player.level = current_level
            pygame.init()
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list.add(player)
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            gravity=True

        levels(15,945,542,Level_14,"Images/level14.png")
        if current_level_no == 16 and player.rect.x == 945 and 1<= player.rect.y <=52:
            level_end_sound.play()
            background=get_image_not_transparent("Images/level15.png")
            level_list.append( Level_15(player) )
            current_level_no =17
            current_level = level_list[current_level_no]
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list = pygame.sprite.Group()
            player.level = current_level
            pygame.init()
            player.rect.x = 0
            player.rect.y = 400
            active_sprite_list.add(player)
            jumpedHowManyTimes=2
            bouncingOffWall=False
            boosting=False
            gravity=True
        if current_level_no==17 and player.rect.x==945 and player.rect.y==52:
            screen.blit(zone_three_complete,(0,0))
            timeForWorldThree=round((pygame.time.get_ticks()-(timeBeforeWorldThreeStarts))/1000,2)
            
            print(timeForWorldThree)
            worldThreeDeaths=deathCounter
            medal_data=open("medal_data.txt","w")
            blackText("Deaths: "+str(worldThreeDeaths),50,170,55)
            pygameClock.tick(5)
            blackText("Time: "+str(timeForWorldThree)+" seconds",50,270,55)
            pygameClock.tick(5)
            medal_data=open("medal_data.txt","w")
            if worldThreeDeaths==0:
              #pygameClock.tick(5)
              screen.blit(no_death_medal,(250,420))
              blackText("No Deaths Medal EARNED",350,420,55)
              medals["no_death_3"]="yes\n"
            else:
              blackText("No Deaths Medal MISSED",250,420,55)
            if timeForWorldThree<=20:
              #pygameClock.tick(5)
              screen.blit(time_medal,(250,500))
              blackText("Time Medal EARNED",350,500,55)
              
              medals["gold_3"]="yes\n"
            else:
              blackText("Time Medal MISSED: 20 secs",250,500,55)
            medal_data=open("medal_data.txt","w")
            for medal in medals:
              medal_data.write(medals[medal])
              
            medal_data.close()
            enterToContinue()
            if play_cutscenes==True:
                
                screen.blit(ending,(0,0))
                blackText("The ZYBORK reached the engine room.",10,5,40)
                pygame.display.flip()
                enterToContinue()
                text_sound.play()
                two_image_switching(ending1,ending2,200)
                text_sound.play()
                #enterToContinue()
                two_image_switching(ending35,ending3,350)
            
            screen.fill(BLACK)
            whiteText("Game by Kade Hennessy",200,250,50)
            enterToContinue()
            screen.fill(BLACK)
            whiteText("Featuring...",10,250,50)
            enterToContinue()
            text_sound.play()
            two_image_switching(dable_featuring,dable_featuring_2,350)
            text_sound.play()
            two_image_switching(chin_featuring,chin_featuring_2,350)
            text_sound.play()
            two_image_switching(scientists_featuring,scientists_featuring_2,350)
            text_sound.play()
            two_image_switching(cafrig_featuring,cafrig_featuring_2,350)
            text_sound.play()
            screen.fill(BLACK)
            secret_ending=0
            if medals["no_death_1"]=="yes\n":
              screen.blit(no_death_medal,(20,83))
              secret_ending=secret_ending+1
            if medals["gold_1"]=="yes\n":
              screen.blit(time_medal,(132,83))
              secret_ending=secret_ending+1
            if medals["no_death_2"]=="yes\n":
              screen.blit(no_death_medal,(809,83))
              secret_ending=secret_ending+1
            if medals["gold_2"]=="yes\n":
              screen.blit(time_medal,(921,83))
              secret_ending=secret_ending+1
            if medals["no_death_3"]=="yes\n":
              screen.blit(no_death_medal,(213,473))
              secret_ending=secret_ending+1
            if medals["gold_3"]=="yes\n":
              screen.blit(time_medal,(699,473))
              secret_ending=secret_ending+1
            whiteText("Thank You for playing :)",200,250,50)
            
            
            
            if secret_ending==6:
              enterToContinue()
              screen.fill(BLACK)
              whiteText("\"None of this makes sense, sir!\"",20,10,30)
              pygameClock.tick(1)
              whiteText("\"Why was there advertisements plastered all over the ship?\"",20,50,30)
              whiteText("\"Why did the ZYBORKs have to dodge what is apperently the ships own",20,90,30)
              whiteText("defense system, Zpikes, when trying to repair it?\"",20,130,30)
              whiteText("\"Why was video footage sent to TV stations?\"",20,170,30)
              pygameClock.tick(1)
              whiteText("\"Pipe down, I'm getting a call.\"",20,210,30)
              pygameClock.tick(2)
              whiteText("\"...\"",20,250,30)
              pygameClock.tick(2)
              whiteText("\"Yes?\"",20,290,30)
              pygameClock.tick(2)
              whiteText("\"What?! Are you sure?\"",20,330,30)
              pygameClock.tick(2)
              whiteText("\"...\"",20,370,30)
              pygameClock.tick(2)
              whiteText("\"Thanks for the info.\"",20,410,30)
              pygameClock.tick(1)
              whiteText("\"...\"",20,450,30)
              pygameClock.tick(1)
              
              whiteText("\"Employee, I just got a call from our Lead Engineer monitoring the ship.\"",20,490,30)
              pygameClock.tick(1)
              whiteText("\"The ship's engine was rigged to fail.\"",20,530,30)
              enterToContinue()
              
              
            else:
              whiteText("Try to get all the medals",200,310,50)
              whiteText("next time, eh?",200,370,50)
              
              enterToContinue()
              
            
            
            
            
            
            
            
              
            #enterToContinue()
            
            pygame.display.flip()
            enterToContinue()
              
            done = True
            pygame.quit()
            sys.exit()
                
        
        

        
        #current_level.draw(screen)   #when done delete thin
        screen.blit(background,(0,0)) #when done un comment this
        active_sprite_list.draw(screen)
        #print(player.rect.x,player.rect.y)
        
        
        
       
 

 

        clock.set_fps_limit(60)
        clock.tick()
        
        pygame.display.update()
      
       
        
 
       
        
      
    pygame.quit()
 
if __name__ == "__main__":
    main()


