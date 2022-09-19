import sys, pygame, random, math
'''
Welcome to BULLET HELL

Inspired by the genre, I aimed to recreate the bullet hell arcade games.
Tim ZHOU

------------------------------------------------------------------------------------
[CONTROLS]

movement
'w,a,s,d' or 'up arrow, left arrow, down arrow, right arrow'

shooting
'left mouse click'
- To aim, use the mouse to direct the character and where the character faces to aim

------------------------------------------------------------------------------------
Have fun!

'''
#pygame
pygame.init()

#FPS set
FPS = 60
fpsClock = pygame.time.Clock()

#setting basic settings
#dimensions, colour, screen and name
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1025
BLACK = (0, 0 , 0)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Bullet Hell')
font = pygame.font.Font('OptimusPrinceps.ttf', 40)
font1 = pygame.font.Font('OptimusPrinceps.ttf', 90)

#setting the angle at which the image rectangle is set
#setting image and hp
correction_angle = 90
cursor = ('nierCursor.png')

#enemy bullets class
class EnemyBullet:
    '''
    Attributes: 
        image: pygame.image
        rect: Rect
        velocity: list(x:int, y:int)
        collision: collideRect
        spawn: list(x:int, y:int)
    '''

    #defining the class and the objects
    def __init__(self, id):
        #stating id for enemy bullet so it is easier to refer back to
        self.id = id
        #pygame load image
        #rotozoom is utilised to zoom in on empty space
        self.image = pygame.transform.rotozoom(pygame.image.load("nierball.png"), 0, 0.08)
        #get rectangle measurement for image, after rotozoom
        self.rect = self.image.get_rect()
        #velocity is pythageros, from random integers of -7,7
        self.velocity = [random.randint(-7,7), random.randint(-7,7)]
        #intial positions, will be random
        self.rect.x = random.randint(1,SCREEN_WIDTH)
        self.rect.y = random.randint(1, SCREEN_HEIGHT)

#player class
class Player:
    '''
    Attributes:
        image: pygame.image
        rect: Rect
        velocity: list(x:int, y:int)
        collision: collideRect
        shoot: PlayerBullet()
        health: int
    '''

    #defining the class and object
    #3 things must be referred to, HP, Image and the player themselve
    def __init__(self, image,hp ):
        #load image
        #rotozoom is utilised to zoom in on empty space
        self.image = pygame.transform.rotozoom(pygame.image.load(image), 0, 0.05)
        #get rectangle measurement for image, after rotozoom
        self.rect = self.image.get_rect()
        #starting position will be the middle of the screen
        #which is half the screen width and height
        self.rect.x = SCREEN_WIDTH/2
        self.rect.y = SCREEN_HEIGHT/2
        #stating the health of the player: chaning hp 
        #meaning it will represent the green bar
        self.health = hp
        #The Max HP Bar, which will allow for the base
        #of the HP Bar
        self.max_health = hp

    #stating the velocity function
    def setVelocity(self, vx, vy):
        #defining the velocity with
        #the x-axis int
        #the y-axis int
        self.velocity = [vx, vy]
    
    #defining the get width statement
    #this will later be used for the health bar of the character
    def get_width(self):
        #uses the in built pygame function
        return self.image.get_width()

    #defining the get height statment
    #this will later be used for the position of the health bar
    def get_height(self):
        #uses the in built pygame function
        return self.image.get_height()

    #defining the movement of the character
    #defining the rotation and spinning of the character
    def move(self):
        #previously we imported the math function
        #this is used to find the vector distance from the mouse to the character
        #this will be used to find the degree of rotation from the player
        #previously we defined the correction angle (starting angle) at 90
        #hence everything will be measured anti-clockwise starting at 90

        #the player position is detected
        player_pos  = screen.get_rect().center
        #the player's measurements
        player_rect = (self.image).get_rect(center = player_pos)

        #we now need to position/measurement of the player's mouse
        #this will be used to find the vector displacement
        mx, my = pygame.mouse.get_pos()

        #we can find the displacement dx and dy
        #this is done by: final - intial = displacement
        #hence by knowing the platyer as the intial, and mouse as final we calculate the displacement
        dx, dy = mx - player_rect.centerx, my - player_rect.centery

        #I use this displacement, to find the angle
        #dx is the adjacent side of the triangle from the angle
        #dy is the opposite side of the triangle from the angle
        #tan(angle) = dy/dx = opposite/adjacement
        #once we have the angle from 0 to angle, we need to find the angle from the starting angle which is 90
        #from this we find the net angle turned
        #hence: angle_1 - angle_0 = angle_n
        angle = math.degrees(math.atan2(-dy, dx)) - correction_angle

        #once we have the angle we need to find the rotated image rectangle
        rot_image      = pygame.transform.rotate(self.image, angle)
        #the image rect that stays the same, is the center, hence we need the center
        #this center is what is going to be moved with the player controls
        rot_image_rect = rot_image.get_rect(center = player_rect.center)
        '''-----------------------------------------------------------'''

        #keys is bool
        #what gets pressed
        keys = pygame.key.get_pressed()
        #detects it from the rotating image center
        rot_image_rect = self.rect.move(self.velocity)
        
        #if A or left arrow is pressed move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity = [-5,0]
        #if D or right arrow is pressed move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity = [5,0]
        #if W or up arrow is pressed moved up
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.velocity = [0,-5]
        #if S or down arrow is pressed down
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.velocity = [0,5]
        #combine moving left and up
        #moving 45 degrees to the left up
        if keys[pygame.K_LEFT] and keys[pygame.K_UP] or keys[pygame.K_a] and keys[pygame.K_w]:
            self.velocity = [-5,-5]
        #combine moving up and right
        #moving 45 degrees to the right up
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP] or keys[pygame.K_d] and keys[pygame.K_w]:
            self.velocity = [5,-5]
        #combine moving left and down
        #moving 45 degrees to the left down
        if keys[pygame.K_LEFT] and keys[pygame.K_DOWN] or keys[pygame.K_a] and keys[pygame.K_s]:
            self.velocity = [-5,5]
        #combine mocing right and down
        #moving 45 degrees to the right down
        if keys[pygame.K_RIGHT] and keys[pygame.K_DOWN] or keys[pygame.K_d] and keys[pygame.K_s]:
            self.velocity = [5,5]
        #moving the rectangle to the velocity that is pressed from the key
        self.rect = self.rect.move(self.velocity[0], self.velocity[1])
        #starting velocity when no key is pressed
        #stationary
        self.velocity = [0,0]

        #when player collides with the enemy bullet
        for bullet in bulletlist:
            if self.rect.colliderect(bullet.rect):
                #remove the bullet from the bullet list
                bulletlist.remove(bullet)

        #blit, print the rotating image and the centered point onto the screen
        screen.blit(rot_image, rot_image_rect.topleft)
        #function health bar, defined below
        self.healthbar()

    def healthbar(self):
        #the health bar has been set below the player, and centered on the player. The color is red for the full health bar
        #this allows the green health bar to become smaller, so it will reveal the red health bar under the player
        pygame.draw.rect(screen, (255,0,0), (self.rect.x, self.rect.y + self.image.get_height() + 10, self.image.get_width(), 10))
        #the health bar has been set below the player, in the same position
        #the green bar size, is a fraction from the remainging health/max health
        pygame.draw.rect(screen, (0,255,0), (self.rect.x, self.rect.y + self.image.get_height() + 10, self.image.get_width() * (self.health/self.max_health), 10))

#define player bullet
#allows for the player shooting
class PlayerBullet:
    '''
    Attributes:
        image: pygame.image
        rect: Rect 
        velocity: list(x:int, y:int)
        angle: float
        displacement_x = float
        displacement_y = float
        x = int
        y = int
    '''

    #defining the class and the object
    def __init__(self, x, y, speed , targetx, targety):
        #load image
        #rotozoom is utilised to zoom in on empty space
        self.image = pygame.transform.rotozoom(pygame.image.load('PlayerAmmo.png'), 0, 0.2)
        #get rectangale for measurement for image, after rotozoom
        self.rect = self.image.get_rect()
        #get angle by using trig, tan(angle)
        #to find the displacement, we have the cursor y value and the x value and the player center coordinate position
        #arctan(dy/dx) = angle
        angle = math.atan2(targety-y, targetx-x)
        #use the inverse of the angle to find the displacement of x
        self.dx = math.cos(angle)*speed
        #use the inverse of the angle to find the displacement of y
        self.dy = math.sin(angle)*speed
        #state the x and y value
        self.x = x 
        self.y = y 

    #definning the shooting
    def shoot(self):
        #because it is in a float value, we need to make it into a integer
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        #once the values have become int, we will turn the rectangle coordinates into the said values
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    

#define the player, by using the player class
#cursor is the image defined previously
#20 is the HP: int
player = Player(cursor, 20) 
#velocity set as 0,0
#stationary values
player.setVelocity(0,0)

#set the list of enemy bullets
#set the list of player bullets
bulletlist = []
playerAmmo = []

#define the main menu
def main_menu():
    #initialise while loop
    run = False
    while not run:
        #check for the keys pressed
        for event in pygame.event.get():
            #if they press the exit key
            if event.type == pygame.QUIT:
                #quit the program
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #if the key pressed is SPACE
                if event.key == pygame.K_SPACE:
                    #turn off the main menu then turn on the main program
                    run = True
                    main()

        #screen is filled
        screen.fill(BLACK)
        #text is made
        text_start1 = font1.render("Bullet Hell", True, (255,255,255))
        text_start2 = font.render("[ SPACE ] to start", True, (255,255,255))
        #blit the text
        screen.blit(text_start1,(57,210))
        screen.blit(text_start2,(200,320))

        #update display with text
        #set FPS: time
        pygame.display.update()
        fpsClock.tick(FPS)

#define the death screen
def death_menu():
    #intialise while loop
    running = False
    while not running:
        #check for the keys pressed
        for event in pygame.event.get():
            #if exit key is pressed quiot the program
            if event.type == pygame.QUIT:
                sys.exit()
            #check if the key is pressed
            if event.type == pygame.KEYDOWN:
                #check if the space key is pressed
                if event.key == pygame.K_SPACE:
                    #turn off the main menu and then add 20 health back as well as turning on the main program
                    running = True
                    player.health += 20
                    main()
        
        #screen is filled
        screen.fill(BLACK)
        #text is made
        death = font1.render("YOU DIED", 1, (255,255,255))
        restart = font.render("[ SPACE ] to restart", True, (255,255,255))
        #blit the text
        screen.blit(death, (SCREEN_WIDTH/2 - death.get_width()/2, 225))
        screen.blit(restart, (SCREEN_WIDTH/2 - restart.get_width()/2, 150))
        
        #update display with text
        #set FPS: time
        pygame.display.update()
        fpsClock.tick(FPS)

#define main game
def main():
    #intialise the while loop
    while True:
        #checks for an event
        for event in pygame.event.get():
            #if the event is pressing the quit key
            if event.type == pygame.QUIT:
                #exit and close program
                sys.exit()

            #otherwise, if the event is a mouse button press
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #if the press is a LEFT mouse click execute the shoot function
                if event.button == 1:
                    #find the position of the mouse
                    x, y = pygame.mouse.get_pos()
                    #set the values for the player bullet class
                    pBullet = PlayerBullet(player.rect.centerx ,player.rect.centery , 20, x, y )
                    #add the player bullet into the bullet class
                    playerAmmo.append(pBullet)
        
        #every frame a ball is made between 0 and 1
        for ball in list(range(0,1)):
            #the created balls will be appeneded to the bullet list
            bulletlist.append(EnemyBullet(ball))

        #for every ball in the bullet list
        for ball in bulletlist: 
            #the speed of the bullets are intialised and allows them to move
            ball.rect = ball.rect.move(ball.velocity)
            #if the balls leave the screen, they will be removed, to prevent stress and over work on the program
            #over the width of the screen
            if ball.rect.left < 0 or ball.rect.right > SCREEN_WIDTH:
                bulletlist.remove(ball)
            #over the height of the screen
            elif ball.rect.top < 0 or ball.rect.bottom > SCREEN_HEIGHT:
                bulletlist.remove(ball)
        
        #for ammo in the player ammo list
        for ammo in playerAmmo:
            #checks if the bullets are off the scrren or not
            #if the bullets are over the width, or below 0 , remove the bullet
            if ammo.rect.left < 0 or ammo.rect.right > SCREEN_WIDTH:
                playerAmmo.remove(ammo)
            #if the bullets are over the height, or below 0, remove the bullet
            elif ammo.rect.top < 0 or ammo.rect.bottom > SCREEN_HEIGHT:
                playerAmmo.remove(ammo)

        #for the balls in the bulletlist
        for ball in bulletlist:
            #detect if the bullets are colliding with the player
            if player.rect.colliderect(ball.rect):
                #if they are, minus 1 health
                player.health -= 1
            # if the health reaches 0, play the death menu
            if player.health == 0:
                death_menu()

        #for the ammo in the player ammo list
        for ammo in playerAmmo:
            #for the bullets in the bullet list
            for bullet in bulletlist:
                #if the bullets and the ammo collide
                if ammo.rect.colliderect(bullet.rect):
                    #if they do, remove the bullet from both the enemy and the player
                    bulletlist.remove(bullet)
                    if ammo in playerAmmo:
                        playerAmmo.remove(ammo)

        #fill the screen with black
        screen.fill(BLACK)

        #player movement commant
        player.move()

        #blit and draw all the objects that are used
        #the enemy bullets
        for ball in range(len(bulletlist)):
            screen.blit(bulletlist[ball].image, bulletlist[ball].rect)
        #the travel and shooting of the player bullet
        for bullet in playerAmmo:
            bullet.shoot()
        #the drawing and blitting of the player ammo
        for bullet in range(len(playerAmmo)):
            screen.blit(playerAmmo[bullet].image, playerAmmo[bullet].rect)
        
        #draw the screen
        #FPS
        pygame.display.flip()
        fpsClock.tick(FPS)

#intialise the program
main_menu()

