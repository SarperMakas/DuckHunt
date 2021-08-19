import pygame as pg
from resize import Resize
import random

pg.init()


class BG:
    def __init__(self, W, H, screen, resize, PATH, pos):
        self.w = W
        self.h = H
        self.pos = pos
        self.PATH = PATH
        self.resize = resize
        self.screen = screen
        self.img = pg.transform.scale(pg.image.load(self.PATH), (self.w, self.h))
        self.imgSize = self.img.get_size()

    def resizeMenu(self, w, h):
        self.w, self.h = w, h
        self.img = pg.transform.scale(pg.image.load(self.PATH), (self.w, self.h))
        self.imgSize = self.img.get_size()

    def draw(self):
        self.screen.blit(self.img, self.pos)



class IMG:
    def __init__(self, W, H, screen, resize, mode, PATHList):
        self.h = H
        self.w = W
        self.PATH = PATHList
        self.resize = resize
        self.screen = screen
        self.mode = mode
        self.rect = None
        self.img, self.iW, self.iH, self.imgSize = [], [], [], []

        for path in self.PATH:
            self.img.append(pg.image.load(path))
        for img in self.img:
            self.iW.append(img.get_width())
            self.iH.append(img.get_height())

        for i in range(len(self.img)):
            # img - int((img - img/4)/4)
            if self.mode == "Costume":
                self.img[i] = self.resize.resizeIMG(f"{self.PATH[i]}", (self.w, (self.iH[i] - int((self.iH[i] - self.iH[i] / 4) / 4)))).convert_alpha()
            else:
                self.img[i] = self.resize.resizeIMG(f"{self.PATH[i]}", (
                           self.iW[i] - int((self.iW[i] - self.iW[i] / 4) / 4), (self.iH[i] - int((self.iH[i] - self.iH[i] / 4) / 4)))).convert_alpha()

        for img in self.img:
            self.imgSize = img.get_size()

    def draw(self, posList, unDraws=None):
        self.rect = posList
        for i in range(len(self.img)):
            if i != unDraws:
                rect = posList[i]
                self.screen.blit(self.img[i], rect)

    def resizeIMG(self, w, h):
        self.w = w
        self.h = h
        for i in range(len(self.img)):
            self.img[i] = self.resize.resizeIMG(f"{self.PATH[i]}", self.imgSize).convert_alpha()
        self.imgSize = self.img[0].get_size()



class Duck:
    def __init__(self, W, H, screen, resize):
        self.w = W
        self.h = H
        self.screen = screen
        self.resize = resize
        self.clap = 0
        self.movement = 0
        self.gravity = self.h / 2000

        self.duckFall = pg.image.load("Duck/duckfall.png").convert_alpha()
        self.duckFall = pg.transform.scale(self.duckFall, (int(self.duckFall.get_width()//1.5), int(self.duckFall.get_height()//1.5)))

        self.duckRight1 = pg.image.load("Duck/duckright1.png").convert_alpha()
        self.duckRight2 = pg.image.load("Duck/duckright2.png").convert_alpha()
        self.duckRight3 = pg.image.load("Duck/duckright3.png").convert_alpha()
        self.duckRightList = [pg.transform.scale(self.duckRight1, (int(self.duckRight1.get_width() // 1.5), int(self.duckRight1.get_height() // 1.5))),
                              pg.transform.scale(self.duckRight2, (int(self.duckRight2.get_width() // 1.5), int(self.duckRight2.get_height() // 1.5))),
                              pg.transform.scale(self.duckRight3, (int(self.duckRight3.get_width() // 1.5), int(self.duckRight3.get_height() // 1.5)))]

        self.clapDict = {0: self.duckRightList[0], 1: self.duckRightList[1], 2: self.duckRightList[2]}

        self.duckShot = pg.image.load("Duck/duckshot.png").convert_alpha()
        self.duckShot = pg.transform.scale(self.duckShot, (int(self.duckShot.get_width()//1.5), int(self.duckShot.get_height()//1.5)))

        self.duckFlayAway1 = pg.image.load("Duck/flyaway1.png").convert_alpha()
        self.duckFlayAway2 = pg.image.load("Duck/flyaway2.png").convert_alpha()
        self.duckFlayAway3 = pg.image.load("Duck/flyaway3.png").convert_alpha()
        self.duckFlayAwayList = [pg.transform.scale(self.duckFlayAway1, (int(self.duckFlayAway1.get_width()//1.5), int(self.duckFlayAway1.get_height()//1.5))),
                                 pg.transform.scale(self.duckFlayAway2, (int(self.duckFlayAway2.get_width()//1.5), int(self.duckFlayAway2.get_height()//1.5))),
                                 pg.transform.scale(self.duckFlayAway3, (int(self.duckFlayAway3.get_width()//1.5), int(self.duckFlayAway3.get_height()//1.5)))]

        self.duckLeftList = []
        for img in self.duckRightList:
            self.duckLeftList.append(pg.transform.flip(img, True, False))

        self.duckList = self.duckRightList + self.duckFlayAwayList + [self.duckFall, self.duckShot]

        self.PATH = ["Duck/duckright1.png", "Duck/duckright2.png", "Duck/duckright3.png", "Duck/flyaway1.png",
                     "Duck/flyaway2.png", "Duck/flyaway3.png", "Duck/duckfall.png", "Duck/duckshot.png"]
        self.imgSize = []
        for img in self.duckList:
            self.imgSize.append(img.get_size())

        self.chosenImg = self.clapDict[self.clap].convert_alpha()
        self.chosenImgRect = self.chosenImg.get_rect(center=(500, 200))


    def resizeDuck(self, w, h):
        self.w = w
        self.h = h
        for index, img in enumerate(self.duckList):
            img = self.resize.resizeIMG(f"{self.PATH[index]}", self.imgSize[index])
            del self.duckList[index]
            self.duckList.insert(index, img)
            self.imgSize[index] = img.get_size()
        self.duckRightList = self.duckList[0:4]
        self.duckFlayAwayList = self.duckList[4:6]
        self.duckFall = self.duckList[6]
        self.duckShot = self.duckList[7]
        self.chosenImg = self.resize.resizeIMG(self.chosenImg, self.chosenImg.get_size())
        self.duckLeftList[0] = self.resize.resizeIMG(self.duckLeftList[0], self.duckLeftList[0].get_size())
        self.duckLeftList[1] = self.resize.resizeIMG(self.duckLeftList[1], self.duckLeftList[1].get_size())
        self.duckLeftList[2] = self.resize.resizeIMG(self.duckLeftList[2], self.duckLeftList[2].get_size())




    def draw(self):
        self.screen.blit(self.chosenImg, self.chosenImgRect)


class Dog:
    def __init__(self, W, H, screen, resize):
        self.w = W
        self.h = H
        self.movement = 0
        self.gravity = self.h/2500
        self.screen = screen
        self.resize = resize
        self.dogCaught = pg.image.load("Dog/dogcaughtduck.png").convert_alpha()
        self.dogLaugh1 = pg.image.load("Dog/doglaughing1.png").convert_alpha()
        self.dogLaugh2 = pg.image.load("Dog/doglaughing2.png").convert_alpha()
        self.IMG = self.dogCaught
        self.IMGRect = self.dogCaught.get_rect(center=(self.w - self.w/5, self.h - self.h / 10))

    def resizeIMG(self, w, h, move):
        self.w = w
        self.h = h
        self.dogCaught = self.resize.resizeIMG("Dog/dogcaughtduck.png", self.dogCaught.get_size())
        self.dogLaugh1 = self.resize.resizeIMG("Dog/doglaughing1.png", self.dogLaugh1.get_size())
        self.dogLaugh2 = self.resize.resizeIMG("Dog/doglaughing2.png", self.dogLaugh1.get_size())
        self.IMG = self.resize.resizeIMG(self.IMG, self.IMG.get_size())
        self.IMGRect = self.dogCaught.get_rect(center=(self.w - self.w/5, self.h - self.h / 10 - move))

    def draw(self):
        self.screen.blit(self.IMG, self.IMGRect)


class Game:
    def __init__(self):
        self.W = 1120
        self.H = 609
        self.dogMoveCount = 0

        self.duckMove = True
        self.dogLaugh = 0
        self.dogWait = 0
        self.flayAway = 0
        self.startCount = False
        self.gameEnd = False
        self.pr = 0
        self.duckFall = True

        self.shotCount = 3
        self.roundCount = 1
        self.scoreCount = 0
        self.mousePos = pg.mouse.get_pos()

        self.duckDirections = ["right", "left", "up", "down"]
        self.backCountForMove = 35
        self.chosenDirection = "right"
        self.chosenDirectionIndex = 0
        self.dirRightOrLeft = "right"
        self.count = 20

        self.duckColor = ["W", "W", "W", "W", "W", "W", "W", "W"]
        self.draw = 0
        self.dogMode = "Normal"
        self.duckShotCount = 0
        self.state = "Menu"
        self.clock = pg.time.Clock()
        self.resize = Resize(self.W, self.H)
        self.screen = pg.display.set_mode((self.W, self.H), pg.RESIZABLE)
        self.bg = BG(self.W, self.H, self.screen, self.resize, "Screen/DuckScreen.png", (0, 0))

        self.sq = pg.transform.scale(pg.image.load("Screen/LittleCursor.png").convert_alpha(), (1, 1))
        self.sqRect = self.sq.get_rect(center=self.mousePos)

        self.costume = IMG(self.W, self.H, self.screen, self.resize, "Costume", ["Screen/Costume.png"])
        self.hitCounter = IMG(self.W, self.H, self.screen, self.resize, "HitCounter", ["HitCounter/hitcounter.png"])
        self.shot = IMG(self.W, self.H, self.screen, self.resize, "Shot", [f"Shot/{self.shotCount}shot.png"])
        self.score = IMG(self.W, self.H, self.screen, self.resize, "Score", ["Screen/ScoreCounter.png"])
        self.round = IMG(self.W, self.H, self.screen, self.resize, "Round", ["Screen/RoundCounter.png"])
        self.cursor = IMG(self.W, self.H, self.screen, self.resize, "Cursor", ["Screen/Cursor.png"])
        self.hitCounterDUCKS = IMG(self.W, self.H, self.screen, self.resize, "Ducks", ["HitCounter/duckW.png" for _ in range(8)])
        self.font = pg.font.Font("04B_19.ttf", 20)
        self.duck = Duck(self.W, self.H, self.screen, self.resize)
        self.dog = Dog(self.W, self.H, self.screen, self.resize)


    def drawGame(self):
        self.duck.draw()
        self.dog.draw()
        rect = self.costume.img[0].get_rect(center=(self.costume.w / 2, self.costume.h-self.costume.imgSize[1]/2))
        self.costume.draw([rect])
        rect = self.hitCounter.img[0].get_rect(center=(self.hitCounter.w / 2, self.hitCounter.h - self.hitCounter.h / 10))
        self.hitCounter.draw([rect])
        rect = self.shot.img[0].get_rect(center=(self.shot.w / 2 - self.shot.w / 3, self.shot.h - self.shot.h / 10))
        self.shot.draw([rect])
        rect = self.score.img[0].get_rect(center=(self.score.w / 2 + self.score.w / 3.875, self.score.h - self.score.h / 10))
        self.score.draw([rect])
        rect = self.score.img[0].get_rect(center=(self.score.w / 2 + self.score.w / 2.5, self.score.h - self.score.h / 10))
        self.round.draw([rect])

        rect = self.cursor.img[0].get_rect(center=self.mousePos)
        self.cursor.draw([rect])

        w, h = self.hitCounter.img[0].get_size()
        dw, dh = self.hitCounterDUCKS.img[0].get_size()
        rect = []
        for i in range(1, 9):
            rect.append((self.hitCounter.w / (35/i)+w+w/8, self.hitCounter.h - self.hitCounter.h / 10-dh))

        if 0 < self.draw % 50 < 20:
            self.hitCounterDUCKS.draw(rect, self.roundCount-1)
        else:
            self.hitCounterDUCKS.draw(rect)

        self.drawText()

        self.mousePos = pg.mouse.get_pos()
        self.sqRect = self.sq.get_rect(center=self.mousePos)
        self.screen.blit(self.sq, self.sqRect)

    def drawText(self):
        text = self.font.render(f"{self.scoreCount}", False, (200, 200, 200))
        rect = text.get_rect(center=(self.score.w / 2 + self.score.w / 3.875, self.score.h - self.score.h / 10 - text.get_height()/3))
        self.screen.blit(text, rect)

        text = self.font.render(f"{self.roundCount}", False, (200, 200, 200))
        rect = text.get_rect(center=(self.score.w / 2 + self.score.w / 2.5, self.score.h - self.score.h / 10 - text.get_height()/3))
        self.screen.blit(text, rect)

    def checkMask(self):
        sqRect = self.cursor.img[0].get_rect(center=pg.mouse.get_pos())
        if self.duck.chosenImgRect.colliderect(sqRect):
            chosenImgMask = pg.mask.from_surface(self.duck.chosenImg)
            sqMask = pg.mask.from_surface(self.cursor.img[0])
            offset = (sqRect.x - self.duck.chosenImgRect.x, sqRect.y - self.duck.chosenImgRect.y)
            point = chosenImgMask.overlap(sqMask, offset)
            if point:
                return True
            else:
                return False

    def mouse(self):
        if self.duckMove is True and self.gameEnd is False:
            self.shotCount -= 1
            if self.checkMask() is True:
                self.duck.chosenImg = self.duck.duckShot
                self.duck.chosenImgRect = self.duck.chosenImg.get_rect(center=self.duck.chosenImgRect.center)
                self.dog.IMG = self.dog.dogCaught
                self.hitCounterDUCKS.img[self.roundCount-1] = pg.transform.scale(pg.image.load("HitCounter/duckR.png"), self.hitCounterDUCKS.img[0].get_size())
                self.startCount = True
            elif self.shotCount == 0:
                self.dogMode = "Laugh"

    def mainResize(self, W, H):
        self.screen = self.resize.resizeScreen()
        self.bg.resizeMenu(W, H)
        self.costume.resizeIMG(W, H)
        self.hitCounter.resizeIMG(W, H)
        self.shot.resizeIMG(W, H)
        self.score.resizeIMG(W, H)
        self.round.resizeIMG(W, H)
        self.font = self.resize.resizeFont(20, '04B_19.ttf')
        self.hitCounterDUCKS.resizeIMG(W, H)
        self.duck.resizeDuck(W, H)
        self.duck.gravity = self.H/2000
        self.dog.gravity = self.H/2500
        self.dog.resizeIMG(W, H, self.dogMoveCount*self.H / 304.5)

    def duckLaughFunction(self):
        self.dogLaugh += 1
        if self.dogLaugh % 15 == 0:
            self.dog.IMG = self.dog.dogLaugh1
        if self.dogLaugh % 17 == 0:
            self.dog.IMG = self.dog.dogLaugh2
        self.duckMove = False

    def dogGoUp(self):
        self.dog.movement += self.dog.gravity
        self.dog.IMGRect.y -= self.dog.movement
        self.dogWait += 1
        if self.duck.chosenImgRect.top >= int(self.H / 1.432941176470588) and self.dogWait <= 35:
            self.dog.IMG = self.dog.dogCaught
        elif self.dog.IMGRect.top >= self.H / 2.129370629370629 and (
                self.shotCount == 0 and self.duck.chosenImg != self.duck.duckFall):
            self.dog.IMG = self.dog.dogLaugh1

    def GameOverForDuck(self):
        if self.duck.chosenImgRect.x >= self.W // 2:
            self.duck.chosenImg = self.duck.duckFlayAwayList[self.flayAway // 10]
            self.duck.chosenImgRect.x -= 1
            self.duck.chosenImgRect.y -= 3

        elif self.duck.chosenImgRect.x <= self.W // 2:
            img = self.duck.chosenImg = self.duck.duckFlayAwayList[self.flayAway // 10]
            self.duck.chosenImg = pg.transform.flip(img, True, False)
            self.duck.chosenImgRect.x += 1
            self.duck.chosenImgRect.y -= 3
        self.duckFall = False


    def checkAndChangeDuck(self):
        self.flayAway += 1
        if self.flayAway == 30:
            self.flayAway = 0

        self.bg.PATH = "BackGround/flyaway.png"
        self.bg.img = pg.transform.scale(pg.image.load(self.bg.PATH), (self.bg.w, self.bg.h))


    def checkEndRound(self, dog):
        if self.duck.chosenImgRect.bottom <= 0 or dog is True:
            self.duckDirections = ["right", "left", "up", "down"]
            self.backCountForMove = 35
            self.chosenDirection = "right"
            self.chosenDirectionIndex = 0
            self.dirRightOrLeft = "right"
            self.count = 20
            if self.duck.chosenImgRect.bottom >= 0:
                self.scoreCount += (self.shotCount + 1)
            self.dogMoveCount = 0
            self.duckMove = True
            self.dogLaugh = 0
            self.dogWait = 0
            self.flayAway = 0
            self.gameEnd = False
            self.pr = 0
            self.startCount = False
            self.duck.chosenImg = self.duck.duckList[0]
            self.duck.chosenImgRect.center = (500, 100)
            self.shotCount = 3
            self.dog.IMGRect.center = (self.W - self.W/5, self.H - self.H / 10)
            self.duckShotCount = 0
            self.bg.PATH = "BackGround/background.png"
            self.bg.img = pg.transform.scale(pg.image.load(self.bg.PATH), (self.bg.w, self.bg.h))
            self.duckFall = True
            self.roundCount += 1




    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()

                elif event.type == pg.VIDEORESIZE:
                    self.W, self.H = self.resize.resizeWidthHeight(event.w, event.h)
                    self.mainResize(self.W, self.H)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and self.state == "Menu":
                        self.state = "GameStart"
                        self.bg.PATH = "BackGround/background.png"
                        self.bg.img = pg.transform.scale(pg.image.load(self.bg.PATH), (self.bg.w, self.bg.h))

                if event.type == pg.MOUSEBUTTONDOWN and self.state == "GameStart" and self.duck.chosenImg != self.duck.duckFall:
                    self.mouse()



            # Going down for duck
            if (self.duck.chosenImgRect.y <= self.costume.img[0].get_rect(center=(self.costume.w / 2, self.costume.h-self.costume.imgSize[1]/2)).y+self.H/35) and self.duckShotCount == 15 and self.duckFall is True:
                self.duck.movement += self.duck.gravity
                self.duck.chosenImgRect.y += self.duck.movement

            elif self.duckMove is True:
                if self.backCountForMove == 0:
                    self.chosenDirection = random.choice(self.duckDirections)
                    self.backCountForMove = 35
                else:
                    if self.chosenDirection == "up":
                        self.duck.chosenImgRect.y -= self.W/560
                        self.backCountForMove -= self.W/2240
                        if self.duck.chosenImgRect.y <= 0:
                            self.chosenDirection = "down"
                            self.backCountForMove = self.count

                    elif self.chosenDirection == "down":
                        self.duck.chosenImgRect.y += self.W/560
                        self.backCountForMove -= self.W/2240
                        if self.duck.chosenImgRect.y >= self.H - (self.costume.imgSize[1]+self.H//50):
                            self.chosenDirection = "up"
                            self.backCountForMove = self.count

                    elif self.chosenDirection == "right":
                        self.duck.chosenImgRect.x += self.W/560
                        self.backCountForMove -= self.W/2240
                        if self.duck.chosenImgRect.x >= self.W:
                            self.chosenDirection = "left"
                            self.backCountForMove = self.count
                        self.dirRightOrLeft = "right"

                    elif self.chosenDirection == "left":
                        self.duck.chosenImgRect.x -= self.W/560
                        self.backCountForMove -= self.W/2240
                        if self.duck.chosenImgRect.x <= 0:
                            self.chosenDirection = "right"
                            self.backCountForMove = self.count
                        self.dirRightOrLeft = "left"

                    if self.dirRightOrLeft == "left":
                        self.duck.chosenImg = self.duck.duckLeftList[self.chosenDirectionIndex // 10]
                    elif self.dirRightOrLeft == "right":
                        self.duck.chosenImg = self.duck.duckRightList[self.chosenDirectionIndex // 10]

                    self.chosenDirectionIndex += 1
                    if self.chosenDirectionIndex == 30:
                        self.chosenDirectionIndex = 0

            # Staying few seconds with shot img.
            if self.startCount is True:
                self.duckShotCount += 1
                self.duckMove = False
                self.duck.chosenImg = self.duck.duckShot
            # Changing img to fall
            if self.duckShotCount == 15:
                self.duck.chosenImg = self.duck.duckFall
                self.duck.chosenImgRect = self.duck.chosenImg.get_rect(center=self.duck.chosenImgRect.center)
                self.duck.chosenImg = self.duck.duckFall
                self.startCount = False



            if self.shotCount == 0 and self.duck.chosenImg != (self.duck.duckFall or self.duck.duckShot):
                self.GameOverForDuck()
                self.checkAndChangeDuck()


            # Going up
            if (self.duck.chosenImgRect.top >= int(self.H/1.432941176470588-1) and self.dogWait <= 35) or (self.dog.IMGRect.top >= self.H/2.129370629370629 and (self.shotCount == 0 and self.duck.chosenImg != self.duck.duckFall)):
                self.dogGoUp()
                self.gameEnd = True
            if self.duck.chosenImgRect.top >= int(self.H/1.432941176470588):
                self.pr += 1

            # Laughing:
            if self.dog.IMGRect.top <= self.H/2.129370629370629 and (self.shotCount == 0 and self.duck.chosenImg != self.duck.duckFall):
                self.duckLaughFunction()
                self.gameEnd = True

            if self.pr == 100:
                self.checkEndRound(True)
            else:
                self.checkEndRound(False)

            size = self.shot.img[0].get_size()
            self.shot.img[0] = pg.transform.scale(pg.image.load(self.shot.PATH[0]), (size[0], size[1]))
            self.shot.imgSize = self.shot.img[0].get_size()
            self.shot.PATH[0] = f"Shot/{self.shotCount}shot.png"

            if self.roundCount == 8:
                pg.quit()
                pg.init()
                game = Game()
                game.run()

            self.draw += 1

            self.screen.fill((0, 0, 0))
            self.bg.draw()
            if self.state == "GameStart":
                self.drawGame()
            pg.display.flip()
            self.clock.tick(304)


if __name__ == '__main__':
    Game().run()
