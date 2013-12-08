import sys
import os
import random

import pygame
from pygame.locals import *
import inputbox
from prices import Price_dict, Price_list
from classes import *

# Размер игрового экрана
W_WIDTH = 800
W_HEIGH = 600
# Палитра цветов)
green = (0, 128, 0)     # green
teal = (0, 128, 128)    # teal
white = (255,255,255)   # white 
black = (0,0,0)         # black
# Максимальное количество денег
MAX_MONEY = 99999
# Позиции вывода текстов на экран
MONEY_TEXT_POS = (660, 40)
TIME_TEXT_POS = (695, 13)
ALERT_POS = (625, 3)
FINAL_TEXT_POS = (40, 30)

WIN_TEXT = 'Поздравляю! Вы скопили нужную сумму, кружок выкупил салон связи и устроил свою жизнь'
LOSE_TEXT = 'Вы проиграли, кружка уволили, вся его жизнь пошла под откос. Вы подвели кружка'

# Внутреннее время быстрее реального в 60*TIME_RAPID раз.
# сразу задаем начальное значение.
# minute_step_able разрешает инкрементацию часов, ибо без него,
# часы могли инкриментнуться более раза вместо одного
TIME_RAPID = 2
START_MINUTES = 00
START_HOURS = 10
minute_inc_counter = 0
minute_step_able = True
minutes = START_MINUTES
hours = START_HOURS
# Время отображения уведомления(в итерациях)
ALERT_TIME = 500
# Вершины, где ночью горожан быть не должно
NIGHT_TABOO_PLACES = [2,3,4,5,6,7,8,9,10,11,12,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34]

# Константы для игрока
player_name = ''    # имя
FINE = 500          # штраф за отсутствие на рабочем месте
MAX_FINES_QUO = 15  # максимальное кол-во штрафоф до game_over
MEAL_PRICE = 50     # цена покупки еды у бармена

pygame.init()
screen = pygame.display.set_mode((W_WIDTH, W_HEIGH))

# Загружаем фоновые рисуноки
background = pygame.image.load('background.png').convert()
start_background = pygame.image.load('start_background.png').convert()
end_background = pygame.image.load('half_life_3_hope.png').convert()
night_cover = pygame.image.load('night_cover.png').convert_alpha()

# Вводим саундтреки и их обработку
directory = os.getcwd() + '/soundtracks'
files_list = os.listdir(directory)
songs_list = []
for file_name in files_list:
    if file_name.endswith('.mp3'):
        songs_list.append('soundtracks/' + file_name)

# создаем пользовательское событие SONG_END.
# оно нам отсигналит, если какой-то трек отыграет
SONG_END = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(SONG_END)

# Ф-я выбора соундтрека
def start_next_song():
    if songs_list:
        next_song = random.choice(songs_list) # случайно выбираем трек...
        print(next_song)
        pygame.mixer.music.load(next_song)    # ...и подгружаем его
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play()

# Ф-я для вывода текста
def set_text(surface, text='', size=50, text_pos=(0,0), alias=True, color=black):
    font = pygame.font.Font(None, size)
    text_obj = font.render(text, alias, color)
    surface.blit(text_obj, text_pos)

# Ф-я вывода сообщений игроку
def alert(text, color=black):
    x = W_WIDTH - len(text)*8 - 5
    y = ALERT_POS[1]
    pos = [x, y]
    set_text(screen, text, 20, pos)

# Определяет ночь ли в игре
def is_night():
    if 22<=hours or 0<=hours<6: return True
    else: return False

def is_working_day():
    if 8 <= hours < 22: return True
    else: return False

def unless_player_press_smth():
    """Ф-я "ставит игру на паузу" до нажатия кнопки игроком. Обрабатывает эти нажатия"""
    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                # Полноэкранный режим или оконный?
                if event.key == K_f:
                    pygame.display.set_mode((W_WIDTH, W_HEIGH), pygame.FULLSCREEN)
                    screen.blit(start_background, (0, 0))
            if event.type == MOUSEMOTION:
                for btn in buttons:
                    if btn.rect.collidepoint(pygame.mouse.get_pos()):
                        btn.changeState(1)
                    else:
                        btn.changeState(0)
            elif event.type == MOUSEBUTTONDOWN:
                if new_game:
                    if btn_start_game.rect.collidepoint(pygame.mouse.get_pos()):
                        global player_name
                        player_name = inputbox.ask(screen, "Your name?")
                        return
                if btn_exit.rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                if not new_game:
                    if btn_finish_game.rect.collidepoint(pygame.mouse.get_pos()):
                        return 
                
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        for btn in buttons:
            btn.rander(screen)
            set_text(screen, btn.text, 20, (btn.x+27, btn.y+7), 1, btn.text_color )
        pygame.display.flip()

while True:
    # Начинаем игру...
    new_game = True
    pygame.display.set_caption('Игра')
    screen.blit(start_background, (0, 0))
    # кнопки меню
    btn_start_game = Button(W_WIDTH/2 - 30,W_HEIGH/2 - 60, "Старт")
    btn_exit = Button(W_WIDTH/2 - 30,W_HEIGH/2, "Выход")
    buttons = [btn_start_game, btn_exit]

    start_next_song()       
    unless_player_press_smth()
    pygame.display.set_caption('Играет ' + player_name)

    minutes = START_MINUTES
    hours = START_HOURS
                
    # Инициируем игровой объект
    hero = Hero(18, 270, 0.25)
    # Инициируем жителей городка
    # (cтартовая позиция определяется рандомно из вершин соответствующего графа)
    person1 = Citizen(random.randint(0,34), 0.1)
    person2 = Citizen(random.randint(0,34), 0.1)
    person3 = Citizen(random.randint(0,34), 0.1)
    person4 = Citizen(random.randint(0,34), 0.1)
    person5 = Citizen(random.randint(0,34), 0.1)
    person6 = FastСitizen(random.randint(0,34), 0.15)
    person7 = FastСitizen(random.randint(0,34), 0.15)
    citizens = [person1, person2, person3, person4, person5, person6, person7]

    neighbour = Neighbour()
    # создаем бармена, стартовая позиция определяется от времени
    if is_working_day():
        barman = Barman(6)  # на работе
    else:
        barman = Barman(0)  # дома
        
    pygame.mouse.set_visible(False)
    hungry_time = [random.randint(0,24) for x in range(random.randint(3,5))]
    # Цикл приема сообщений
    while True:
        screen.blit(background, (0, 0)) # чтобы спрайты не накладывались

        # Если ночь, затемняем экран
        if is_night():
            screen.blit(night_cover, (0,0))

        for event in pygame.event.get(): 
            if event.type == QUIT: # обрабатываем событие шечка по крестику
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                # Полноэкранный режим или оконный?
                if event.key == K_f:
                    pygame.display.set_mode((W_WIDTH, W_HEIGH), pygame.FULLSCREEN)
                    screen.blit(background, (0, 0))
                elif event.key == K_ESCAPE:
                    pygame.display.set_mode((W_WIDTH, W_HEIGH))
                    screen.blit(background, (0, 0))
                if (event.key == K_e and hero.is_near_barman() 
                    and barman.is_at_workplace() ):
                    hero.hungry = False
                    hero.money -= MEAL_PRICE
                    hero.alert_text = 'Вы купили поесть'
                    hero.alert_times = ALERT_TIME
            # Если соундтрек закончился, вызываем start_next_song()
            if event.type == SONG_END:
                start_next_song()
        
        # Передвижение протеже        
        keys = pygame.key.get_pressed()
        if keys[K_LEFT]:
            hero.x -= hero.step
        if keys[K_RIGHT]:
            hero.x += hero.step
        if keys[K_UP]:
            hero.y -= hero.step
        if keys[K_DOWN]:
            hero.y += hero.step

        #set_text(screen, str(hero.x) + '|' + str(hero.y))   

        # Оповещения о действиях протеже
        if hero.alert_text:
            alert(hero.alert_text)
            hero.alert_times -= 1
        if hero.alert_times == 0: hero.alert_text = ''

        # Голод протеже
        if hours == 0 and minutes == 0:
            hungry_time = [random.randint(0,24) for x in range(random.randint(3,5))]
        if hours in hungry_time and minutes == 00:
            hero.hungry = True
        if hero.hungry:
            hero.alert_text = 'Вы голодны. Поешьте в кафе'

        if hero.fines >= MAX_FINES_QUO - 3:
            hero.alert_text = ('Еще ' + str(MAX_FINES_QUO - hero.fines) +
                                ' штраф и вас уволят')
        if hero.is_near_barman() and barman.is_at_workplace():
            if not hero.alert_times:
                hero.alert_text = 'Нажмите E, что бы поесть'
                hero.alert_times = int(ALERT_TIME/5)

        # Движение persons(синие и оранжевые кружки)
        for person in citizens:
            if person.is_at_point(person.target_x, person.target_y):
                if not is_working_day():
                    while True:
                        person.target_vert = random.choice(person.Links[person.target_vert])
                        if person.target_vert in NIGHT_TABOO_PLACES: continue
                        else: break
                else:
                    person.target_vert = random.choice(person.Links[person.target_vert]) 
                
                person.target_x = person.Verts[person.target_vert][0]
                person.target_y = person.Verts[person.target_vert][1]

            person.make_step()

        # Горожане у рабочего места кружка в салоне
        for person in citizens:
            if (person.is_at_point(person.Verts[26][0], person.Verts[26][1]) or
             person.is_at_point(person.Verts[27][0], person.Verts[27][1])):
                if hero.is_at_workplace():
                        if not person.is_paid_for:
                            key = random.choice(Price_list)
                            hero.money += Price_dict[key]
                            person.is_paid_for = True
                            person.alert_times = ALERT_TIME
                        if hero.money > MAX_MONEY:
                            hero.money = MAX_MONEY
                else:
                        hero.alert_text = 'Не было на месте. Штраф!'
                        hero.alert_times = ALERT_TIME
                        hero.money -= FINE
                        hero.fines += 1
                        if hero.money < -MAX_MONEY:
                            hero.money = -MAX_MONEY 
            # Отображение уведомлений от горожан
            if person.is_paid_for:
                if not hero.alert_text: # затычка, что бы выводы текста не накладывались
                    alert(key)      # нужно бы переписать всю систему вывода алертов
                person.alert_times -= 1
            if person.alert_times == 0: person.is_paid_for = False

        # Условия окончания игры
        if hero.money == MAX_MONEY:
            win = True
            break
        if hero.fines == MAX_FINES_QUO:
            win = False
            break

        # Жизненный цикл соседа(neighbour)
        if (hours == 12 or hours == 18) and minutes == 0:
            neighbour.direction = 'toward'
        if neighbour.is_at_point(neighbour.Verts[5][0], neighbour.Verts[5][1]):
            neighbour.direction = 'back'
        if (neighbour.is_at_point(neighbour.Verts[0][0], neighbour.Verts[0][1]) and
                neighbour.direction == 'back'):
            neighbour.direction = 'stay'
            neighbour.target_vert = 0

        if neighbour.direction != 'stay':
            if neighbour.is_at_point(neighbour.target_x, neighbour.target_y):
                    if neighbour.direction == 'toward':
                        neighbour.target_vert += 1
                    else: 
                        neighbour.target_vert -= 1
                    neighbour.target_x = neighbour.Verts[neighbour.target_vert][0]
                    neighbour.target_y = neighbour.Verts[neighbour.target_vert][1]
            
            neighbour.make_step()

        # Жизненный цикл бармена(barman)
        if hours == 8 and minutes == 0:
            barman.direction = 'toward'
            barman.target_vert = 0
        if hours == 22 and minutes == 0:
            barman.direction = 'back'
            barman.target_vert = 6
        if (barman.is_at_point(barman.Verts[6][0], barman.Verts[6][1]) and 
                                barman.direction == 'toward'):
            barman.direction = 'stay'
        if (barman.is_at_point(barman.Verts[0][0], barman.Verts[0][1]) and 
                                barman.direction == 'back'):
            barman.direction = 'stay'

        if barman.direction != 'stay':
            if barman.is_at_point(barman.target_x, barman.target_y):
                    if barman.direction == 'toward':
                        barman.target_vert += 1
                    else: 
                        barman.target_vert -= 1
                    barman.target_x = barman.Verts[barman.target_vert][0]
                    barman.target_y = barman.Verts[barman.target_vert][1]
            
            barman.make_step()

        # Подсчет внутреигрового времени
        minutes = (START_MINUTES + (TIME_RAPID*pygame.time.get_ticks()//1000)%60 - 
                    minute_inc_counter*START_MINUTES)
        if minutes == 59:
            if minute_step_able:
                hours += 1
            minute_step_able = False
            minute_inc_counter += 1
        if hours == 24:
            hours = 0 
        if minutes == 1:
           minute_step_able = True
        
        # Вывод денег и времени на экран
        # собираем строку для красивого вывода денег
        money_string = ('$' + '0'*(len(str(MAX_MONEY))-len(str(abs(hero.money))))
                        + str(abs(hero.money)))
        if hero.money < 0: money_string = '-' + money_string
        set_text(screen, money_string, 50, MONEY_TEXT_POS, True, green)
        
        # собираем строку для красивого вывода времени
        if not hours//10: time_string = '0' + str(hours)
        else: time_string = str(hours)
        time_string += ':'
        if not minutes//10:
            time_string += '0' + str(minutes)
        else: time_string += str(minutes)
        set_text(screen, time_string, 50, TIME_TEXT_POS, True, teal)

        # Отрисовываем спрайты в буфер    
        hero.rander(screen)
        for person in citizens:
            person.rander(screen)
        neighbour.rander(screen)
        barman.rander(screen)
        # Отображаем буфер на экран
        pygame.display.flip()

    new_game = False
    screen.blit(end_background, (0, 0))

    if win:
        final_text = WIN_TEXT
        size = 23
    else:
       final_text = LOSE_TEXT
       size = 25
       
    set_text(screen, final_text, size, FINAL_TEXT_POS, True, white) 
    btn_finish_game = Button(W_WIDTH/2 - 30,W_HEIGH/2 - 60, "Жду...")
    buttons = [btn_finish_game, btn_exit]
    pygame.mouse.set_visible(True)
    unless_player_press_smth()
