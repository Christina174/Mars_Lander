import pygame
import random
import time

pygame.init()
width = 500
height = 500

cadr = pygame.display.set_mode((width,height))

k = random.randint(3, width//50)
v=[]
m = random.randint(0, k-3)

for i in range(0, k):
    y = random.randint(int(height/2), height-25)
    x = random.randint(0, width)
    if i == 0:
        x = 0
    if i == k-1:
        x = width
    v.append([x,y])
v = sorted(v) 

for i in range(1, len(v)-1):
    if v[i][0]-v[i-1][0]<35:
        v[i][0]=v[i-1][0]+35
    else:
        v[i][0]=v[i][0]
v[m+1][1]= v[m][1]

WHITE = (255, 255, 255)
Xsh = width//2
Ysh = 0

clock = pygame.time.Clock()
g = 4
flag = True
PAUSED = False

def Crash():
    global PAUSED
    cadr.fill((0,0,0))
    mount = pygame.draw.aalines(cadr, WHITE, False, v)
    regolit = pygame.draw.line(cadr, WHITE, [0, (height-15)], [width, (height-15)], 5)
    pygame.draw.polygon(cadr, WHITE, [[Xsh, Ysh-15],[Xsh-3, Ysh], [Xsh-20, Ysh-10], [Xsh-15, Ysh+8],[Xsh-30, Ysh+7],[Xsh-18, Ysh+12],[Xsh, Ysh+20], [Xsh+5, Ysh+5],[Xsh+20, Ysh-12], [Xsh+5, Ysh+3]])
    PAUSED = True

def CrossLines(X1,Y1,X2,Y2, X3,Y3,X4,Y4, XR1, YR1, XR2, YR2, XD1, YD1, XD2, YD2):
    global PAUSED
    cL1 = ((X3-X1)*(Y2-Y1)-(Y3-Y1)*(X2-X1))*((X4-X1)*(Y2-Y1)-(Y4-Y1)*(X2-X1))
    cL2 = ((X1-X3)*(Y4-Y3)-(Y1-Y3)*(X4-X3))*((X2-X3)*(Y4-Y3)-(Y2-Y3)*(X4-X3))
    
    cR1 = ((XR1-X1)*(Y2-Y1)-(YR1-Y1)*(X2-X1))*((XR2-X1)*(Y2-Y1)-(YR2-Y1)*(X2-X1))
    cR2 = ((X1-XR1)*(YR2-YR1)-(Y1-YR1)*(XR2-XR1))*((X2-XR1)*(YR2-YR1)-(Y2-YR1)*(XR2-XR1))
    
    cD1 = ((XD1-X1)*(Y2-Y1)-(YD1-Y1)*(X2-X1))*((XD2-X1)*(Y2-Y1)-(YD2-Y1)*(X2-X1))
    cD2 = ((X1-XD1)*(YD2-YD1)-(Y1-YD1)*(XD2-XD1))*((X2-XD1)*(YD2-YD1)-(Y2-YD1)*(XD2-XD1))

    if cL1<=0 and cL2<=0 and cL1 == cR1:
        if X3-X1> X2-XR1:
            Earth (X3-15, Y1)
        else:
            Earth (XR1, Y1)
    elif cL1<=0 and cL2<=0 and cL1 != cR1 or cD1<=0 and cD2<=0:
        Crash()
    elif cR1<=0 and cR2<=0 and cL1 != cR1:
        Crash()

def Earth (coordX, Y1):
    global PAUSED
    cadr.fill((0,0,0))
    mount = pygame.draw.aalines(cadr, WHITE, False, v)
    regolit = pygame.draw.line(cadr, WHITE, [0, (height-15)], [width, (height-15)], 5)
    clock.tick(10)
    shattle = pygame.draw.aalines(cadr, WHITE, True, [[Xsh, Y1-25], [Xsh-10, Y1-15], [Xsh-7, Y1-10],[Xsh-10, Y1], [Xsh-7, Y1-10], [Xsh+7, Y1-10],[Xsh+10, Y1], [Xsh+7, Y1-10],[Xsh+10, Y1-15]])
    pygame.draw.aalines(cadr, WHITE, True, [[coordX+3, Y1], [coordX+3, Y1-15], [coordX+10, Y1-15], [coordX+10, Y1-10], [coordX+3, Y1-10]])
    PAUSED = True
        
while flag:
    if PAUSED == False:
        prop1 = ([Xsh-10, Ysh+25], [Xsh-7, Ysh+15])
        prop2 = ([Xsh+10, Ysh+25], [Xsh+7, Ysh+15])
        downS = ([Xsh-7, Ysh+15], [Xsh+7, Ysh+15])
        
        cadr.fill((0,0,0))
        mount = pygame.draw.aalines(cadr, WHITE, False, v)
        regolit = pygame.draw.line(cadr, WHITE, [0, (height-15)], [width, (height-15)], 5)
        clock.tick(10)
        f = random.randint(15,35)
        fire = pygame.draw.ellipse(cadr, WHITE, (Xsh-7, Ysh+15, 14, f))
        shattle = pygame.draw.aalines(cadr, WHITE, True, [[Xsh, Ysh], [Xsh-10, Ysh+10], [Xsh-7, Ysh+15],[Xsh-10, Ysh+25], [Xsh-7, Ysh+15], [Xsh+7, Ysh+15],[Xsh+10, Ysh+25], [Xsh+7, Ysh+15],[Xsh+10, Ysh+10]])
        
        #ускорение свободного падения
        Ysh += g
        
        if Xsh+10>=width or Xsh-10 <=0 or Ysh+25>=height-15:
            Crash()       
            PAUSED = True
        
        for i in pygame.event.get():
            key_list = pygame.key.get_pressed()
            if i.type == pygame.QUIT:
                exit()
            elif i.type == pygame.KEYDOWN:
                if i.key == pygame.K_LEFT:
                    Xsh -= 12
                elif i.key == pygame.K_RIGHT:
                    Xsh += 12
                elif key_list[pygame.K_p]:
                    PAUSED = not PAUSED
        
        #столкновение с отвесной поверхностью. Проверка пересечения отрезков
        for i in range(len(v)-1):
            #print(v[i][0])
            CrossLines(v[i][0],v[i][1],v[i+1][0],v[i+1][1], prop1[0][0],prop1[0][1],prop1[1][0],prop1[1][1], prop2[0][0],prop2[0][1],prop2[1][0],prop2[1][1], downS[0][0],downS[0][1],downS[1][0],downS[1][1]) 
        
    for e in pygame.event.get():
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                PAUSED = not PAUSED
        if e.type == pygame.QUIT:
                exit()
    pygame.display.update()
