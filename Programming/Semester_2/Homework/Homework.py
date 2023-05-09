import pygame
from abc import ABC, abstractmethod
from threading import  Thread
import time
import sqlite3

# Для обновления БД смотри Примечание 1

# Слздание массива для дальнейшего добавления в БД
mass = [("P", 1, x, "White") for x in range(0, 8)] + [("P", 6, x, "Black") for x in range(0, 8)]
mass += [("L", 0, 0, "White"), ("L", 0, 7, "White"), ("L", 7, 0, "Black"), ("L", 7, 7, "Black")]
mass += [("Kn", 0, 1, "White"), ("Kn", 0, 6, "White"), ("Kn", 7, 1, "Black"), ("Kn", 7, 6, "Black")]
mass += [("E", 0, 2, "White"), ("E", 0, 5, "White"), ("E", 7, 2, "Black"), ("E", 7, 5, "Black")]
mass += [("F", 0, 3, "White"), ("K", 0, 4, "White"), ("F", 7, 3, "Black"), ("K", 7, 4, "Black")]


try:
    connection = sqlite3.connect("positions.db") # Подклучение к БД
    cursor = connection.cursor() # курсор для выполнения запросов

    cursor.execute("""CREATE TABLE Pos (
                                    id INTEGER PRIMARY KEY,
                                    Fig text NOT NULL,
                                    x INTEGER NOT NULL,
                                    y INTEGER NOT NULL,
                                    color text NOT NULL);""")

    cursor.executemany("INSERT INTO Pos VALUES(NULL, ?, ?, ?, ?)", mass)
    cursor.close()

except sqlite3.Error as error:
    # print("Ошибка при подключении к sqlite: ", error)
    # cursor.execute("""DROP TABLE Pos;""")
    # --------------//Примечание 1//----------------
    # Чтоб обновить данные нужно раскомментировать строку cursor.execute("""DROP TABLE Pos;""") и запустить этот файл, дальше закомментировать её и запустить файл снова. БД обновится

    pass

finally:
    if (connection):
        connection.commit()
        connection.close()

class StandartPosition:

    def __init__(self):
        result = []
        try:
            connection = sqlite3.connect("positions.db")  # Подклучение к БД
            cursor = connection.cursor()  # курсор для выполнения запросов
            cursor.execute("""SELECT * from Pos""")
            mass_position = cursor.fetchall()
            cursor.close()

        except sqlite3.Error as error:
            print("Ошибка при подключении к sqlite: ", error)

        finally:
            if (connection):
                connection.commit()
                connection.close()
        for i in mass_position:
            if i[1] == "P":
                result.append(Peshka(i[2], i[3], i[4]))
            elif i[1] == "L":
                result.append(Ladia(i[2], i[3], i[4]))
            elif i[1] == "F":
                result.append(Ferz(i[2], i[3], i[4]))
            elif i[1] == "K":
                result.append(King(i[2], i[3], i[4]))
            elif i[1] == "Kn":
                result.append(Knight(i[2], i[3], i[4]))
            elif i[1] == "E":
                result.append(Eleph(i[2], i[3], i[4]))


        self.mass_position = result


class ChessDeskError(Exception):

    def __init__(self, text):

        self.txt = text

class Figurs(ABC):  # Класс всех фигур на доске

    def __init__(self, x, y, color):
        self._color = color  # Цвет фигуры (белый или чёрный)
        self._start_position = (x, y)  # Стартовая позиция фигуры
        self._x = x
        self._y = y
        self._attacked = False  # Обозначение, атакована ли фигура
        self._moves = []  # Все возможные ходы фигуры
        self._chosen = False

    def __add__(self, other): # Перегрузка для Ферзя
        return self._moves + other._moves

    @abstractmethod # Задача абстрактного метод
    def can_move(self, mass):  # Метод для нахождения вариантов хода
        for i in desk._figurs:  # приравнивание всех атрибутов выбора на False
            i._chosen = False
        mass._remover(self)  # метод удаляющий невозможные ходы
        self._moves = mass._move  # обновление атрибута фигуры
        desk._all_moves = mass._move  # добавление в атрибут доски все видимые пути
        self._chosen = True
        desk._upload()

    def move_to(self, x, y):
        # Часть кода для вызова из файла Test.py (Сейчас не нужна)
        # y_dict = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7}
        # x = x - 1
        # y = y_dict[y]
        # ________________________________________________________________
        if (x, y) in desk._all_moves:
            self._start_position = (x, y)
            self._x = x
            self._y = y
        else:
            try:
                raise ChessDeskError("Нельзя выполнить это действие!")
            except ChessDeskError as ChD:
                print(ChD)

        desk._all_moves = []
        new_mass = desk._figurs[::]
        for i in desk._figurs:
            if i._attacked and self._start_position == i._start_position:
                if i._name == "K": # Проверка на съедение короля (Окончание игры)
                    if i._color == "White":
                        desk._Winner = "Black"
                    else:
                        desk._Winner = "White"
                new_mass.remove(i)
            else:
                i._attacked = False
        desk._figurs = new_mass[::]
        desk._upload()

    @abstractmethod
    def get_name(self, name):
        def decorator1(funk):
            def wrapped(dec):
                return "У выбранной фигуры название: " + funk(dec) + "\n"
            return wrapped

        def decotator2(funk):
            def wrapper(dec):
                return "И позиция: " + funk(dec)
            return wrapper
        y_de_dict = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
        @decorator1
        def function_1(a):
            return (a)

        @decotator2
        def function_2(a):
            return (str(a[0]) + " " + str(a[1]))

        print(function_1(name), function_2((self._x + 1, y_de_dict[self._y])))

class _Desk:  # класс шахматной доски

    def __init__(self, figurs):
        self._dicter = {}  # словарь с ключами: стартовыми позициями, значениями: фигурами
        self._figurs = figurs  # все фигуры на доске
        self._all_moves = []  # все возможные ходы выбранной фигуры
        position_in_desk = []
        for i in self._figurs:  # позиции всех фигур на доске
            self._dicter[i._start_position] = i
            position_in_desk.append(i._start_position)
        self._position_in_desk = position_in_desk  # создание атрибута с таким массивом
        self._Winner = ""

    def create_table(self, figurs): # Метод для добавления фигур на доску в другом файле
        self._dicter = {}  # словарь с ключами: стартовыми позициями, значениями: фигурами
        self._figurs = figurs  # все фигуры на доске
        self._all_moves = []  # все возможные ходы выбранной фигуры
        position_in_desk = []
        for i in self._figurs:  # позиции всех фигур на доске
            self._dicter[i._start_position] = i
            position_in_desk.append(i._start_position)
        self._position_in_desk = position_in_desk  # создание атрибута с таким массивом

    def _upload(self):
        self._dicter = {}
        position_in_desk = []
        for i in self._figurs:  # переопределение позиций фигур
            self._dicter[i._start_position] = i
            position_in_desk.append(i._start_position)
        self._position_in_desk = position_in_desk

    def draw_desk(self):  # отрисовка доски
        current_figur_coor = "White" # Переменная, кооторая показывает, какого цвета фигуры ходят

        # стандартный вызов окна pygame

        pixels = 60

        WIDHT = 200 + 8 * pixels
        HEIGHT = 200 + 8 * pixels
        FPS = 30

        pygame.init()
        screen = pygame.display.set_mode((WIDHT, HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()

        # работа с шрифтом и текстом

        f1 = pygame.font.Font(None, 90)
        f2 = pygame.font.Font(None, 60)
        text1 = f1.render('A B C D E F G H', True, (0, 0, 0))

        running = 1
        # запуск программы

        while running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = 0
                if event.type == pygame.MOUSEBUTTONDOWN and self._Winner == "": # Проверка на нажатие фигуры
                    stoped = False
                    for i in self._figurs: # Проход по всем фигурам на доске
                        if i._color == current_figur_coor: # Проверяет, чтоб фигура по цвету соответствовала ходу
                            if i._start_position[0] == (event.pos[1] - 100)//60 and i._start_position[1] == (event.pos[0] - 100)//60: # Если нажатие произошло на фигуру (Подсчёт координат)
                                if self._all_moves == i._moves and self._all_moves != []: # При повторном нажатии выводится информация о фигуре
                                    i.get_name()
                                i.can_move()
                            if self._all_moves == i._moves: # Находится фигура, которая сейчас выбрана
                                for j in set(i._moves): # Проходимся по всем ходам фигуры
                                    if j[0] == (event.pos[1] - 100)//60 and j[1] == (event.pos[0] - 100)//60: # Если было нажатие на ход выбранной фигуры, то фигура перемещается
                                        i.move_to(j[0], j[1])
                                        time.sleep(0.1)
                                        if current_figur_coor == "White":
                                            current_figur_coor = "Black"
                                        else:
                                            current_figur_coor = "White"
                                        stoped = True # переменная, которая остановит перебор по фигурам (Так как могут случайно захватиться съеденные фигуры)
                                        break
                        if stoped:
                            break

            screen.fill((200, 200, 200))
            for i in range(0, 8):  # проход по всем клеткам доски и их отрисовка в зависимости от параметров
                for j in range(0, 8):
                    if (i, j) in self._dicter.keys():  # на этой клетке стоит фигура
                        color_fig = self._dicter[(i, j)]._color
                        if self._dicter[(i, j)]._attacked:
                            color_fig = "Red"
                        sym = self._dicter[(i, j)]._name
                        if color_fig == "Black" or color_fig == "Red":
                            color_sym = "White"
                        else:
                            color_sym = "Black"
                        pygame.draw.rect(screen, color_fig, (100 + j * pixels, 100 + i * pixels, pixels, pixels))
                        if sym != "Kn":  # отрисовка названия фигуры
                            screen.blit(f2.render(sym, True, color_sym), (115 + j * pixels, 110 + i * pixels))
                        else:
                            screen.blit(f2.render(sym, True, color_sym), (100 + j * pixels, 110 + i * pixels))
                    elif (i, j) in self._all_moves:  # при вызове метода can_move фигура берётся в руку ==> показываются все ходы фигуры
                        pygame.draw.rect(screen, (255, 230, 0), (100 + j * pixels, 100 + i * pixels, pixels, pixels))
                    elif (i + j) % 2 == 0:
                        pygame.draw.rect(screen, (156, 156, 156), (100 + j * pixels, 100 + i * pixels, pixels, pixels))
                    else:
                        pygame.draw.rect(screen, (163, 116, 73), (100 + j * pixels, 100 + i * pixels, pixels, pixels))
                    # линиии на доске
                    pygame.draw.rect(screen, (128, 128, 128), (100 + j * pixels, i * pixels, 2, HEIGHT))
                    pygame.draw.rect(screen, (128, 128, 128), (j * pixels, 100 + i * pixels, WIDHT, 2))
            pygame.draw.rect(screen, (128, 128, 128), (0 * pixels, 100 + 8 * pixels, WIDHT, 2))
            pygame.draw.rect(screen, (128, 128, 128), (100 + 8 * pixels, 0 * pixels, 2, HEIGHT))
            # прикрепление текста
            screen.blit(text1, (110, 600))
            for i in "12345678":
                text2 = f1.render(i, True, (0, 0, 0))
                screen.blit(text2, (30, 60 * int(i) + 40))
            # Отрисовка оповещения о победе
            if self._Winner == "White":
                pygame.draw.rect(screen, (128, 128, 128), (90, 180, 550, 100))
                winner_text = f1.render("Белые победили!", True, (93, 20, 122))
                screen.blit(winner_text, (100, 200))
            if self._Winner == "Black":
                pygame.draw.rect(screen, (128, 128, 128), (70, 180, 590, 100))
                winner_text = f1.render("Чёрные победили!", True, (93, 20, 122))
                screen.blit(winner_text, (80, 200))
                
            pygame.display.flip()


        pygame.quit()

class Positions(_Desk):  # дочерний класс позиций на доске

    def __init__(self, move):
        super(Positions, self).__init__(desk._figurs)
        self._move = move  # создание атрибута со всеми путями для определённой фигуры

    def _remover(self, current_fig):  # метод удаления всех невозможных ходов
        new_move = []
        for i in self._move:
            if i[0] >= 0 and i[1] >= 0 and i[0] <= 7 and i[1] <= 7: # and not (i in self._position_in_desk):
                for fig in self._figurs: # Нахождение фигуры, которая может быть атакована
                    if fig._start_position == i and fig._color != current_fig._color: # проверка на правильную позицию и цвет фигуры
                        fig._attacked = True
                new_move.append(i)
        self._move = new_move

class King(Figurs):  # король

    def __init__(self, x, y, color):
        super(King, self).__init__(x, y, color)
        self._name = "K"

    def can_move(self):  # метод нахождения всех возможных ходов фигуры
        mass = Positions([(self._x + i, self._y + j) for i in range(-1, 2) for j in range(-1, 2) if i != 0 or j != 0])
        super(King, self).can_move(mass)  # возвращение в метод родительского класса

    def get_name(self):
        super(King, self).get_name(self._name)

        # у остальных фигур аналогичный код отвечает за то же

class Peshka(Figurs):

    def __init__(self, x, y, color):
        super(Peshka, self).__init__(x, y, color)
        self._name = "P"

    def can_move(self):
        if self._color == "White":  # по цыету разные стороны
            mass = Positions([(self._x + 1, self._y)])
        else:
            mass = Positions([(self._x - 1, self._y)])
        super(Peshka, self).can_move(mass)

    def get_name(self):
        super(Peshka, self).get_name(self._name)


class Knight(Figurs):

    def __init__(self, x, y, color):
        super(Knight, self).__init__(x, y, color)
        self._name = "Kn"

    def can_move(self):
        mass = Positions(
            [(self._x + i, self._y + j) for i in range(-2, 3) for j in range(-2, 3) if abs(i) + abs(j) == 3])
        super(Knight, self).can_move(mass)

    def get_name(self):
        super(Knight, self).get_name(self._name)


class Eleph(Figurs):

    def __init__(self, x, y, color):
        super(Eleph, self).__init__(x, y, color)
        self._name = "E"

    def can_move(self):
        # удаляет все возможные перепрыгивания через фигуры
        pit = desk._position_in_desk  # все фигуры на доске
        # def find_other_color(x, y): # Поиск позиций, где фигура может съесть другую
        #     for i in desk._figurs:
        #         if (x, y) == i._start_position and i._color != self._color:
        #             return [(x, y)]
        #     return []
        res1 = []
        res2 = []
        x, y = self._x, self._y
        # прохождение по диагонали и удаление всех перепрыгивний
        for i in range(-7, 8):
            if 0 <= x + i <= 7 and 0 <= y + i <= 7 and i != 0:
                res1.append((x + i, y + i))
                if i < 0 and (x + i, y + i) in pit:
                    # res1 = find_other_color(x + i, y + i) # Добавление позиций, когда фигцра может съесть другую
                    res1 = [(x + i, y + i)]
                if i > 0 and (x + i, y + i) in pit:
                    # res1 += find_other_color(x + i, y + i) # Добавление позиций, когда фигцра может съесть другую
                    res1.append((x + i, y + i))
                    break
        # прохождение по другой диагонали и удаление всех перепрыгивний
        for i in range(-7, 8):
            if 0 <= x + i <= 7 and 0 <= y - i <= 7 and i != 0:
                res2.append((x + i, y - i))
                if i < 0 and (x + i, y - i) in pit:
                    # res2 = find_other_color(x + i, y - i)
                    res2 = [(x + i, y - i)]
                if i > 0 and (x + i, y - i) in pit:
                    res2.append((x + i, y - i))
                    break
        mass = Positions(res1 + res2)
        super(Eleph, self).can_move(mass)

    def get_name(self):
        super(Eleph, self).get_name(self._name)


class Ladia(Figurs):

    def __init__(self, x, y, color):
        super(Ladia, self).__init__(x, y, color)
        self._name = "L"

    def can_move(self):
        # Аналогично, как у слона, только другой направление
        def find_other_color(x, y):
            for i in desk._figurs:
                if (x, y) == i._start_position and i._color != self._color:
                    return [(x, y)]
            return []
        pit = desk._position_in_desk
        res1 = []
        res2 = []
        x, y = self._x, self._y
        for i in range(-7, 8):
            if 0 <= x + i <= 7 and i != 0:
                res1.append((x + i, y))
            if i < 0 and (x + i, y) in pit:
                res1 = [(x + i, y)]
            if i > 0 and (x + i, y) in pit:
                res1.append((x + i, y))
                break
        for i in range(-7, 8):
            if 0 <= y + i <= 7 and i != 0:
                res2.append((x, y + i))
            if i < 0 and (x, y + i) in pit:
                res2 = [(x, y + i)]
            if i > 0 and (x, y + i) in pit:
                res2.append((x, y + i))
                break

        mass = Positions(res1 + res2)
        super(Ladia, self).can_move(mass)

    def get_name(self):
        super(Ladia, self).get_name(self._name)


class Ferz(Figurs):

    def __init__(self, x, y, color):
        super(Ferz, self).__init__(x, y, color)
        self._name = "F"
        self.eleph = Eleph(self._x, self._y, self._color) # Композиция
        self.ladia = Ladia(self._x, self._y, self._color)


    def can_move(self):
        # совмещение ходов слона и ладьи многопоточно

        def figure_creating(fig, x, y):
            if fig._name == "E":
                fig = Eleph(x, y, self._color)
            else:
                fig = Ladia(x, y, self._color)

            fig.can_move()

            if fig._name == "E":
                self.eleph = fig
            else:
                self.ladia = fig

            # print(fig._moves, fig._name)

        th1 = Thread(target=figure_creating, args=(self.eleph, self._x, self._y, ))
        th2 = Thread(target=figure_creating, args=(self.ladia, self._x, self._y, ))
        th2.start()
        th1.start()

        th1.join()
        th2.join()

        mass = Positions(self.eleph + self.ladia)
        super(Ferz, self).can_move(mass)

    def get_name(self):
        super(Ferz, self).get_name(self._name)

desk = _Desk([])
