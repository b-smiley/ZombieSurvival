# Zombie Survival Game
# Game created by - B.S - 12/27/2021
# Survive the hoard of zombies for as long as possible!

# Imports
from cgitb import small
from turtle import title
import pygame,sys,random,time
from math import atan2,degrees,pi
from pygame.locals import *

# Initializing 
pygame.init()

# Frames Per Second Settings
fps = 60  
framesPerSec = pygame.time.Clock()

# Colors 
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
black = (0,0,0)
white = (255,255,255)
grey = (189, 184, 183)

# Zombie and Human Images
zNorth = "Photos\zNorth.png"
zSouth = "Photos\zSouth.png"
zEast = "Photos\zEast.png"
zWest = "Photos\zWest.png"
zpp = "Photos\\posxposy.png"
zpn = "Photos\posxnegy.png"
znp = "Photos\\negxposy.png"
znn = "Photos\\negxnegy.png"
pN = "Photos\\NorthPlayer.png"
pE = "Photos\EastPlayer.png"
pS = "Photos\SouthPlayer.png"
pW = "Photos\WestPlayer.png"

zombie_start_image = pygame.image.load(zNorth) # Starting Image
player_start_image = pygame.image.load(pN) # Starting Image
bullet_image = pygame.image.load("Photos\\Bullet.png")
background = pygame.image.load("Photos\\Background.png")
game_over_bg = pygame.image.load("Photos\GameOver.png")
rule1_img = pygame.image.load("Photos\\rule1.png")
rule2_img = pygame.image.load("Photos\\rule2.png")
rule3_img = pygame.image.load("Photos\\rule3.png")

# Fonts
small_font = pygame.font.SysFont("Times New Roman",30)
medium_font = pygame.font.SysFont("Times New Roman",60)
large_font = pygame.font.SysFont("Times New Roman",100)

# Screen Setup
desktops=pygame.display.get_desktop_sizes()
primary_desktop = desktops[0]
screenwidth = primary_desktop[0]
screenheight = primary_desktop[1] - 50 # -50 Pixels just to show the tab on the screen, Without this it is fullscreen
sc_x = screenwidth/2
sc_y = screenheight/2
sc = (sc_x,sc_y)
screen = pygame.display.set_mode((screenwidth,screenheight)) 
screen.fill(white)
pygame.display.set_caption("Zombie Survival")

# Additional Variables
score = 0
ammo = 10 
spawn_amount = 1
zombie_spawn = {
"n":(random.randint(0,screenwidth),0),
"s":(random.randint(0,screenwidth),screenheight),
"e":(screenwidth, random.randint(0,screenheight)),
"w":(0,random.randint(0,screenheight)),
}

# Chracter Classes

class Zombie(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.image = zombie_start_image        
        self.rect = self.image.get_rect(center=position)
        self.rect.center = (position)  
        self.position = pygame.math.Vector2(position)
        self.speed = 2
        
        #Direction depends on the random spawn key, postion depends on random spawn coordinates along the key.

    def move(self,human):
        human_position = human.rect.center
        direction = human_position - self.position
        velocity = direction.normalize() * self.speed 
        # Normalizes the vector to have a hypotenuse length of 1
        # Angle of hypotenuse remains the same
        # Direction * Speed = Velocity
        
        self.position += velocity
        self.rect.topleft = self.position
        
        hx = human_position[0]
        hy = human_position [1]
        zx = self.position[0]
        zy = self.position[1]
        dx = hx - zx
        dy = hy - zy
        rads = atan2(-dy,dx) # Pygame uses flips y-axis, use -dy
        rads %= 2*pi
        degs = round(degrees(rads)) 
        
        # Broke up the unit circle to make the zombie pngs change
        if degs in range(0,15):
            self.image = pygame.image.load(zWest)
        if degs in range(16,75):
            self.image = pygame.image.load(zpp)
        if degs in range(76,105):
            self.image = pygame.image.load(zSouth)
        if degs in range(106,165):
            self.image = pygame.image.load(znp)
        if degs in range(166,195):
            self.image = pygame.image.load(zEast)
        if degs in range(196,255):
            self.image = pygame.image.load(znn)
        if degs in range(256,285):
            self.image = pygame.image.load(zNorth)
        if degs in range(286,345):
            self.image = pygame.image.load(zpn)
        if degs in range(346,360):
            self.image = pygame.image.load(zWest)
        
    def update(self,human):
        self.move(human)

class Human(pygame.sprite.Sprite):
    def __init__(self,position):
        super().__init__()
        self.image = player_start_image
        self.rect = self.image.get_rect(center=position)
        self.position = pygame.math.Vector2(position)
        self.velocity = pygame.math.Vector2(sc) # Should start the player at the center of the game
        self.speed = 4
        self.direction = "n" # player_start_image starts  with pN

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Using the typical "aswd" movement combination
        if self.rect.top > 0:
            if pressed_keys[K_w]: # North
                self.rect.move_ip(0,-self.speed)
                self.image = pygame.image.load(pN)
                self.direction = "n"
        if self.rect.bottom < screenheight: # If the bottom of the Human is above the screen height then allow user to move down. Same idea for other directions
            if pressed_keys[K_s]: # South
                self.rect.move_ip(0,self.speed)
                self.image = pygame.image.load(pS)
                self.direction = "s"
        if self.rect.left > 0:
            if pressed_keys[K_a]: # West
                self.rect.move_ip(-self.speed,0)
                self.image = pygame.image.load(pW)
                self.direction = "w"
        if self.rect.right < screenwidth:
            if pressed_keys[K_d]: # East
                self.rect.move_ip(self.speed,0)
                self.image = pygame.image.load(pE)
                self.direction = "e"
   
    def shoot(self):
        global ammo
        if ammo > 0:
            print("shoot bullet")
            ammo -= 1
            b = Bullet((self.rect[0],self.rect[1]),self.direction) # Create a new bullet heading in the current direction
            b.move()
            return True, b

        if ammo == 0:
            #display_reload = True
            #return display_reload
            return False, "this is to make it a tuple"
            
    def reload(self):
        global ammo
        ammo = 10
        print("Reload Sucessful")
    
    def reset(self,position):
        self.rect = self.image.get_rect(center=position)
        
    def update(self):
        self.move()
        screen.blit(self.image,self.rect)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,human_position,human_direction):
        super().__init__()
        self.image = bullet_image
        #self.direction tells the move method which if statement to run
        self.direction = human_direction
        # This is to offset the bullets so they appear from the gun art
        if self.direction == "n":
            self.position_x = human_position[0] + 70 
            self.position_y = human_position[1]          
        if self.direction == "s":      
            self.position_x = human_position[0] + 130 
            self.position_y = human_position[1] + 200       
        if self.direction == "e":
            self.position_x = human_position[0] + 200
            self.position_y = human_position[1] + 70   
        if self.direction == "w":         
            self.position_x = human_position[0]
            self.position_y = human_position[1] + 130
        self.rect = self.image.get_rect(center = (self.position_x,self.position_y)) 
        #self.rect will be set to where the position the human shot the bullet from

    def move(self):
        speed = 15
        if self.direction == "n":
            self.rect.move_ip(0,-speed)         
        if self.direction == "s":      
            self.rect.move_ip(0,speed)         
        if self.direction == "e":
            self.rect.move_ip(speed,0)         
        if self.direction == "w":         
            self.rect.move_ip(-speed,0)

    def update(self):
        self.move()         

# Creating Sprite Groups
all_sprites = pygame.sprite.LayeredUpdates()
zombies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Setting up Sprites
h1 = Human(position=(sc))
# Events
increase_spawn = pygame.USEREVENT + 1
pygame.time.set_timer(increase_spawn,4000)

# Additional Functions
def spawn_zombie():
        # For random Zombie spawn in N,E,S,W directions
        # Grabs a random set of (key,value) from dictionary
        random_spawn_key = random.choice(list(zombie_spawn))
        random_spawn_value = zombie_spawn[random_spawn_key]
        z = Zombie(random_spawn_value)
        zombies.add(z)

def format_time(secs):
    sec = secs%60
    minute = secs//60
    suv_time = "Survival Time - " + str(minute) + ":" + str(sec)
    return suv_time  
  

# Game Loop
def main():
    global ammo,score,spawn_amount
    run = True
    start_screen = True
    game_on = False
    game_over = False
    t0 = time.time() # Execution Time
    while run:
        if game_on:
            play_time = (time.time() - t0) # Current Time - Execution Time
            # Cycles through all events occuring
            for event in pygame.event.get():
                if event.type == QUIT: # If the user presses the exit button
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN: # If the user shoots
                    shot = h1.shoot()
                    has_ammo = shot[0] # True or False
                    bullet = shot[1] # the bullet sprite in h1.shoot()
                    
                    if has_ammo:
                        bullets.add(bullet)
                    #if not has_ammo:
                        #displayreload = medium_font.render("Reload Ammo!",False,white)
                        #screen.blit(displayreload,(150,150))

                if event.type == pygame.KEYDOWN:
                    if event.key == K_r: # If the user reloads
                        h1.reload()
                        screen.fill(black)
                if event.type == increase_spawn:
                    spawn_amount += 1                    
                    for _ in range(spawn_amount):
                        spawn_zombie()

            # Displaying Text and Background
            screen.fill(white) # Backup background in case png does not work 
            screen.blit(background,(0,0))
            displaytime = small_font.render(format_time(round(play_time)),True,white)
            displayammo = small_font.render("Ammo:" + str(ammo),True,white)
            displayscore = small_font.render("Score:" + str(score),True,white)
            screen.blit(displaytime,(10,10))
            screen.blit(displayammo,(10,50))
            screen.blit(displayscore,(10,100))
            
            # Displaying Sprites
            h1.update()
            zombies.draw(screen)
            zombies.update(h1)
            bullets.update()
            bullets.draw(screen)        
            
            # If a bullet hits any zombies
            for zombie in zombies:
                if pygame.sprite.spritecollideany(zombie,bullets):
                    zombie.kill()
                    score += 1

            # If Zombies get to the Human
            if pygame.sprite.spritecollideany(h1,zombies):
                # Game over music 
                game_over = True 
                game_on = False 
            
        if game_over:
        # Display Background and Text
            screen.fill(red) # As a backup if background image does not load
            screen.blit(game_over_bg,(0,0))
            display_game_over = large_font.render("Game Over!",True,grey)
            dis_go_rect = display_game_over.get_rect(center=(sc_x,sc_y-200))
            display_play_again = large_font.render("Play Again? [Y] [N]",True,grey)
            dis_pa_rect = display_play_again.get_rect(center=(sc_x,sc_y))
            screen.blit(display_game_over,(dis_go_rect))
            screen.blit(display_play_again,(dis_pa_rect))
            
            # User Options
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = False
                    run = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_n:
                        game_over = False
                        run = False
                        pygame.quit()
                        sys.exit()

                    if event.key == K_y:
                        # Reset Zombies, Human, and other game attributes
                        # Based on my websearches there is no pygame function to destroy a sprite that has already been blitted to screen
                        # Most developers just covered up the screen again with the background     
                        h1.reset(position=(sc))
                        for zombie in zombies:
                            zombie.kill()
                        t0 = play_time
                        score = 0
                        ammo = 10
                        game_over = False
                        game_on = True

        if start_screen:
            screen.fill(white)
            title = large_font.render("ZOMBIE SURVIVAL",True,black)
            titlerect = title.get_rect(center=(sc_x,sc_y-300))
            rule1 = small_font.render("Press W,A,S,D to Move",True,black)
            rule1rect = rule1.get_rect(center=(sc_x-400,sc_y-150))
            rule1_img_rect = rule1_img.get_rect(center = (sc_x-400,sc_y))
            rule2 = small_font.render("Click Mouse to Shoot Bullets",True,black)
            rule2rect = rule2.get_rect(center=(sc_x,sc_y-150))
            rule2_img_rect = rule2_img.get_rect(center = (sc_x,sc_y))
            rule3 = small_font.render("Press R to Reload",True,black)
            rule3rect = rule3.get_rect(center=(sc_x+400,sc_y-150))
            rule3_img_rect = rule2_img.get_rect(center = (sc_x+400,sc_y))
            spacebarcommand = medium_font.render("Press Spacebar to Begin",True,black)
            sbc_rect = spacebarcommand.get_rect(center=(sc_x,sc_y+300))

            screen.blit(title,(titlerect))
            screen.blit(rule1,(rule1rect))
            screen.blit(rule2,(rule2rect))
            screen.blit(rule3,(rule3rect))
            screen.blit(spacebarcommand,(sbc_rect))
            screen.blit(rule1_img,(rule1_img_rect))
            screen.blit(rule2_img,(rule2_img_rect))
            screen.blit(rule3_img,(rule3_img_rect))
            
                  
            for event in pygame.event.get():
                if event.type == QUIT:
                    game_over = False
                    run = False
                    start_screen = False
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == K_n:
                        game_over = False
                        run = False
                        start_screen = False
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE:
                        game_on = True
                        start_screen = False
            
        pygame.display.update()
        framesPerSec.tick(fps)    

main()