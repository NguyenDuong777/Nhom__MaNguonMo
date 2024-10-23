# ăn táo bằng cách bấm chuột vào quả táo. khi ăn 1 quả táo được 5 điểm
import pygame, sys
from pygame.locals import *
import random
import time   # gọi thư viện thời gian
WINDOWWIDTH = 800 # Chiều dài cửa sổ
WINDOWHEIGHT = 500 # Chiều cao cửa sổ
pygame.init()
w = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
ytao = 0
ycam = 0
yxoai = 0
y_b = 0

#pygame.display.set_caption('Hinh  chuyen dong')
#oto = pygame.image.load('car.png') # đọc 1 file ảnh vào chương trình

BG = pygame.image.load('BACKGROUND.jpg')
BG = pygame.transform.scale(BG, (WINDOWWIDTH, WINDOWHEIGHT))
#w.blit(BG,(0,0))
tao = pygame.image.load('Tao.png')
tao = pygame.transform.scale(tao, (40, 50))
cam = pygame.image.load('ORANGE.png')
xoai = pygame.image.load('Xoai.png')
cam = pygame.transform.scale(cam, (40, 50))
xoai = pygame.transform.scale(xoai, (40, 50))
width_img = BG.get_width()
FPS = 20
fpsClock = pygame.time.Clock()
clock = pygame.time.Clock()
diem = 0
time0 = time.time()
toc_do = 1
while True:
    
    for event in pygame.event.get():
        if event.type == QUIT :
            
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:  # sự kiện bấm chuột
            if event.pos[0]>410 and event.pos[0]<490 and event.pos[1]>ytao-50 and event.pos[1]<ytao+50:
            # event.pos[0] =x  và event.pos[1] =y   
               diem = diem +5
               ytao = 0
        if event.type ==pygame.KEYDOWN:
            if event.key == K_UP:
                toc_do = toc_do +5

               
    #w.fill((255, 200, 100)) # đổ màu nền của cửa sổ game
    w.blit(BG,(0,y_b))
    #w.blit(BG,(0,y_b+WINDOWHEIGHT))
    #y_b = y_b -5
    w.blit(tao, (450,ytao)) # vẽ ảnh vừa đọc vào cửa sổ
    w.blit(cam, (250,ycam))
    w.blit(xoai, (350,yxoai))
    ytao = ytao+ toc_do
    ycam = ycam+10
    yxoai = yxoai+20
    #if y_b < - WINDOWHEIGHT:
    #   y_b += WINDOWHEIGHT
    if ytao  > WINDOWHEIGHT:
        ytao =0
        toc_do  =1
        
    if ycam  > WINDOWHEIGHT:
        ycam =0
    if yxoai  > WINDOWHEIGHT:
        yxoai =0
    
    time1 = time.time()
    #print(time)
    font = pygame.font.SysFont('Arial', 30)
    text = font.render('Tong diem: {} '.format(diem), True, (255, 0, 0)) # in ra màn hình tổng điểm
    text1 = font.render('Thoi gian: {} '.format(int(time1-time0)), True, (255, 0, 0)) # in ra màn hình thời gian chơi
    text = font.render('Tong diem: {} '.format(diem), True, (255, 0, 0))
    w.blit(text, (50, 50))
    w.blit(text1, (50, 80))
    
    pygame.display.update() # vẽ lại hình trong vòng lặp
    fpsClock.tick(FPS)
   
'''Bài tập :
    1) tìm hoặc vẽ 2 con chim. Viết chương trinh cho 1 con chim bay từ trái qua phải, 1 con bay từ phải qua trái màn hình
    2) Tìm hoặc vẽ 2 ô tô, cho 2 ô tô chuyển động với vận tốc khác nhau
    3) vẽ 10 hình tròn với 10 màu khác nhau chuyển động từ trên xuống dưới màn hình với 10 tốc độ khác nhau'''
