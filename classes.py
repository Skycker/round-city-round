import pygame
from pygame.locals import *

class Sprite:
    """Класс чего-то, что можно отрисовать"""
    def rander(self, surface):
        #'''Отрисовывает спрайт в собственных координатах'''
        self.pos = self.img.get_rect().move(self.x, self.y)
        surface.blit(self.img, self.pos)

# Описание персонажей
class Citizen(Sprite):
    """Класс описывающий горожан"""
    def __init__(self, start_vert, step=0.06):
        # граф для движения Citizens
        self.Verts = [[900,233], [602,233],  # вершина 0,1
                    [602,328], [670,493],   # вершина 2,3
                    [697,360], [626, 460],  # вершина 4,5 
                    [615,541], [576,493],   # вершина 6,7
                    [537,478], [528,408],   # вершина 8,9
                    [590,577], [477,518],   # вершина 10,11
                    [477,342], [347,239],   # вершина 12,13
                    [347,41], [-153,41],    # вершина 14,15
                    [-153,274], [-153,525], # вершина 16,17
                    [340,525], [245,238],   # вершина 18,19   
                    [245,173], [162,173],   # вершина 20,21
                    [67, 173], [97, 219],   # вершина 22,23
                    [140,265], [126,335],   # вершина 24,25
                    [46, 240], [40, 332],   # вершина 26,27
                    [189,274], [210,310],   # вершина 28,29
                    [203,378], [143,385],   # вершина 30,31
                    [74,385], [90,200],     # вершина 32,33
                    [600, 344]]             # вершина 34
        # Список смежности графа Citizens
        self.Links = [[1], [2, 13], [3],            # для 0,1,2
                    [4,5,6,7,34], [34], [34,3],     # для 3,4,5
                    [3,10], [8,9], [34],            # для 6,7,8
                    [34], [11], [12],               # для 9,10,11
                    [34], [14,18,19], [15,13],      # для 12,13,14
                    [14,16], [15,17], [16,18],      # для 15,16,17
                    [13, 17], [20,21,22,23,28,13],  # для 18,19
                    [22,24],[21,23,24], [22,24],    # для 20,21,22
                    [20,27,28,25,26], [27], [28],   # для 23,24,25
                    [33], [33], [19,29,30,31],      # для 26,27,28
                    [28,30,31], [29,28,31], [28,30,32], # для 29,30,31
                    [27,26,31,25],[13],[1]]             # для 32,33, 34

        # Шаг, на который будет смещаться объкт
        self.step = step
        # x, y - коодинаты начального положения
        self.x = self.Verts[start_vert][0]    
        self.y = self.Verts[start_vert][1] 
        # аватар экземпляра 
        self.img = pygame.image.load('citizen.png').convert_alpha()
        self.pos = self.img.get_rect().move(self.x, self.y)
        # координаты и вершина назначения
        self.target_x = self.Verts[start_vert][0] 
        self.target_y = self.Verts[start_vert][1]
        self.target_vert = start_vert
        # Индикатор, заплатил ли кружок за что-нить
        self.is_paid_for = False
        self.alert_times = 0   
   
    def is_at_point(self, centre_x, centre_y):
        """Определяет находится ли спрайт в квадрете 1*1 вокруг введенных
        координат
        """
        if (centre_x-0.5<=self.x<=centre_x+0.5 and
            centre_y-0.5<=self.y<=centre_y+0.5): return True
        else: return False

    def make_step(self):
        """Передвигает спрайт на один шаг в строну target_x, target_y"""
        if not self.is_at_point(self.target_x, self.target_y):
                if self.target_x > self.x:
                    self.x += self.step
                else:
                    self.x -= self.step

                if self.target_y > self.y:
                    self.y += self.step
                else:
                    self.y -= self.step


class Neighbour(Citizen):
    """Класс описывающий соседа"""
    def __init__(self, start_vert=0, step=0.5):
        self.Verts = [[442,72], [469,72],      # вершина 0,1
                    [469,233], [602,233],      # вершина 2,3
                    [602,328], [670,493]]      # вершина 4,5
        # аватара
        self.img = pygame.image.load('neighbour.png').convert_alpha()
        # Шаг, на который будет смещаться объкт
        self.step = step
        # x, y - коодинаты начального положения
        self.x = self.Verts[start_vert][0]    
        self.y = self.Verts[start_vert][1]
        self.pos = self.img.get_rect().move(self.x, self.y)
        # координаты и вершина назначения
        self.target_x = self.Verts[start_vert][0] 
        self.target_y = self.Verts[start_vert][1]
        self.target_vert = start_vert 
        # направление движения: за едой(toward) или домой(back) или на месте(stay)
        self.direction = 'stay'
             

class Barman(Citizen):
    """Класс описывающий бармена"""
    def __init__(self, start_vert=0, step=0.06):
        self.Verts = [[900,233], [602,233],     # вершина 0,1
                    [602,328], [681,409],       # вершина 2,3
                    [770,409], [767,482],       # вершина 4,5
                    [734,521]]                  # вершина 6
        # аватара
        self.img = pygame.image.load('barman.png').convert_alpha()
        # Шаг, на который будет смещаться объкт
        self.step = step
        # x, y - коодинаты начального положения
        self.x = self.Verts[start_vert][0]    
        self.y = self.Verts[start_vert][1]
        self.pos = self.img.get_rect().move(self.x, self.y)
        # координаты и вершина назначения
        self.target_x = self.Verts[start_vert][0] 
        self.target_y = self.Verts[start_vert][1]
        self.target_vert = start_vert 
        # направление движения: на работу(toward), с работы(back) или на месте(stay)
        self.direction = 'stay'

    def is_at_workplace(self):
        if self.x >= 704 and self.y >= 456: return True
        else: return False


class FastСitizen(Citizen):
    """Класс описывающий быстрого горожанина"""
    def __init__(self, start_vert, step=0.15):
        Citizen.__init__(self, start_vert, step)
        self.img = pygame.image.load('fast_citizen.png').convert_alpha()


class DangerousCitizen(FastСitizen):
    """Класс описывающий грабителя"""
    pass


class Hero(Citizen):
    """Класс описывающий главного героя"""
    def __init__(self, x, y, step, money=0, pay=30):
        # координаты х,у и шаг
        self.x = x
        self.y = y
        self.step = step
        # аватар протеже
        self.img = pygame.image.load('hero.png').convert_alpha()
        # заработанные деньги
        self.money = money
        # штраф за необслуженного клинта
        self.fines = 0
        # текст оповещения о действиях игрока
        self.alert_text = ''
        self.alert_times = 0
        self.hungry = False
        self.slipless_nights_qou = 0

    def is_at_workplace(self):
        """На рабочем месте ли протеже?"""
        if -30<=self.x<=80 and 177<=self.y<=365: return True 
        else: return False

    def is_near_barman(self):
        """В пиццерии ли протеже?"""
        if self.x >= 625 and self.y >= 390: return True
        else: return False

    def is_at_home(self):
        """Дома ли протеже?"""
        if self.x >= 573 and self.y <= 160: return True
        else: return False


class Button(Sprite):
    """Класс описывающий кнопку"""
    def __init__(self, x, y, text='', color=(0,0,0)):
        self.x = x
        self.y = y
        self.text = text
        self.text_color = color
        
        pygame.sprite.Sprite.__init__(self)
        self.img_sel = pygame.image.load('pressed_button.png').convert_alpha()
        self.img_unsel = pygame.image.load('button.png').convert_alpha()
        self.changeState(0)

    def changeState(self, state):
        """Метод меняет картинку кнопки(нажата/не нажата)"""
        if state == 0:
            self.img = self.img_unsel
        elif state == 1:
            self.img = self.img_sel
        
        self.rect = self.img.get_rect()
        self.rect.center = (self.x,self.y)