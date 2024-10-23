import pygame, sys
from pygame.locals import *
import random
import math

# Khởi tạo kích thước cửa sổ
chieu_dai = 800
chieu_rong = 500
pygame.init()
w = pygame.display.set_mode((chieu_dai, chieu_rong))
pygame.display.set_caption('Game Bắn Chim')

# Tạo nền game
anh_nen = pygame.image.load('BG2.png')
anh_nen = pygame.transform.scale(anh_nen, (chieu_dai, chieu_rong))

# Font chữ hiển thị điểm số
font = pygame.font.SysFont(None, 36)

# Tạo ảnh chim
chim1 = pygame.image.load('BIRD.png')
chim1 = pygame.transform.scale(chim1, (80, 70))
chim2 = pygame.image.load('EN.png')
chim2 = pygame.transform.scale(chim2, (80, 70))

# Tọa độ chim
x1, y1 = random.randint(0, chieu_dai-80), random.randint(0, chieu_rong-70)
x2, y2 = random.randint(0, chieu_dai-80), random.randint(0, chieu_rong-70)

# Tạo hitbox cho chim dựa trên kích thước thực tế của ảnh
hitbox1 = chim1.get_rect(topleft=(x1, y1))
hitbox2 = chim2.get_rect(topleft=(x2, y2))

# List đạn
dan_list = []
dan_speed = 10  # Tốc độ đạn
dan_radius = 5   # Kích thước đạn

# Trọng lực để chim rơi xuống khi trúng đạn
gravity = 2

# Thời gian khung hình
FPS = 60
fpsClock = pygame.time.Clock()

# Điểm số
score = 0

# Hàm tính toán vận tốc của đạn theo hướng bấm chuột
def calculate_bullet_velocity(start_pos, mouse_pos, speed):
    dx = mouse_pos[0] - start_pos[0]
    dy = mouse_pos[1] - start_pos[1]
    distance = math.sqrt(dx**2 + dy**2)
    if distance == 0:
        return 0, 0
    return (dx / distance * speed), (dy / distance * speed)

# Kiểm tra chim bị bắn trúng
def chim_bi_ban(hitbox, x, y, gravity):
    y += gravity  # Chim rơi xuống
    if y > chieu_rong:  # Nếu chim rơi xuống hết màn hình
        x, y = random.randint(0, chieu_dai - 80), random.randint(0, chieu_rong - 70)
        hitbox.topleft = (x, y)  # Reset lại vị trí của chim
    return x, y

while True:
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Bấm chuột để bắn đạn
        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = [400, 480]  # Vị trí bắn đạn (giữa màn hình, phía dưới)
            velocity = calculate_bullet_velocity(start_pos, pos, dan_speed)
            dan_list.append([start_pos[0], start_pos[1], velocity[0], velocity[1]])  # Thêm đạn với vận tốc tương ứng

    # Hiển thị ảnh nền
    w.blit(anh_nen, (0, 0))

    # Di chuyển chim
    x1 += 1
    x2 -= 1

    if x1 > chieu_dai:
        x1 = 0
    if x2 < 0:
        x2 = chieu_dai

    # Cập nhật vị trí hitbox khi chim di chuyển
    hitbox1.topleft = (x1, y1)
    hitbox2.topleft = (x2, y2)

    # Di chuyển đạn
    for dan in dan_list[:]:
        dan[0] += dan[2]  # Cập nhật vị trí theo vận tốc
        dan[1] += dan[3]

        # Kiểm tra va chạm với chim
        if hitbox1.collidepoint(dan[0], dan[1]):
            score += 5
            y1 = chieu_rong  # Chim bị bắn trúng và sẽ rơi xuống
            dan_list.remove(dan)
        elif hitbox2.collidepoint(dan[0], dan[1]):
            score += 5
            y2 = chieu_rong  # Chim bị bắn trúng và sẽ rơi xuống
            dan_list.remove(dan)

        # Xóa đạn khi ra khỏi màn hình
        if dan[0] < 0 or dan[0] > chieu_dai or dan[1] < 0 or dan[1] > chieu_rong:
            dan_list.remove(dan)

    # Vẽ chim
    w.blit(chim1, (x1, y1))
    w.blit(chim2, (x2, y2))

    # Vẽ đạn
    for dan in dan_list:
        pygame.draw.circle(w, (255, 0, 0), (int(dan[0]), int(dan[1])), dan_radius)

    # Cập nhật vị trí chim rơi khi bị bắn trúng
    x1, y1 = chim_bi_ban(hitbox1, x1, y1, gravity)
    x2, y2 = chim_bi_ban(hitbox2, x2, y2, gravity)

    # Hiển thị điểm số
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    w.blit(score_text, (10, 10))

    # Cập nhật màn hình và kiểm soát FPS
    pygame.display.update()
    fpsClock.tick(FPS)
