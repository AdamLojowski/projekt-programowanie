import pygame
from pygame.locals import *
import os.path
import time
import random
import math
from pygame.sprite import Sprite
import sys
import time
import os

pygame.font.init()

# parametry programu
SCREEN_WIDTH = 806
SCREEN_HEIGHT = 916
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)

font = pygame.font.Font('freesansbold.ttf',32)
font_game_over = pygame.font.Font('freesansbold.ttf',70)

textX = 60
textY = 70
texthpX = 750

# funkcja pomocnicza
def loadImage(name, useColorKey=False):
    """ Załaduj obraz i przekształć go w powierzchnię.

    Funkcja ładuje obraz z pliku i konwertuje jego piksele 
    na format pikseli ekranu. Jeśli flaga useColorKey jest 
    ustawiona na True, kolor znajdujący się w pikselu (0,0)
    obrazu będzie traktowany jako przezroczysty
    """
    fullname = os.path.join("imgs",name)
    image = pygame.image.load(fullname)
    image = image.convert() 
    if useColorKey is True:
        colorkey = image.get_at((0,0)) 
        image.set_colorkey(colorkey,RLEACCEL)

    return image

def loadSound(name):
    """Załaduj dźwięk i spraw, żeby działał."""
    
    fullname = os.path.join("imgs",name)
    sound = pygame.mixer.Sound(fullname)
    return sound

#Klasa obiektów

class MyBird(pygame.sprite.Sprite):
    """Klasa odpowiadająca za głównego bohatera gry """
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("bird.png", True)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH/2+25, SCREEN_HEIGHT/2) #GDZIE WSTAWIĆ 
        self.x_velocity = 0
        self.y_velocity = 0
        self.hp = 3
        self.score = 0
        self.spawn = 0
        
    def update(self):
        """Określ położenie Ptaka, obróć ptaka i usuń odpowiednie kolce, jeśli
        odbije się od boku ekranu"""
        
        self.rect.move_ip((self.x_velocity,self.y_velocity)) #move in-place
        if self.rect.left < -30:
            self.x_velocity = -self.x_velocity
            self.image = pygame.transform.flip(self.image, True, False)
            self.spawn += 1
            self.score += 1
            print(self.score)
            xpFX.play()
        elif self.rect.right > SCREEN_WIDTH+40:
            self.x_velocity = -self.x_velocity
            self.image = pygame.transform.flip(self.image, True, False)
            self.spawn += 1
            self.score +=1
            print(self.score)
            xpFX.play()       

class Spike_right(pygame.sprite.Sprite):
    """Klasa odpowiadająca za prawe kolce"""
    
    def __init__(self, index):
        """Stwórz Sprite'a, załaduj obraz, określ jego wielkość i położenie"""
        
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("spike.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH
        self.rect.centery = index

class Spike_left(pygame.sprite.Sprite):
    """Klasa odpowiadająca za lewe kolce"""
    
    def __init__(self, index):
        """Stwórz Sprite'a, załaduj obraz, określ jego wielkość i położenie"""
        pygame.sprite.Sprite.__init__(self)
        self.image = loadImage("spike.png", True)
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.centerx = 0
        self.rect.centery = index
        
                          
def colision(obj1, sprite_obj):
    """Sprawdź, czy dwie grupy Sprite'ów się zderzyły

    @param1 obj1:Sprite
    @param2 sprite_obj:Sprite
    @return Bool"""
    
    for item in sprite_obj:
            distance = math.sqrt((item.rect.x - obj1.rect.x)**2 + (item.rect.y - obj1.rect.y)**2)
            if distance < 60:
                  return True
    else:
            return False
        
def show_score(x, y):
    """Pokaż ilość zdobytych punktów na ekranie

    @param1 x:int szerokość, na jakiej ma się znajdować
    @param2 y:int długość, na jakiej ma się znajdować"""
    
    score_value = font.render("Score:" + str(mybird.score), True, (0,0,255))
    score_rect = score_value.get_rect()
    score_rect.midtop = (textX, textY)
    screen.blit(score_value,score_rect)

def show_hp(mybird):
    """Pokaż ptasią pulę życia na ekranie

    @param mybird:class MyBird"""

    hp_value = font.render("hp:"+ str(mybird.hp), True, (0,0,255))
    hp_rect = hp_value.get_rect()
    hp_rect.midtop = (texthpX,textY)
    screen.blit(hp_value, hp_rect)

def game_over(x, y):
    """Wyświetl napis końca gry na ekranie

    @param1 x:int szerokość, na jakiej ma się znajdować
    @param2 y:int długość, na jakiej ma się znajdować"""
    
    text_over = font.render("Game over :c", True, (0,0,255))
    over_rect = text_over.get_rect()
    over_rect.midtop = (x, y)
    screen.blit(text_over,over_rect)


pygame.init()    


# właściwy program
screen = pygame.display.set_mode(SCREEN_SIZE) 
pygame.display.set_caption("Don't Touch the spiky things")

#załaduj tło
background_image = loadImage("bkg.png")
screen.blit(background_image,(0,0))

#załaduj muzykę
ouchFX = loadSound("ouch.wav")
xpFX = loadSound("xp.wav")

#załaduj Sprity
mybirdSprite = pygame.sprite.RenderClear()
mybird = MyBird()
mybirdSprite.add(mybird)

spike_rightSprites = pygame.sprite.RenderClear()
spike_leftSprites = pygame.sprite.RenderClear()

def main_menu():
    """Stwórz menu główne gry"""
    global highest
    
    highscore = open('imgs//highscore.txt', 'r') #załaduj najwyższy wynik
    highest = int(highscore.read())
    highscore.close()
    
    click = False
    while True:
        background_image = loadImage("menu_screen.png") #określ tło
        screen.blit(background_image,(0,0))

        mx,my = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(50,100,200,50) #określ pozycje przycisków
        button_2 = pygame.Rect(50,200,200,50)
        button_3 = pygame.Rect(50,300,200,50)
        button_4 = pygame.Rect(50,400,200,50)
        button_5 = pygame.Rect(50,500,200,50)

        if button_1.collidepoint((mx,my)): #poruszanie się po interface
            if click:
                  game(3)
        if button_2.collidepoint((mx,my)):
            if click:
                  game(1)
        if button_3.collidepoint((mx,my)):
            if click:
                  autor()
        if button_4.collidepoint((mx,my)):
            if click:
                  instrukcja()
        if button_5.collidepoint((mx,my)):
            if click:
                  end()
        

        pygame.draw.rect(screen, (255, 0, 0), button_1) #wyświetl przyciski
        pygame.draw.rect(screen, (255, 0, 0), button_2)
        pygame.draw.rect(screen, (255, 0, 0), button_3)
        pygame.draw.rect(screen, (255, 0, 0), button_4)
        pygame.draw.rect(screen, (255, 0, 0), button_5)
        
        buttons_name()      
        
        click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    
        pygame.display.update()


def buttons_name():
        """Wyświetl napisy na przyciskach """
        
        start = font.render("Classic", True, (255,255,255))
        start_rect = start.get_rect()
        start_rect.midtop = (150, 110)
        screen.blit(start,start_rect)

        hard = font.render("One shot", True, (255,255,255))
        hard_rect = hard.get_rect()
        hard_rect.midtop = (150, 210)
        screen.blit(hard,hard_rect)
        
        about_me = font.render("About me", True, (255,255,255))
        about_me_rect = about_me.get_rect()
        about_me_rect.midtop = (150, 310)
        screen.blit(about_me,about_me_rect)

        how = font.render("How to", True, (255,255,255))
        how_rect = how.get_rect()
        how_rect.midtop = (150, 410)
        screen.blit(how,how_rect)

        end = font.render("End", True, (255,255,255))
        end_rect = end.get_rect()
        end_rect.midtop = (150, 510)
        screen.blit(end,end_rect)

        high = font.render("Highest score: "+str(highest), True, (0,0,0))
        high_rect = high.get_rect()
        high_rect.midtop = (520, 110)
        screen.blit(high,high_rect)


def game(life):
    """Wyświetl grę
    @param1 life:int oznacza ilość żyć, którą posiada Ptak"""
    
    pygame.init()    


    # właściwy program
    screen = pygame.display.set_mode(SCREEN_SIZE) 
    pygame.display.set_caption("Don't Touch the spiky things")

    #załaduj tło
    background_image = loadImage("bkg.png")
    screen.blit(background_image,(0,0))

    ouchFX = loadSound("ouch.wav")
    xpFX = loadSound("xp.wav")

    #załaduj ptaka
    mybirdSprite = pygame.sprite.RenderClear()
    mybird = MyBird()
    mybirdSprite.add(mybird)

    mybird.hp = life

    spike_rightSprites = pygame.sprite.RenderClear()
    spike_leftSprites = pygame.sprite.RenderClear()


    clock = pygame.time.Clock()
    running = True
    n = 1
    jump = True
    gravity = False
    running = True
    gravity_val = 5 #domyślna wartość grawitacji
    
    while running:
        clock.tick(40)
        background_image = loadImage("bkg.png") #załaduj tło
        screen.blit(background_image,(0,0))
        for event in pygame.event.get(): #operuj przyciskami
            if event.type == pygame.QUIT:
                running = False
            elif event.type == KEYDOWN:
                if n == 1:
                    mybird.x_velocity = -10
                    n += 1

                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    gravity = False
                    if jump:
                        mybird.y_velocity = -22 #siła skoku
                        gravity = 0
            elif event.type == KEYUP:
                if event.key == K_SPACE:
                    gravity = True
                    mybird.y_velocity = gravity_val

        if gravity:
            mybird.y_velocity += 0.15 #zwiększaj przyspieszenie w dół, gdy Ptak nie lata

        if mybird.rect.top < 65: #tylko dolna połowa ekranu
                mybird.hp -=1
                mybird.rect.center = (SCREEN_WIDTH/2+25, SCREEN_HEIGHT/2)
                print("Ouch")
                ouchFX.play()
        elif mybird.rect.bottom >= SCREEN_HEIGHT-50:
                mybird.hp -=1
                mybird.rect.center = (SCREEN_WIDTH/2+25, SCREEN_HEIGHT/2)
                print("Ouch")
                ouchFX.play()
           
        if colision(mybird,spike_rightSprites) or colision(mybird, spike_leftSprites):
                mybird.hp -= 1
                print("Ouch")
                mybird.rect.center = (SCREEN_WIDTH/2+25, SCREEN_HEIGHT/2)
                ouchFX.play()

        if mybird.hp <= 0: #Koniec gry i powrót do menu
            running = False
            print("Game Over")
            game_over(425, 425)
            pygame.display.flip()
            if mybird.score > highest: #zapisz najwyższy wynik
                save_score = open('imgs//highscore.txt', 'w')
                save_score.writelines(str(mybird.score))
                save_score.close()
            
            time.sleep(3)
            main_menu()
                
        score_value = font.render("Score:" + str(mybird.score), True, (0,0,255)) #wyświetl aktualny wynik
        score_rect = score_value.get_rect()
        score_rect.midtop = (600, textY)
        screen.blit(score_value,score_rect)                                  
        mybirdSprite.update()
        
        if mybird.spawn > 0 and mybird.rect.left > 0: #stwórz kolce po prawej stronie
             mybird.spawn = 0
             for i in range(random.randint(1,8)):
                   spike_leftSprites.add(Spike_left(random.randint(1,8)*100))
                   
        elif mybird.spawn > 0 and mybird.rect.right < SCREEN_WIDTH: #stwórz kolce po lewej stronie
              mybird.spawn = 0
              for i in range(random.randint(1,8)):
                    spike_rightSprites.add(Spike_right(random.randint(1,8)*100))


        if mybird.rect.left < -30: #usuń kolce po lewej
              for item in spike_leftSprites:
                    spike_leftSprites.remove(item)
        elif mybird.rect.right > SCREEN_WIDTH+40: #usuń kolce po prawej
              for item in spike_rightSprites:
                    spike_rightSprites.remove(item)


        if mybird.score == 11:   #zwiększaj szybkość ptaka, gdy zdobywasz punkty, przywróć życie
              mybird.x_velocity = 12
        elif mybird.score == 21:
              mybird.x_velocity = 14
        elif mybird.score == 31:
              mybird.hp = life
              mybird.x_velocity = 16
        elif mybird.score == 51:
              mybird.hp = life
              mybird.x_velocity = 18
        elif mybird.score == 71:
              mybird.hp = life
              mybird.x_velocity = 20
        elif mybird.score == 101:
              mybird.hp = life
              mybird.x_velocity = 22

        mybirdSprite.clear(screen, background_image)  #clearuj Sprite'y
        spike_rightSprites.clear(screen, background_image)
        spike_leftSprites.clear(screen, background_image)


        spike_rightSprites.draw(screen) #rysuj Sprite'y
        spike_leftSprites.draw(screen)
        show_hp(mybird)
        
        mybirdSprite.draw(screen) #pokaż zaktualizowaną klatkę
        pygame.display.flip()

def autor():
    """Wyświetl informacje o autorze """
    running = True
    while running:
        background_image = loadImage("autor.png")
        screen.blit(background_image,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            

        pygame.display.update()

def instrukcja():
    """Wyświetl instrukcję do gry"""
    
    running = True
    while running:
        background_image = loadImage("instrukcja.png")
        screen.blit(background_image,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()    

def end():
    """zakończ"""
    sys.exit()

main_menu()


