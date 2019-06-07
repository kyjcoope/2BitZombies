import pygame

#RGB colors
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)

lock = True

class Scene:
    def __init__(self, resolution):
        pygame.init()
        self.resolution = resolution
        self.gameDisplay = pygame.display.set_mode(resolution)
        pygame.display.set_caption('2BitZombies')
        pygame.display.set_icon(pygame.image.load('icon.png'))
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0)) #hide cursor when on screen
        self.spriteList = []
        self.clock = pygame.time.Clock()
        self.backgroundColor = white

    def update(self):
        pygame.display.update()
        self.gameDisplay.fill(self.backgroundColor)
        self.clock.tick(30)

class Sprite:
    def __init__(self, scene, x_loc, y_loc, img, classtype):
        self.scene = scene
        self.useSpriteImage = 0
        self.classtype = classtype
        self.collidesWith = []
        self.controlable = 0
        self.boundCondition = "none"
        self.alive = True
        self.scaled = False
        self.collisions = False
        self.x_scale = 0
        self.y_scale = 0
        self.dx = 0
        self.dy = 0
        scene.spriteList.append(self)
        self.x_loc = x_loc
        self.y_loc = y_loc
        self.img = img
        self.spriteImage1 = []
        self.spriteImage2 = []
        self.currentImage = 0
        self.spriteImage1.append(pygame.image.load(self.img))

    def updateVelocity(self): #pixel per frame
        self.x_loc =self.dx+self.x_loc
        self.y_loc =self.dy+self.y_loc

    def changeImage(self):
        if self.useSpriteImage == 0:
            if self.currentImage>=len(self.spriteImage1)-1:
                self.currentImage = 0
            else:
                self.currentImage = self.currentImage+1
        if self.useSpriteImage == 1:
            if self.currentImage>=len(self.spriteImage2)-1:
                self.currentImage = 0
            else:
                self.currentImage = self.currentImage+1
            

    def addImage(self, img):
        if self.useSpriteImage == 0:
            self.spriteImage1.append(pygame.transform.scale(pygame.image.load(img),(self.x_scale, self.y_scale)))
        if self.useSpriteImage == 1:
            self.spriteImage2.append(pygame.transform.scale(pygame.image.load(img),(self.x_scale, self.y_scale)))
            
    def update(self):
        if(self.alive):
            self.updateVelocity()
            self.boundingAction()
            if self.useSpriteImage == 0:
                self.scene.gameDisplay.blit(self.spriteImage1[self.currentImage],(self.x_loc,self.y_loc))
            if self.useSpriteImage == 1:
                self.scene.gameDisplay.blit(self.spriteImage2[self.currentImage],(self.x_loc,self.y_loc))

    def scale(self, x_scale, y_scale):
        self.x_scale = x_scale
        self.y_scale = y_scale
        if self.useSpriteImage == 0:
            self.spriteImage1[self.currentImage] = pygame.transform.scale(self.spriteImage1[self.currentImage],(x_scale, y_scale))
        if self.useSpriteImage == 1:
            self.spriteImage2[self.currentImage] = pygame.transform.scale(self.spriteImage2[self.currentImage],(x_scale, y_scale))
        self.scaled = True

    def rotate(self, angle):
        if self.useSpriteImage == 0:
            self.spriteImage1[self.currentImage] = pygame.transform.rotate(self.spriteImage1[self.currentImage], angle)
        if self.useSpriteImage == 1:
            self.spriteImage2[self.currentImage] = pygame.transform.rotate(self.spriteImage2[self.currentImage], angle)

    def flip(self, xbool, ybool):
        if self.useSpriteImage == 0:
            self.spriteImage1[self.currentImage] = pygame.transform.flip(self.spriteImage1[self.currentImage], xbool, ybool)
        if self.useSpriteImage == 1:
            self.spriteImage2[self.currentImage] = pygame.transform.flip(self.spriteImage2[self.currentImage], xbool, ybool)
        
    def boundingAction(self):
        if self.boundCondition == "wrap":
            if self.x_loc > self.scene.resolution[0]:
                self.x_loc = 0
            elif self.x_loc < 0:
                self.x_loc = self.scene.resolution[0]
            if self.y_loc > self.scene.resolution[1]:
                self.y_loc = 0
            elif self.y_loc < 0:
                self.y_loc = self.scene.resolution[1]
        elif self.boundCondition == "bounce":
            if self.x_loc > self.scene.resolution[0]:
                self.dx = self.dx*-1;
            elif self.x_loc < 0:
                self.dx = self.dx*-1;
            if self.y_loc > self.scene.resolution[1]:
                self.dy = self.dy*-1;
            elif self.y_loc < 0:
                self.dy = self.dy*-1;
        elif self.boundCondition == "none":
            pass
        elif self.boundCondition == "die":
            if(self.alive):
                if self.x_loc > self.scene.resolution[0]:
                    self.alive = False
                elif self.x_loc < 0:
                    self.alive = False
                if self.y_loc > self.scene.resolution[1]:
                    self.alive = False
                elif self.y_loc < 0:
                    self.alive = False

    def getSizeX(self):
        if self.scaled==False:
            return self.spriteImage1[self.currentImage].get_rect().size[0]
        elif self.scaled==True:
            return self.x_scale

    def getSizeY(self):
        if self.scaled==False:
            return self.spriteImage1[self.currentImage].get_rect().size[1]
        elif self.scaled==True:
            return self.y_scale
        
    def getLoc(self):
        return (self.x_loc, self.y_loc)

    def collision(self): #returns "None" if nothing
        
        for i in range(len(self.scene.spriteList)):
            if self.scene.spriteList[i].collisions == False:
                pass
            elif self.scene.spriteList[i] == self:
                pass
            elif self.alive == False:
                pass
            elif self.scene.spriteList[i].collisions == True and self.scene.spriteList[i].alive == True:
                for j in range(len(self.collidesWith)):
                    if(self.collidesWith[j] == self.scene.spriteList[i].classtype):
                        if (self.x_loc < self.scene.spriteList[i].x_loc+self.scene.spriteList[i].getSizeX()) and (self.x_loc + self.getSizeX() > self.scene.spriteList[i].x_loc):
                            if (self.y_loc < self.scene.spriteList[i].y_loc+self.scene.spriteList[i].getSizeY()) and (self.y_loc + self.getSizeY() > self.scene.spriteList[i].y_loc):
                                return self.scene.spriteList[i].classtype
                
                   

def quitEvent(crashed):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
            return crashed

