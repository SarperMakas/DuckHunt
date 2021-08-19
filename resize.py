import ctypes, pygame


class Resize:
    def __init__(self, W, H):
        self.w = W
        self.h = H
        self.Log = [(self.w, self.h), (self.w, self.h)]
        self.user = ctypes.windll.user32
        self.relW = self.user.GetSystemMetrics(0)
        self.relH = int(self.user.GetSystemMetrics(1) - self.user.GetSystemMetrics(1) // 20.5 + (self.user.GetSystemMetrics(1)*1.017518248175182 - self.user.GetSystemMetrics(1)))
        self.wh_Ratio = self.relW / self.relH
        self.hw_Ratio = self.relH / self.relW
        self.screenW = W
        self.screenH = H

    def resizeScreen(self):
        newScreen = pygame.display.set_mode((self.screenW, self.screenH), pygame.RESIZABLE)
        return newScreen

    def resizeWidthHeight(self, eventW, eventH):
        if self.screenW != eventW:
            self.screenW = int(eventW)
            self.screenH = int(self.screenW // self.wh_Ratio)
        else:
            self.screenH = int(eventH)
            self.screenW = int(self.screenH // self.hw_Ratio)

        self.Log.append((self.screenW, self.screenH))
        return self.screenW, self.screenH


    def resizeIMG(self, IMGPath, imgSize):

        """ratioW = self.screenW / imgSize[0]
        ratioH = self.screenH / imgSize[1]

        sizeW = self.Log[-1][0] - self.Log[-2][0]
        sizeH = self.Log[-1][1] - self.Log[-2][1]

        W = imgSize[0] + sizeW/ratioW
        H = imgSize[1] + sizeH/ratioH"""

        ratioW = self.Log[-2][0] / imgSize[0]
        ratioH = self.Log[-2][1] / imgSize[1]

        W = self.screenW / ratioW
        H = self.screenH / ratioH

        if type(IMGPath) == str:
            newIMG = pygame.transform.scale(pygame.image.load(IMGPath).convert_alpha(), (int(W), int(H)))
        else:
            newIMG = pygame.transform.scale(IMGPath.convert_alpha(), (int(W), int(H)))

        return newIMG


    def resizeFont(self, normalPNT, ttf):
        font = pygame.font.Font(f'{ttf}', int(normalPNT * self.screenH / self.h))
        return font



def main():
    screen = pygame.display.set_mode((1000, 700), pygame.RESIZABLE)
    img = pygame.image.load("../Flappy Bird/IMG/Flappy Bird.png")
    imgSize = img.get_size()
    clock = pygame.time.Clock()
    r = Resize(1000, 700)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.VIDEORESIZE:
                r.resizeWidthHeight(event.w, event.h)
                screen = r.resizeScreen()
                img = r.resizeIMG("Flappy Bird/IMG/Flappy Bird.png", imgSize)

        screen.fill((255, 0, 0))
        screen.blit(img, (screen.get_width()/2-img.get_width()/2, screen.get_height()/2-img.get_height()/2))
        pygame.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
