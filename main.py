from random import randint

from pygame import *

win_width = 700
win_height = 500
display.set_caption('Shooter')
window = display.set_mode((win_width, win_height))

img_back = '57939bc82a4cc5c051859b6834c37d89.jpg'
img_back2 = 'msg6626102196-249.jpg'
img_hero = 'photo_5271635579597086264_y-removebg-preview.png'
img_bullet = 'photo_5271635579597086263_y-removebg-preview.png'
img_enemy = 'і-2147483648_-238640-removebg-preview.png'
img_enemy2 = 'photo_5271635579597086262_y-removebg-preview.png'
img_enemy3 = 'photo1714915324__1_-removebg-preview (2).png'

img_back4 = 'fon_5335026234574363357_y.jpg'

score = 0
lost = 0
max_lost = 3
lvl1 = True
lvl2 = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >5:
            self .rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x +=  self.speed
    def fire(self):
        bullet: Bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 100, 80, -10)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

class Enemy (GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = -50
            lost += 1


ship = Player(img_hero, 1, win_height -130, 130, 131, 100)
bullets = sprite.Group()

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(7, win_width-80), -60, 100, 50, randint(1, 5))
    monsters.add(monster)

monsters2 = sprite.Group()
for i in range(1, 6):
    monster2 = Enemy(img_enemy2, randint(7, win_width-80), -60, 75, 44, randint(4, 7))
    monsters2.add(monster2)


#mixer.init()
#mixer.music.load('space.ogg') #music
#mixer.music.play()
#fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
font2 = font.Font(None, 36)
win = font1.render('You win!', True, (255, 255, 255))
lose = font1.render('You lose!', True, (255, 0, 0))


background = transform.scale(image.load(img_back), (win_width, win_height))
finish = False
run = True
goal = 5
goal2 = 10
life = 3
life2 = 3
max_fire = 5
real_time = False
num_fire = 0
from time import time as timer

background2 = transform.scale(image.load(img_back2), (win_width, win_height))


menu = True
game = False
background3 = transform.scale(image.load(img_back4), (win_width, win_height))
while run:

    #menu
    if menu:
        window.blit(background3, (0, 0))
        text_menu = font2.render('Натисніть будь-яку кнопку', True, (255, 255, 255))
        window.blit(text_menu, (190, 400))
        for e in event.get():
            if e.type == KEYDOWN:
                menu = False
                game = True
            elif e.type == QUIT:
                run = False
    if game:



        for e in event.get():
            if e.type == QUIT:
                run = False

            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < max_fire and real_time == False:
                        num_fire += 1
                        # fire_sound.play()
                        ship.fire()
                    if num_fire >= max_fire and real_time == False:
                        last_time = timer()
                        real_time = True

        if lvl1:


            if not finish:
                window.blit(background, (0,0))
                ship.update()
                bullets.update()
                monsters.update()
                text = font2.render('Рахунок:' + str( score), True, (255, 255, 255))
                window.blit(text, (10, 20))
                text_lose = font2.render('Пропущено:' + str( lost), True, (255, 255, 255))
                window.blit(text_lose, (10, 50))

                ship.reset()
                bullets.draw(window)
                monsters.draw(window)
                collides = sprite.groupcollide(monsters, bullets, True, True)
                for c in collides:
                    score += 1
                    monster = Enemy(img_enemy, randint(50, win_width-80), -60, 80, 50, randint(1,5))
                    monsters.add(monster)

                if real_time == True:
                    now_time = timer()
                    if now_time - last_time < 3:
                        reload = font2.render('Wait, reload..', True, (255, 0,0))
                        window.blit(reload, (260, 460))
                    else:
                        real_time = False
                        num_fire = 0
                if life == 3:
                    life_color = (0, 150, 0)
                if life == 2:
                    life_color = (150, 150, 0)
                if life == 1:
                    life_color = (150, 0, 0)
                text_life = font1.render(str(life), True, life_color)
                window.blit(text_life, (650, 10))
                if sprite.spritecollide(ship, monsters, False):
                    sprite.spritecollide(ship, monsters, True)
                    life -= 1
                if life == 0 or lost >= max_lost:
                    finish = True
                    window.blit(lose, (200, 200))



                if score >= goal:
                    #finish = True
                   # window.blit(win, (200, 200))
                    lvl1 = False
                    lvl2 = True
                    num_fire = 0
                    score = 0
                    for b in bullets:
                        b.kill()
                    for m in monsters:
                        m.kill()


        if lvl2:
            if not finish:
                window.blit(background2, (0, 0))
                ship.update()
                bullets.update()
                monsters2.update()
                text = font2.render('Рахунок:' + str(score), True, (255, 255, 255))
                window.blit(text, (10, 20))
                text_lose = font2.render('Пропущено:' + str(lost), True, (255, 255, 255))
                window.blit(text_lose, (10, 50))

                ship.reset()
                bullets.draw(window)
                monsters2.draw(window)
                collides = sprite.groupcollide(monsters2, bullets, True, True)
                for c in collides:
                    score += 1
                    monster2 = Enemy(img_enemy2, randint(50, win_width - 80), -60, 80, 50, randint(4, 7))
                    monsters2.add(monster2)

                if real_time == True:
                    now_time = timer()
                    if now_time - last_time < 3:
                        reload = font2.render('Wait, reload..', True, (255, 0, 0))
                        window.blit(reload, (260, 460))
                    else:
                        real_time = False
                        num_fire = 0
                if life == 3:
                    life_color = (0, 150, 0)
                if life == 2:
                    life_color = (150, 150, 0)
                if life == 1:
                    life_color = (150, 0, 0)
                text_life = font1.render(str(life), True, life_color)
                window.blit(text_life, (650, 10))
                if sprite.spritecollide(ship, monsters2, False):
                    sprite.spritecollide(ship, monsters2, True)
                    life -= 1
                if life == 0 or lost >= max_lost:
                    finish = True
                    window.blit(lose, (200, 200))

                if score >= goal2:
                    # finish = True
                    window.blit(win, (200, 200))
                    lvl1 = False
                    lvl2 = False

    display.update()
    time.delay(50)


