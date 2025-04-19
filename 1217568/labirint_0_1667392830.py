from pygame import *
mixer.init()
mixer.music.load('mainmenu_AIwQm69j.mp3')
mixer.music.play(-1)
mixer.music.set_volume(0.03)
lose = mixer.Sound('wastedsound.mp3')
winpobeda = mixer.Sound('gimn-vi-ka_yvegPb5u.mp3')
boom = mixer.Sound('9mm-pistol-shoot-short-reverb-7152.wav')
boom.set_volume(0.02)
winpobeda.set_volume(0.15)
lose.set_volume(0.15)
win_width = 1450
win_height = 780
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load("cs2mirage.webp"), (win_width, win_height))
 
#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x 
        self.rect.y = player_y
 
    #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
        self.direction = "right"
        self.image_right = transform.scale(image.load("hitman1_gun.png"), (size_x, size_y))
        self.image_left = transform.scale(image.load("hitman2_gun.png"), (size_x, size_y))
    
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self): 
        # Спершу рух по горизонталі
        if packman.rect.x <= win_width-20 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        if self.x_speed > 0:
            self.direction = "right"
            self.image = self.image_right
        elif self.x_speed < 0:
            self.direction = "left"
            self.image = self.image_left
            # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if packman.rect.y <= win_height-20 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # йдемо вниз
            for p in platforms_touched:
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    def fire(self):
        boom.play()
        if self.direction == "right":
            bullet = Bullet('yellow_hand.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        else:
            bullet = Bullet('yellow_hand.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
#клас спрайту-ворога
class Enemy_h(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 =x1
        self.x2 =x2

   #рух ворога
    def update(self):
        if self.rect.x <= self.x1: 
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 =y1
        self.y2 =y2

   #рух ворога
    def update(self):
        if self.rect.y <= self.y1: #w1.wall_x + w1.wall_width
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #рух ворога
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width+10 or self.rect.x < -10:
            self.kill()
# Таймер
font.init()
font_timer = font.Font(None, 36)
start_time = time.get_ticks()
countdowntime = 67
wasted_image = transform.scale(image.load("wasted.jpg"), (win_width, win_height))

def draw_timer():
    vremya = (time.get_ticks() - start_time) // 1000
    remaining_time = max(countdowntime - vremya, 0)
    if remaining_time == 0:
        img = image.load('wasted2.jpg')
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        finish = True
    else:         
        timer_text = font_timer.render(f'Time: {remaining_time}', True, (255, 255, 255))
        text_rect = timer_text.get_rect(center=(win_width // 2, 20))
        window.blit(timer_text, text_rect)


#Створюємо віконце
 # задаємо колір відповідно до колірної схеми RGB

#Створюємо групу для стін
barriers = sprite.Group()

bullets = sprite.Group()



w1 = GameSprite('linia.png', 190, 110, 22, 635)
w2 = GameSprite('linia2.png', 200, 100, 200, 22)
w3 = GameSprite('linia.png', 388, 110, 22, 200)
w4 = GameSprite('linia2.png', 398, 300, 150, 22)
w5 = GameSprite('linia.png', 535, 310, 22, 100)
w6 = GameSprite('linia2.png', 396, 400, 150 , 22)
w7 = GameSprite('linia2.png', 396, 580, 105, 22)
w8 = GameSprite('linia.png', 388, 495, 22, 100)
w9 = GameSprite('linia2.png', 396, 485, 370, 22)
w10 = GameSprite('linia.png', 755 , 495, 22, 100)
w11 = GameSprite('linia2.png', 660, 580, 105, 22)
w12 = GameSprite('linia2.png', 550, 100, 880, 22)
w13 = GameSprite('linia.png', 540, 110, 22, 95)
w14 = GameSprite('linia.png', 1420, 110, 22, 635)
w15 = GameSprite('linia.png', 700, 275, 22, 220)
w16 = GameSprite('linia2.png', 708, 265, 200, 22)
w17 = GameSprite('linia.png', 897   , 275, 22, 55)
w18 = GameSprite('linia2.png', 707, 395,  725  , 22)
w19 = GameSprite('linia2.png', 198  , 735, 1235, 22)
w20 = GameSprite('linia.png', 1100, 544, 22, 200)
w21 = GameSprite('linia2.png', 935, 533, 350, 22)
w22 = GameSprite('linia.png', 1100, 110, 22, 180)
w23 = GameSprite('linia2.png', 1110, 280, 200, 22)
w24 = GameSprite('linia.png', 1300, 110, 20, 22)
barriers.add(w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23, w24 )
bonus = sprite.Group()
b1 = (GameSprite('defusaaaa-removebg-preview.png', 540, 500, 100, 100))
b2 = (GameSprite('defusaaaa-removebg-preview.png', 450, 308, 100, 100))
b3 = (GameSprite('defusaaaa-removebg-preview.png', 730, 265, 100, 100))
b4 = (GameSprite('defusaaaa-removebg-preview.png', 1150, 130, 100, 100))
b5 = (GameSprite('defusaaaa-removebg-preview.png', 1000, 540, 100, 100))

bonus.add(b1, b2 , b3, b4, b5)
num = 0
def draw_bonus_counter():
    bonus_text = font_timer.render(f'Бонусів зібрали: {num} / 5', True, (255, 255, 255))
    window.blit(bonus_text, (10, 10))
monsters = sprite.Group()
#створюємо спрайти
packman = Player('hitman1_gun.png', 55, win_height - 150, 50 , 50, 0, 0)
monster = Enemy_h('robot1_gun.png', win_width - 1350, 180, 50, 50, 5,  25, 150)
monster2 = Enemy_h('robot1_gun.png', 700, 515, 50, 50, 5, 650, 695)
monster3 = Enemy_h('robot2_gun.png', 415, 515, 50, 50, 5, 410, 460)
monster4 = Enemy_h('robot1_gun.png', 445,  330, 50, 50, 5, 390, 460)
monster5 = Enemy_h('robot2_gun.png', 1150,  590, 40, 40, 5, 1145, 1210)
monster6 = Enemy_h('robot2_gun.png', 710, 430, 50, 50, 5, 705, 760)
monster7 = Enemy_h('robot2_gun.png', 710, 345, 50, 50, 5, 705, 900)
monster8 = Enemy_v('robot1_gun.png', 1150, 355, 40, 43, 5, 290, 355)
monster9 = Enemy_v('robot1_gun.png', 1150, 495, 40, 43, 5, 420, 500)
monster10 = Enemy_v('robot1_gun.png', 700, 615, 50, 50, 5, 605, 700)
monsters.add(monster, monster2, monster3, monster4, monster5, monster6, monster7, monster8, monster9, monster10)
final_sprite = GameSprite('bomba-removebg-preview.png', 1150, 650, 80, 80)

#змінна, що відповідає за те, як закінчилася гра
finish = False
def draw_timer():
    global finish
    vremya = (time.get_ticks() - start_time) // 1000
    remaining_time = max(countdowntime - vremya, 0)
    if remaining_time == 0:
        finish = True
        mixer.music.stop()
        lose.play()
        img = image.load('wasted3.jpg')
        window.blit(transform.scale(img, (win_width, win_height)), (0, 0)) 
    else:         
        timer_text = font_timer.render(f'Time: {remaining_time}', True, (255, 255, 255))
        text_rect = timer_text.get_rect(center=(win_width // 2, 20))
        window.blit(timer_text, text_rect)
#ігровий цикл
start_screen = transform.scale(image.load("kontra.jpg"), (win_width, win_height))
game_started = False

while not game_started:
    window.blit(start_screen, (0, 0))
    display.update()
    for e in event.get():
        if e.type == QUIT:
            exit()
        elif e.type == KEYDOWN and e.key == K_RETURN: 
            game_started = True
run = True
while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -6
            elif e.key == K_RIGHT:
                packman.x_speed = 6
            elif e.key == K_UP :
                packman.y_speed = -6
            elif e.key == K_DOWN :
                packman.y_speed = 6
            elif e.key == K_SPACE:
                packman.fire()
 
        elif e.type == KEYUP:
            if e.key == K_LEFT :
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0
    if not finish:
        window.blit(back, (0, 0))
        #малюємо об'єкти  
        packman.update()
        bullets.update()
        bonus.draw(window)
        draw_bonus_counter()
        packman.reset()
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
        sprite.groupcollide(monsters,bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets , barriers , True, False)
        draw_timer()
        
        #включаємо рух
        if sprite.spritecollide(packman, bonus, True):
            num += 1
            packman.x_speed += 3 if packman.x_speed > 0 else -3
            packman.y_speed += 3 if packman.y_speed > 0 else -3
        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            mixer.music.stop()
            lose.play()
            img = image.load('wasted3.jpg')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        if  num == 5 and sprite.collide_rect(packman, final_sprite):
            finish = True
            mixer.music.stop()
            winpobeda.play()
            img = image.load('top.jpg')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
        
   
        #цикл спрацьовує кожну 0.05 секунд
        display.update()