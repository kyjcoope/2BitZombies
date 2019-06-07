import gameEngine, pygame, time, random, worldMap, math, random, copy
    
class Player:
    def __init__(self, scene):
        self.sprite = gameEngine.Sprite(scene, 400, 300, 'player1.png', 'player')
        self.sprite.scale(20,40)
        self.sprite.collidesWith.append('enemy')
        self.sprite.collidesWith.append('coin')
        self.totalHealth = 5
        self.sprite.collisions = True
        self.flipLockL = False #on when facing left
        self.flipLockR = True
        self.position = [int(self.sprite.x_loc/20), int(self.sprite.y_loc/20)]
        self.lastTimeJump = time.time()
        self.lastTimeShoot = time.time()
        self.jumping = False
        self.walking = False
        self.jump = False
        self.down = False
        self.health = 5
        self.numAvailableBoxes = 10
        self.weapon = 1
        self.availableBoxes = 0

        #sounds
        self.shootSound = pygame.mixer.Sound("shot.wav")
        


        #animations
        self.sprite.addImage('player2.png') #1
        self.sprite.addImage('player3.png') 
        self.sprite.addImage('player4.png') 
        self.sprite.addImage('player5.png')
        self.sprite.addImage('player2.png') #1
        self.sprite.addImage('player3.png') 
        self.sprite.addImage('player4.png') 
        self.sprite.addImage('player5.png') 

    def controls(self, scene, world, mousePosTrue, mousePosGrid, bullets, boxes, groundBlocks):
        keys = pygame.key.get_pressed()
        mouse_keys = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        makeBox = 1
        global weapon
        #movement LEFT/RIGHT
        if keys[pygame.K_a]:
            self.sprite.dx=-5
            self.walking = True
        elif keys[pygame.K_d]:
            self.sprite.dx=5
            self.walking = True
        else:
            self.sprite.dx=0
            self.walking = False

        #JUMP 
        if keys[pygame.K_w]:
            if (not self.jump) and (not self.jumping):
                self.jump = True
        if(self.jump):
            if(not self.jumping):
                self.sprite.dy=-10
                self.jumping = True
            if(self.jumping):
                if(self.sprite.dy==0) and (world[self.position[1]+1][self.position[0]] == 1):
                    self.jump = False
                    self.jumping = False
        #DOWN
        if keys[pygame.K_s]:
            if (not self.down):
                if self.lastTimeJump < time.time()-0.1:
                    self.lastTimeJump = time.time()
                    self.sprite.dy = 10
                    self.down = True

        if keys[pygame.K_1]:
            self.weapon = 1

        if keys[pygame.K_2]:
            self.weapon = 2

        if keys[pygame.K_p]:
            main()

        #Place Box
        if mouse_keys[0] == 1: #LMC
            if self.weapon == 2: #select weapon
                self.shoot(mousePosTrue, bullets)

                
        if self.weapon == 1: #builder selected
            if self.numAvailableBoxes > 0:
                try: #check if can build/if there is a foundation to build on
                    if(world[int(mousePosGrid[1]/20)+1][int(mousePosGrid[0]/20)]) != 1:#bottom check
                        makeBox = 0
                        if(world[int(mousePosGrid[1]/20)][int(mousePosGrid[0]/20)+1]) == 1 and world[int(mousePosGrid[1]/20)+1][int(mousePosGrid[0]/20) + 1] == 1: #right check
                            makeBox = 1
                        if(world[int(mousePosGrid[1]/20)][int(mousePosGrid[0]/20)-1]) == 1 and world[int(mousePosGrid[1]/20)+1][int(mousePosGrid[0]/20)-1] == 1:#left check
                            makeBox = 1
                except IndexError:
                    pass

                for i in range(len(boxes)): #check if a box already here
                    if boxes[i].sprite.x_loc == mousePosGrid[0] and boxes[i].sprite.y_loc==mousePosGrid[1]:
                            makeBox = 0
                for i in range(len(groundBlocks)):#check if a ground box is already here
                    if groundBlocks[i].sprite.x_loc == mousePosGrid[0] and groundBlocks[i].sprite.y_loc==mousePosGrid[1]:
                        makeBox = 0
                        
                if makeBox == 1:#all checks passed okay to build box
                    pygame.draw.rect(scene.gameDisplay, gameEngine.green, (mousePosGrid[0],mousePosGrid[1],20,20))#green good box
                    if mouse_keys[0] == 1:#mouse click check
                        boxes.append(Box(int(mousePosGrid[0]/20),int(mousePosGrid[1]/20), scene, world))
                        self.numAvailableBoxes = self.numAvailableBoxes - 1
                else:#check failed/make red bad box
                    pygame.draw.rect(scene.gameDisplay, gameEngine.red, (mousePosGrid[0],mousePosGrid[1],20,20))
                        
        #walking/image flip
        if(mousePosTrue[0] < self.sprite.x_loc):#mouse to the left of the player
            if(not self.flipLockL): 
                saveCurrent = self.sprite.currentImage
                for i in range(len(self.sprite.spriteImage1)):
                    self.sprite.currentImage = i
                    self.sprite.flip(True, False)
                self.sprite.currentImage = saveCurrent
                self.flipLockL = True
                self.flipLockR = False
        else: #mouse to the right of the player
            if(not self.flipLockR):
                saveCurrent = self.sprite.currentImage
                for i in range(len(self.sprite.spriteImage1)):
                    self.sprite.currentImage = i
                    self.sprite.flip(True, False)
                self.sprite.currentImage = saveCurrent
                self.flipLockR = True
                self.flipLockL = False
        
    def update(self, scene, world, mousePosTrue, mousePosGrid, bullets, boxes, groundBlocks):
        self.position = [int(self.sprite.x_loc/20), int(self.sprite.y_loc/20)+1]
        try: #check if about to go through the ground
            if world[int((self.sprite.dy+self.sprite.y_loc)/20)+2][int((self.sprite.x_loc+7)/20)] == 1:
                self.sprite.y_loc=(int((self.sprite.dy+self.sprite.y_loc)/20))*20
                self.sprite.dy=0
                self.down = False
            else:
                self.sprite.dy+=1 #gravity
        except IndexError:
            self.sprite.dy=0 #on the ground
        self.controls(scene, world, mousePosTrue, mousePosGrid, bullets, boxes, groundBlocks) #player controls
        if self.walking:#walking animation
            self.sprite.changeImage()
        else:
            self.sprite.currentImage = 0
        if(self.health<=0):  #DIE
            self.sprite.alive = False
        self.sprite.update()
        

    def shoot(self, mousePosTrue, bullets):
        if(self.lastTimeShoot+.25<time.time()): #shoot delay
            self.lastTimeShoot = time.time()
            divisor = (mousePosTrue[0]-self.sprite.x_loc)
            if divisor == 0:
                divisor = 0.01 #to protect against division by 0
            angle = math.atan((mousePosTrue[1]-self.sprite.y_loc)/divisor) #calc angle to shoot
            force = 20 #speed of bullet

            #flip force based on direct character is facing/ apply force to bullet at angle
            if(mousePosTrue[0]<self.sprite.x_loc):
                forceX = -force*math.cos(angle)
                forceY = -force*math.sin(angle)
            else:
                forceX = force*math.cos(angle)
                forceY = force*math.sin(angle)

            #Check if bullet is free to spawn and spawn it if so
            for x in range(len(bullets)):
                if(bullets[x].sprite.alive == False):
                    bullets[x].sprite.alive=True
                    pygame.mixer.Sound.play(self.shootSound)
                    if(self.flipLockL):
                        bullets[x].sprite.dy = forceY
                        bullets[x].sprite.dx = forceX
                    if(self.flipLockR):
                        bullets[x].sprite.dy = forceY
                        bullets[x].sprite.dx = forceX
                    bullets[x].sprite.x_loc = self.sprite.x_loc
                    bullets[x].sprite.y_loc = self.sprite.y_loc+13
                    break
                

class Bullet:
    def __init__(self, scene):
        self.sprite = gameEngine.Sprite(scene, 400,300, 'bullet.png', 'bullet')
        self.sprite.boundCondition = "die"
        self.sprite.collidesWith.append('enemy')
        self.sprite.collisions = True
        self.sprite.scale(20,20)
        self.sprite.alive = False

    def update(self):
        if(self.sprite.collision() == 'enemy'):
            self.sprite.alive = False
        
        self.sprite.update()

class Enemy:
    def __init__(self, scene, targets):
        self.rand_num = random.randint(0,len(targets)-1) #pick array element to get targets from, check element picks different targets
        self.sprite = gameEngine.Sprite(scene, 200, 300, 'enemy1.png', 'enemy')
        self.sprite.scale(20,40)
        self.sprite.collidesWith.append('bullet')
        self.sprite.collisions = True
        self.flipLockL = False #on when facing left
        self.flipLockR = True
        self.position = [int(self.sprite.x_loc/20), int(self.sprite.y_loc/20)]
        self.lastTimeJump = time.time()
        self.lastTimeShoot = time.time()
        self.jumping = False
        self.walking = False
        self.jump = False
        self.down = False
        self.tp = False
        self.sprite.alive = False
        self.health = 1
        self.lastAttack = time.time()
        self.deathAnimTimer = time.time()
        self.deathAnimCount = 0
        self.jumpDelay = time.time()
        self.alive = True
        self.drop = True

        #control flags
        self.key_w = False
        self.key_a = False
        self.key_s = False
        self.key_d = False

        #animations
        self.sprite.useSpriteImage = 0
        self.sprite.addImage('enemy2.png') #1
        self.sprite.addImage('enemy3.png') 
        self.sprite.addImage('enemy4.png') 
        self.sprite.addImage('enemy5.png')
        self.sprite.addImage('enemy2.png') #1
        self.sprite.addImage('enemy3.png') 
        self.sprite.addImage('enemy4.png') 
        self.sprite.addImage('enemy5.png')

        self.sprite.useSpriteImage = 1
        self.sprite.addImage('enemydying1.png') #1
        self.sprite.addImage('enemydying2.png') 
        self.sprite.addImage('enemydying3.png') 
        self.sprite.addImage('enemydying5.png') #1
        self.sprite.addImage('enemydying6.png') 
        self.sprite.addImage('enemydying7.png')

        self.sprite.useSpriteImage = 0

        #sound
        self.zombieSound = pygame.mixer.Sound("zombieSound.wav")
        self.hitSound = pygame.mixer.Sound("hit.wav")

    def controls(self, world, targets):
        #movement LEFT/RIGHT
        if self.key_a:
            self.sprite.dx=-5
            self.walking = True
            if(not self.flipLockL):
                saveCurrent = self.sprite.currentImage
                for i in range(len(self.sprite.spriteImage1)):
                    self.sprite.currentImage = i
                    self.sprite.flip(True, False)
                self.sprite.currentImage = saveCurrent
                self.flipLockL = True
                self.flipLockR = False
        elif self.key_d:
            self.sprite.dx=5
            self.walking = True
            if(not self.flipLockR):
                saveCurrent = self.sprite.currentImage
                for i in range(len(self.sprite.spriteImage1)):
                    self.sprite.currentImage = i
                    self.sprite.flip(True, False)
                self.sprite.currentImage = saveCurrent
                self.flipLockR = True
                self.flipLockL = False
        else:
            self.sprite.dx=0
            self.walking = False

        #JUMP 
        if self.key_w:
            if (not self.jump) and (not self.jumping):
                self.jump = True
        if(self.jump):
            if(not self.jumping):
                self.sprite.dy=-10
                self.jumping = True
            if(self.jumping):
                try:
                    if(self.sprite.dy==0) and (world[self.position[1]+1][self.position[0]] == 1):
                        self.jump = False
                        self.jumping = False
                except IndexError:
                    pass
        #DOWN
        if self.key_s:
            if (not self.down):
                if self.lastTimeJump < time.time()-0.1:
                    self.lastTimeJump = time.time()
                    self.sprite.dy = 10
                    self.down = True

            
    def update(self, world, targets, boxes, player, pickUpBoxes, pickUpHearts):
        if(self.alive):
            #gravity/dont fall through the ground check
            self.position = [int(self.sprite.x_loc/20), int(self.sprite.y_loc/20)+1]
            try:#ground check
                if world[int((self.sprite.dy+self.sprite.y_loc)/20)+2][int((self.sprite.x_loc+7)/20)] == 1:
                    self.sprite.y_loc=(int((self.sprite.dy+self.sprite.y_loc)/20))*20
                    self.sprite.dy=0
                    self.down = False
                else:#gravity
                    self.sprite.dy+=1
            except IndexError:
                self.sprite.dy=0 #your on the ground
            self.controls(world, targets) #move enemy/control
            if self.walking: #walking animation
                self.sprite.changeImage()
            else:
                self.sprite.currentImage = 0

            #BRAIN            
            targetX = targets[self.rand_num][0]
            targetY = targets[self.rand_num][1]

            targetY_valid = False
            targetX_valid = False
            
            if targetX - 20 > self.sprite.x_loc: #if target to the right
                self.key_d = True
                self.key_a = False
                targetX_valid = False
            elif targetX + 20 < self. sprite.x_loc: #if target to the left
                self.key_a = True
                self.key_d = False
                targetX_valid = False
            else: #on target
                self.key_a = False
                self.key_d = False
                targetX_valid = True

            if targetY - 20 > self.sprite.y_loc: #if target below
                self.key_s = True
                self.key_w = False
                targetY_valid = False
            elif targetY < self. sprite.y_loc: #if target above
                self.key_w = True
                self.key_s = False
                targetY_valid = False
            else: #on target
                self.key_w = False
                self.key_s = False
                targetY_valid = True

            #ATTACK
            if self.sprite.alive == True:
                if(targetX_valid and targetY_valid):
                    if(self.lastAttack < time.time() - 0.7):
                        self.lastAttack = time.time()
                        if self.rand_num == 0: #attack player
                            pygame.mixer.Sound.play(self.hitSound)
                            player.health = player.health - 1
                        else:
                            dontdonext = 1
                            for i in range(len(boxes)): #attack box
                                if(targetX == boxes[i].sprite.x_loc and targetY == boxes[i].sprite.y_loc):
                                        boxes[i].health = boxes[i].health - 0.4
                                        dontdonext = 0
                                        break
                            if dontdonext: #attack player
                                pygame.mixer.Sound.play(self.hitSound)
                                player.health = player.health - 1
            #bullet collision
            if(self.sprite.collision() == 'bullet'):
                self.health=self.health-0.5
                
        if(self.health<=0):
            if(self.alive):#when first die
                self.sprite.currentImage = len(self.sprite.spriteImage2)
                self.deathAnimCount = 0
            self.alive = False
            self.sprite.useSpriteImage = 1
            self.sprite.dx = 0
            self.sprite.dy = 0
            self.key_w = False
            self.key_a = False
            self.key_s = False
            self.key_d = False
            #death animation control
            if(self.deathAnimTimer < time.time() - 0.1):
                self.deathAnimTimer = time.time()
                self.sprite.changeImage()
                self.deathAnimCount = self.deathAnimCount + 1
            if(self.deathAnimCount >= 5):
                self.sprite.alive = False
                #drop pickups
                if(self.drop):
                    if(random.randint(0,2)):
                        self.drop = False
                        for i in range(len(pickUpBoxes)):
                            if pickUpBoxes[i].sprite.alive == False:
                                pickUpBoxes[i].sprite.alive = True
                                pickUpBoxes[i].sprite.x_loc = self.sprite.x_loc
                                pickUpBoxes[i].sprite.y_loc = self.sprite.y_loc + 30
                                break
                    else:
                        self.drop = False
                        for i in range(len(pickUpHearts)):
                            if pickUpHearts[i].sprite.alive == False:
                                pickUpHearts[i].sprite.alive = True
                                pickUpHearts[i].sprite.x_loc = self.sprite.x_loc
                                pickUpHearts[i].sprite.y_loc = self.sprite.y_loc + 30
                                break

        #finally
        self.sprite.update()
class BoxPickup:
    def __init__(self,scene):
        self.sprite = gameEngine.Sprite(scene, 0, 0, 'box1.png', 'pickup')
        self.sprite.scale(10,10)
        self.sprite.collidesWith.append('player')
        self.sprite.collisions = True
        self.sprite.alive = False
        self.pickupSound = pygame.mixer.Sound("pickup.wav")

    def update(self, player):
        if(self.sprite.collision() == 'player'):
            pygame.mixer.Sound.play(self.pickupSound)
            player.numAvailableBoxes = player.numAvailableBoxes + 1
            self.sprite.alive = False
        self.sprite.update()

class HeartPickup:
    def __init__(self,scene):
        self.sprite = gameEngine.Sprite(scene, 0, 0, 'heart.png', 'pickup')
        self.sprite.scale(10,10)
        self.sprite.collidesWith.append('player')
        self.sprite.collisions = True
        self.sprite.alive = False
        self.pickupSound = pygame.mixer.Sound("pickup.wav")

    def update(self, player):
        if(self.sprite.collision() == 'player'):
            pygame.mixer.Sound.play(self.pickupSound)
            if player.health < 5:
                player.health = player.health + 1
            self.sprite.alive = False
        self.sprite.update()
        
class Box:
    def __init__(self, x ,y, scene, world):
        self.sprite = gameEngine.Sprite(scene, x*20, y*20, 'box1.png', 'box')
        self.sprite.scale(20,20)
        self.sprite.addImage('box2.png')
        self.sprite.addImage('box3.png')
        self.sprite.addImage('box4.png')
        self.sprite.addImage('box5.png')
        self.good = False
        
        world[y][x] = 1
        self.health = 1
        self.lastHealth = 1
        
    def update(self, world, boxes, deleteList):
        flipthatshit = 0
        self.sprite.update()
        if(self.sprite.collision() == 'bullet'):
            self.health=self.health-0.1

        #check box stability
        if(world[int(self.sprite.y_loc/20)+1][int(self.sprite.x_loc/20)]) == 1:#bottom check
            self.good = True    
        elif(world[int(self.sprite.y_loc/20)][int(self.sprite.x_loc/20)+1]) == 1 and world[int(self.sprite.y_loc/20)+1][int(self.sprite.x_loc/20)+1] == 1: #right check
            self.good = True
        elif(world[int(self.sprite.y_loc/20)][int(self.sprite.x_loc/20)-1]) == 1 and world[int(self.sprite.y_loc/20)+1][int(self.sprite.x_loc/20)-1] == 1:#left check
             self.good = True
        else:
            self.good = False
            
        if(not self.good):
            self.health=self.health-0.5

        #check dmg and change image accordingly
        if(self.health<self.lastHealth-0.2):
            self.sprite.changeImage()
            self.lastHealth = self.health

        #check if should die and delete
        if(self.health<=0):
            self.sprite.alive = False
            world[int(self.sprite.y_loc/20)][int(self.sprite.x_loc/20)] = 0
            for i in range(len(boxes)): #see if box needs deleted, and add to deleteList if so
                if boxes[i].sprite.x_loc == self.sprite.x_loc and boxes[i].sprite.y_loc==self.sprite.y_loc:
                    deleteList.append(i)
                    break
class Ground:
    def __init__(self, x ,y, scene, world):
        self.sprite = gameEngine.Sprite(scene, x*20, y*20, 'ground.png', 'ground')
        self.sprite.scale(20,20)
        world[y][x] = 1
        
    def update(self):
        self.sprite.update()

class Coin:
    def __init__(self, scene):
        self.sprite = gameEngine.Sprite(scene, 400, 100, 'coin1.png', 'coin')
        self.sprite.collidesWith.append('player')
        self.sprite.collisions = True
        self.lastTime = time.time()
        self.sprite.scale(20,20)
        self.sprite.addImage('coin2.png') #1
        self.sprite.addImage('coin3.png') #2
        self.sprite.addImage('coin4.png') #3
        self.sprite.addImage('coin3.png') #4
        self.sprite.currentImage = 4
        self.sprite.flip(True, False)
        self.sprite.addImage('coin2.png') #5
        self.sprite.currentImage = 5
        self.sprite.flip(True, False)
        
    def update(self):            
        if(self.lastTime+.1<time.time()):
            self.sprite.changeImage()
            self.lastTime = time.time()
        self.sprite.update()            
        

def createWorld(world,groundBlocks,scene):
    count = 0
    for i in range(len(world)):
        for j in range(len(world[i])):
            if(world[i][j] == 1):
                groundBlocks.append(Ground(j, i, scene, world))
                count=count+1

def deleteBoxes(boxList, boxes):
    for i in range(len(boxList)):
        temp = boxes.pop(boxList.pop())
        del temp

def targetScanner(world, targets, player):

    #row 28 check/ default to player
    for j in range(len(world[0])):
        if world[28][j] == 1:
            targets[1] = (j*20, 28*20)
            break
        else:
            targets[1] = (player.sprite.x_loc, player.sprite.y_loc)

    #row 27 check/defualt to row 28 then player
    for j in range(len(world[0])):
        if world[27][j] == 1:
            targets[2] = (j*20, 27*20)
            break
        else:
            for j in range(len(world[0])):
                if world[28][j] == 1:
                    targets[2] = (j*20, 28*20)
                    break
                else:
                    targets[2] = (player.sprite.x_loc, player.sprite.y_loc)
    
class Heart:
    def __init__(self, scene):
        self.sprite = gameEngine.Sprite(scene, 10, 10, 'heart.png', 'heart')
        self.sprite.scale(20,20)

    def update(self):
        self.sprite.update()

def makeHealth(player, healthBar, scene):
    for i in range(player.totalHealth):
        healthBar.append(Heart(scene))
        healthBar[i].sprite.x_loc=(i)*20
        healthBar[i].sprite.y_loc = 3
        
def healthUpdate(player, healthBar):
    for i in range(player.health):
        healthBar[i].update()

def texObjects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def StartEndButtons(scene, mousePosTrue, textSurf1, textRect1, textSurf2, textRect2):#buttens and text at start/end
    if 350 + 100 > mousePosTrue[0] > 350 and 350 + 25> mousePosTrue[1] > 350 - 25:#check mouse pos
        pygame.draw.rect(scene.gameDisplay, (128,128,128), (350,350,100,50))#draw button hover color
        mouseButton = pygame.mouse.get_pressed()#check mouse press on button
        if(mouseButton[0] == 1):
            main()
            gameEngine.pygame.quit()
    else:
        pygame.draw.rect(scene.gameDisplay, (192,192,192), (350,350,100,50))#draw button not hover
    try:
        scene.gameDisplay.blit(textSurf1, textRect1)
        scene.gameDisplay.blit(textSurf2, textRect2)
    except:
        pass

def main():
    #declarations/initiations
    crashed = False
    resolution = (800,600)
    makeBox = 0
    mousePosTrue = []
    mousePosGrid = []
    pickUpBoxes = []
    pickUpHearts = []
    matrixPos = []
    world = copy.deepcopy(worldMap.worldTile)
    box_removed = False
    deleteList = []
    targets = []
    last_enemy_spawn = time.time()

    scene = gameEngine.Scene(resolution)
    scene.backgroundColor = (200,200,255)

    #text/fonts
    smallText = pygame.font.Font("freesansbold.ttf", 20)
    
    #loss text
    textSurf1, textRect1 = texObjects("YOU DIED!", smallText, gameEngine.red)
    textSurf2, textRect2 = texObjects("RETRY", smallText, gameEngine.black)
    textRect1.center = ((400), (300))
    textRect2.center = ((400), (375))

    #win text
    textSurf3, textRect3 = texObjects("WINNER WINNER!", smallText, gameEngine.red)
    textSurf4, textRect4 = texObjects("RETRY", smallText, gameEngine.black)
    textRect3.center = ((400), (300))
    textRect4.center = ((400), (375))

    textSurf5, textRect5 = texObjects("x", smallText, gameEngine.black)
    textRect5.center = ((400), (300))

    #extra images
    cursor = pygame.image.load('cursor.png')
    boxSelect = pygame.image.load('box_select.png')
    boxSelect = pygame.transform.scale(boxSelect, (40, 40))
    gunSelect = pygame.image.load('gun_select.png')
    gunSelect = pygame.transform.scale(gunSelect, (40, 40))
    numBoxesImage = pygame.image.load('box1.png')
    numBoxesImage = pygame.transform.scale(numBoxesImage, (20, 20))

    
    mousePosTrue = pygame.mouse.get_pos()
    mousePosGrid = [int(mousePosTrue[0]/20)*20, int(mousePosTrue[1]/20)*20]
    player = Player(scene)
    bullets = []
    healthBar = []
    boxes = []
    enemys = []
    groundBlocks = []
    coin = Coin(scene)
    createWorld(world,groundBlocks,scene)
    targets.append((player.sprite.x_loc, player.sprite.y_loc))
    targets.append((0,0))
    targets.append((0,0))
    makeHealth(player, healthBar, scene)
    pause = False
    win = False
    for i in range(0,5):
        enemys.append(Enemy(scene, targets))
    enemys[0].alive = True
    for i in range(0,5):
        bullets.append(Bullet(scene))
    for i in range(0,5):
        pickUpBoxes.append(BoxPickup(scene))
    for i in range(0,5):
        pickUpHearts.append(HeartPickup(scene))
    #game loop
    while not crashed:
        #check game close/crash
        crashed = gameEngine.quitEvent(crashed)
        #update scene
        scene.update()
        #mousePos update
        mousePosTrue = pygame.mouse.get_pos()
        mousePosGrid = [int(mousePosTrue[0]/20)*20, int(mousePosTrue[1]/20)*20]

        if(win):
            StartEndButtons(scene, mousePosTrue, textSurf3, textRect3, textSurf4, textRect4)
        if(not pause):
            #game end
            if(player.health<0):
                StartEndButtons(scene, mousePosTrue, textSurf1, textRect1, textSurf2, textRect2)

            #game win
            if(player.sprite.collision() == 'coin'):
                pause = True
                win = True

            #update sprite lists
            for i in range(len(groundBlocks)):
                groundBlocks[i].update()
            for i in range(len(boxes)):
                boxes[i].update(world, boxes, deleteList)
            deleteBoxes(deleteList, boxes)

            #spawn enemys
            if(last_enemy_spawn < time.time() - 3):
                last_enemy_spawn = time.time()
                for i in range(len(enemys)):
                    if enemys[i].sprite.alive == False:
                        enemys[i].sprite.alive = True
                        enemys[i].alive = True
                        enemys[i].drop = True
                        enemys[i].sprite.useSpriteImage = 0
                        enemys[i].sprite.y_loc = 520
                        if(i%2): 
                            enemys[i].sprite.x_loc = 800
                        else:
                            enemys[i].sprite.x_loc = -100
                        enemys[i].health = 1
                        break

            #more sprite updates
            for i in range(len(enemys)):
                enemys[i].update(world, targets, boxes, player, pickUpBoxes, pickUpHearts)
            for i in range(0,5):
                bullets[i].update()
            for i in range(0,5):
                pickUpBoxes[i].update(player)
            for i in range(0,5):
                pickUpHearts[i].update(player)
            if player.weapon == 1:
                scene.gameDisplay.blit(boxSelect,(5,30))
            elif player.weapon == 2:
                scene.gameDisplay.blit(cursor,(mousePosTrue[0],mousePosTrue[1]+10))
                scene.gameDisplay.blit(gunSelect,(5,30))
            coin.update()

            #building HUD
            scene.gameDisplay.blit(numBoxesImage,(5,80))
            textSurf5, textRect5 = texObjects("x"+str(player.numAvailableBoxes), smallText, gameEngine.black)
            textRect5.center = ((40), (95))
            scene.gameDisplay.blit(textSurf5, textRect5)
            player.update(scene, world, mousePosTrue, mousePosGrid, bullets, boxes, groundBlocks)
            targets[0] = (player.sprite.x_loc, player.sprite.y_loc)
            targetScanner(world, targets, player)
            healthUpdate(player, healthBar)
        

if __name__ == "__main__":
    main()
    gameEngine.pygame.quit()
    
