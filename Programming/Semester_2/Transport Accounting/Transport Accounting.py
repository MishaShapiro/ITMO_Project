from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
import sqlite3
from tkcalendar import Calendar
from datetime import *

curent_date = datetime.now() # Текущая дата и время

class DataBase:

    def __init__(self):
        self.connection = sqlite3.connect("information.db") # Подключение к БД
        self.cursor = self.connection.cursor()

    def Delete_Table(self): # Удаление таблицы
        self.cursor.execute("""DROP TABLE all_transport;""")
        self.cursor.execute("""DROP TABLE all_reports;""")

    def Create_Table(self): # Создание таблицы
        self.cursor.execute("""CREATE TABLE all_transport (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type TEXT NOT NULL,
                maxweight FLOAT NOT NULL,
                lenght FLOAT NOT NULL,
                width FLOAT NOT NULL,
                height FLOAT NOT NULL);""")

        self.cursor.execute("""CREATE TABLE all_reports (
                id_rep INTEGER PRIMARY KEY AUTOINCREMENT,
                id INTEGER NOT NULL,
                time_start TEXT NOT NULL,
                time_end TEXT NOT NULL,
                name TEXT NOT NULL);""")

    def Test_Upload(self): # Данные по умолчанию (Для dev tools)
        elements = [("Газель", 2, 3, 2, 1.7),
                    ("Бычок", 3, 4.2, 2.2, 2.4),
                    ("MAN-10", 10, 6, 2.45, 2.7),
                    ("Фура", 20, 13.6, 2.46, 2.5)]
        self.cursor.executemany("""INSERT INTO all_transport VALUES(NULL, ?, ?, ?, ?, ?)""", elements)
        elements = [(1, "2023-05-12 13:30:00", "2023-05-12 14:00:00", "Зубенко Михаил Петрович"),
                    (2, "2023-05-13 14:30:00", "2023-05-13 18:10:00", "Иванов Игорь Юрьевич"),
                    (1, "2023-05-13 13:30:00", "2023-05-13 14:00:00", "Уразалин Амир")]
        self.cursor.executemany("""INSERT INTO all_reports VALUES(NULL, ?, ?, ?, ?)""", elements)

    def Commit_Table(self): # Commit
        self.connection.commit()

    def Output(self, table_name): # запрос всех элементов из таблицы
        self.cursor.execute("""SELECT * from {0};""".format(table_name))
        return self.cursor.fetchall()

    def Input(self, mass, table_name): # Добавление элемента в конец таблицы
        if table_name == "all_transport":
            self.cursor.execute("""INSERT INTO all_transport VALUES(NULL, ?, ?, ?, ?, ?)""", mass)
        else:
            self.cursor.execute("""INSERT INTO all_reports VALUES(NULL, ?, ?, ?, ?)""", mass)

    def Delete_element(self, id): # Удаление элемента по ID
        self.cursor.execute("""DELETE FROM all_transport WHERE id = {0};""".format(id))

class Commands: # Класс со всеми командами

    def __init__(self):
        pass
    # _________________________________________________________________
    # БЛОК СО ВСПОМОГАТЕЛЬНЫМИ ФУНКЦИЯМИ
    # _________________________________________________________________

    def Date_convertor(self, string): # Конвертирует дату (строковую) в удобный формат для дальнейшего использования
        string = string.split(" ")
        string = list(map(int, string[0].split("-") + string[1].split(":")))
        return datetime(string[0], string[1], string[2], string[3], string[4])

    def ID_connection(self, table1, table2): # Связь между таблицей заявок и таблицей транспорта
        res = []
        for i in table1:
            for j in table2:
                if i[1] == j[0]:
                    res.append([i[0]] + list(j) + list(i[2::]))
        return res

    def Upload_Table(self, info_from_table, uploaded_table): # Обновление таблицы (Получение элементов из БД)
        for i in uploaded_table.get_children(): # Удаление всех текущих элементов
            uploaded_table.delete(i)
        for i in info_from_table: # Добавление элементов в таблицу
            uploaded_table.insert("", END, values=i)

    def Add_Information_in_Table(self): # Добавить элемент в таблицу (Нажатие на кнопку)
        try: # Проверка на корректно введённые данные
            mass = [self.Add_Entry1.get(), float(self.Add_Entry2.get()), float(self.Add_Entry3.get()), float(self.Add_Entry4.get()), float(self.Add_Entry5.get())]
            if self.Add_Entry1.get() != "":
                if mass[1] <= 0 or mass[2] <= 0 or mass[3] <= 0 or mass[4] <= 0:
                    raise IndexError
                else:
                    self.data.Input(mass, "all_transport") # Добавление в БД
                    self.data.Commit_Table() # Commit БД
                    self.Upload_Table(self.data.Output("all_transport"), self.table) # Обновление таблицы
                    self.Back_Button_Action() # Возврат в главное окно
            else:
                messagebox.showerror("Ошибка!", "Заполните все ячейки корректно!")
        except:
            messagebox.showerror("Ошибка!", "Заполните все ячейки корректно! Грузоподьёмность, длина, ширина и высота должны быть заданы положительными числовыми значениями!")

    def Delete_Information_From_Table(self): # Удаление элемента главной таблицы по ID
        try:
            id = int(self.Delete_Entry.get())
            if not(id in [i[0] for i in self.data.Output("all_transport")]):
                messagebox.showerror("Ошибка!", "Такого ID нет в списке")
            else:
                self.data.Delete_element(id)
                self.data.Commit_Table()
                self.Upload_Table(self.data.Output("all_transport"), self.table)
                self.Back_Button_Action()
        except:
            messagebox.showerror("Ошибка!", "Введите ID корректно")

    def Sort_Table(self): # Сортировка элементов главной таблицы по предложенным признакам
        mass = self.data.Output("all_transport")
        current_id = 0 # Текущий ID
        key = {}
        res = []
        if self.Sort_List.get() == "ID": # Изменение переменно в зависимости от выбранного значения
            current_id = 0
        elif self.Sort_List.get() == "Типу":
            current_id = 1
        elif self.Sort_List.get() == "Грузоподьёмности":
            current_id = 2
        elif self.Sort_List.get() == "Длине":
            current_id = 3
        elif self.Sort_List.get() == "Ширине":
            current_id = 4
        elif self.Sort_List.get() == "Высоте":
            current_id = 5
        for i in mass: # проход по таблице для дальнейшей сортировки
            if i[current_id] in key.keys():
                key[i[current_id]].append(i)
            else:
                key[i[current_id]] = [i]
        for i in sorted(key.keys()): # Сортировка по ключевым значениям
            for j in key[i]:
                res.append(j)
        self.Upload_Table(res, self.table)

    def Reports_Selecion(self, time_start, time_end): # Подбор грузовиков
        mass = self.data.Output("all_reports")
        booked = []
        res = []
        for i in mass: # Проверка на интервалы времени
            if not(time_start > self.Date_convertor(i[3]) or time_end < self.Date_convertor(i[2])):
                booked.append(i[1]) # Если не подходит, то заносим в забронированные
        for i in self.data.Output("all_transport"): # Подбор свободных грузовиков
            if i[0] not in booked:
                res.append("{0} - {1}".format(i[0], i[1]))
        return res

    def Report_finder(self): # Определение значений для Combobox
        if len(self.Report_Entry1.get()) == 5 and len(self.Report_Entry2.get()) == 5: # Проверка на правильно заданное время
            try:
                time1 = list(map(int, self.Report_Entry1.get().split(":")))
                time2 = list(map(int, self.Report_Entry2.get().split(":")))
                calendardate = list(reversed(list(map(int, str(self.calendar.get_date()).split("/")))))
                self.full_time1 = datetime(int("20" + str(calendardate[0])), calendardate[2], calendardate[1], time1[0], time1[1])
                self.full_time2 = datetime(int("20" + str(calendardate[0])), calendardate[2], calendardate[1], time2[0], time2[1])
                if self.full_time1 > self.full_time2: # Инферсия, если время в первом больше, чем во втором (Прибавление одного дня)
                    self.full_time2 = datetime(int("20" + str(calendardate[0])), calendardate[2], calendardate[1]+1, time2[0], time2[1])
                # print(self.full_time1) # Проверка инверсии
                # print(self.full_time2)
                if curent_date < datetime(int("20" + str(calendardate[0])), calendardate[2], calendardate[1], time1[0], time1[1]): # Сравнение с текущей датой для исключения прошедшего времени
                    free_transport = self.Reports_Selecion(self.full_time1, self.full_time2)
                    self.Report_Combobox["values"] = free_transport # Обновление Combobox
                    self.Report_Combobox.set("")
                else:
                    messagebox.showerror("Ошибка", "Введённая дата и время уже прошли!")
            except:
                messagebox.showerror("Ошибка", "Неверно введено время!")
        else:
            messagebox.showerror("Ошибка", "Введите время в формате xx:xx (01:00; 13:30; 10:05)!")

    def Report_Create(self): # Создание заявки
        if self.Report_Combobox.get() == "" or self.Report_Entry3.get() == "":
            messagebox.showerror("Ошибка", "Заполнена не вся информация!")
        else:
            self.data.Input([self.Report_Combobox.get().split("-")[0][:-1:], self.full_time1, self.full_time2, self.Report_Entry3.get()], "all_reports") # Добавление в таблицу БД введённую информация
            self.data.Commit_Table()
            self.More_Information()

    def Forget_Main_Frame(self): # Очищает все элементы из текущего окна
        for elements in self.active_elements:
            elements.place_forget()

    # _________________________________________________________________
    # БЛОК С ОТРИСОВКОЙ
    # _________________________________________________________________
    def Draw_Main_Frame(self): # отрисовка главного окна
        self.Button_Add.place(x=10, y=10)
        self.Button_Delete.place(x=330, y=10)
        self.table.place(x=10, y=50)
        self.Button_Sort.place(x=500, y=10)
        self.Sort_List.place(x=500, y=50)
        self.Button_Info.place(x=500, y=190)
        self.Button_Report.place(x=500, y=230)
        self.Button_Quit.place(x=500, y=370)

    def Draw_Add_Report(self): # отрисовка окна с заявками
        self.Main_Label = Label(self.root, text="Составить заявку", font="48")
        self.Report_Label1 = Label(self.root, text="Выбрать дату")
        self.Report_Label2 = Label(self.root, text="Забронировать")
        self.Report_Label3 = Label(self.root, text="С: ")
        self.Report_Label4 = Label(self.root, text="До: ")
        self.Report_Label5 = Label(self.root, text="Вводите время в формате xx:xx\n часы, минуты", fg="darkblue", font="24")
        self.Report_Label6 = Label(self.root, text="Введите ФИО")
        self.Report_Entry1 = Entry(self.root,  width=25)
        self.Report_Entry2 = Entry(self.root, width=25)
        self.Report_Entry3 = Entry(self.root, width=25)
        self.Report_Button_Find = Button(self.root, width=25, height=1, text="Подобрать свободные грузовики", command=self.Report_finder)
        self.Report_Combobox = Combobox(self.root, width=25,  values=(), state='readonly')
        self.Report_Button_Create = Button(self.root, width=20, height=1, text="Создать заявку", command=self.Report_Create)
        self.Open_Table_Button = Button(self.root, width=20, height=1, text="Посмотреть таблицу", command=self.More_Information)
        self.calendar = Calendar(self.root, selectmode="day", year=curent_date.year, month=curent_date.month, day=curent_date.day)
        self.Button_Back = Button(self.root, width=15, height=1, text="Вернуться", command=self.Back_Button_Action)


    def Draw_Add_Frame(self): # определенеие элементов окна добавления
        self.Main_Label = Label(self.root, text="Добавить транспорт", font="48")
        self.Add_Label1 = Label(self.root, text="Тип")
        self.Add_Label2 = Label(self.root, text="Грузоподьемность, тонн")
        self.Add_Label3 = Label(self.root, text="Длина, м")
        self.Add_Label4 = Label(self.root, text="Ширина, м")
        self.Add_Label5 = Label(self.root, text="Высота, м")
        self.Add_Entry1 = Entry(self.root, width=25)
        self.Add_Entry2 = Entry(self.root, width=25)
        self.Add_Entry3 = Entry(self.root, width=25)
        self.Add_Entry4 = Entry(self.root, width=25)
        self.Add_Entry5 = Entry(self.root, width=25)
        self.Button_Add_Add = Button(self.root, width=15, height=1, text="Добавить", command=self.Add_Information_in_Table)
        self.Button_Back = Button(self.root, width=15, height=1, text="Вернуться", command=self.Back_Button_Action)

    def Draw_Delete_Frame(self):
        self.Main_Label = Label(self.root, text="Удалить транспорт", font="48")
        self.Delete_Label = Label(self.root, text="Введите ID:")
        self.Delete_Entry = Entry(self.root, width=25)
        self.Delete_Button = Button(self.root, width=15, height=1, text="Удалить", command=self.Delete_Information_From_Table)
        self.Button_Back = Button(self.root, width=15, height=1, text="Вернуться", command=self.Back_Button_Action)

    def Draw_More_Information_Frame(self):
        heads = ["ID заявки", "ID", "Тип", "Грузоподьемность, тонн", "Длина, м", "Ширина, м", "Высота, м", "Время, Начало", "Время, Конец", "ФИО Занявшего"]  # Заголовки таблицы
        self.table_information = ttk.Treeview(self.root, columns=heads, show="headings", height=16)  # Создание элемента таблицы
        for head in heads:
            if head == "ID":
                self.table_information.column(head, width=30)
            elif head == "Грузоподьемность, тонн" or head == "ФИО Занявшего":
                self.table_information.column(head, width=145)
            elif head == "Время, Начало" or head == "Время, Конец":
                self.table_information.column(head, width=130)
            else:
                self.table_information.column(head, width=73)
            self.table_information.heading(head, text=head, anchor="center")
        self.Main_Label = Label(self.root, text="Больше информации", font="48")
        self.Add_Report_Button = Button(self.root, width=15, height=1, text="Составить заявку", command=self.Add_Report)
        self.Button_Back = Button(self.root, width=15, height=1, text="Вернуться", command=self.Back_Button_Action)

    # _________________________________________________________________
    # БЛОК С РАСПОЛОЖЕНИЕМ ЭЛЕМЕНТОВ НОВЫХ ОКОН
    # _________________________________________________________________

    def Back_Button_Action(self): # Кнопка возврата в главное окно
        self.Forget_Main_Frame()
        self.root.geometry("700x450")
        self.active_elements = [self.Button_Add, self.Button_Delete, self.table, self.Button_Sort, self.Sort_List,
                                self.Button_Info, self.Button_Report, self.Button_Quit]
        self.Draw_Main_Frame()

    def Add_Report(self):
        self.Forget_Main_Frame()
        self.root.geometry("600x450")
        self.Draw_Add_Report()
        self.active_elements = [self.Main_Label, self.Report_Label1, self.Report_Label2, self.Report_Label3,
                                self.Report_Label4, self.calendar, self.Report_Label5, self.Report_Label6, self.Report_Entry1,
                                self.Report_Entry2, self.Report_Entry3, self.Report_Button_Find,  self.Report_Combobox,
                                self.Report_Button_Create, self.Open_Table_Button, self.Button_Back]
        self.Report_Label1.place(x=90, y=50)
        self.Report_Label2.place(x=400, y=50)
        self.Report_Label3.place(x=350, y=90)
        self.Report_Label4.place(x=350, y=130)
        self.Report_Label5.place(x=330, y=160)
        self.Report_Label6.place(x=220, y=300)
        self.Main_Label.place(x=250, y=10)
        self.calendar.place(x=10, y=90)
        self.Report_Entry1.place(x=400, y=90)
        self.Report_Entry2.place(x=400, y=130)
        self.Report_Entry3.place(x=220, y=350)
        self.Report_Button_Find.place(x=10, y=300)
        self.Report_Combobox.place(x=10, y=350)
        self.Report_Button_Create.place(x=10, y=400)
        self.Open_Table_Button.place(x=220, y=400)
        self.Button_Back.place(x=450, y=400)

    def More_Information(self): # Окно Больше информации
        self.Forget_Main_Frame()
        self.root.geometry("1000x450")
        self.Draw_More_Information_Frame()
        self.Upload_Table(self.ID_connection(self.data.Output("all_reports"), self.data.Output("all_transport")), self.table_information)
        self.active_elements = [self.Main_Label, self.table_information, self.Add_Report_Button,
                                self.Button_Back]
        self.Main_Label.place(x=350, y=10)
        self.table_information.place(x=10, y=40)
        self.Add_Report_Button.place(x=10, y=400)
        self.Button_Back.place(x=840, y=400)

    def Delete_Element(self): # Окно Удалить элемент
        self.Forget_Main_Frame()
        self.root.geometry("300x150")
        self.Draw_Delete_Frame()
        self.active_elements = [self.Main_Label, self.Delete_Label, self.Delete_Entry, self.Delete_Button, self.Button_Back]
        self.Main_Label.place(x=90, y=10)
        self.Delete_Label.place(x=10, y=40)
        self.Delete_Entry.place(x=90, y=40)
        self.Delete_Button.place(x=10, y=80)
        self.Button_Back.place(x=150, y=80)

    def Add_Element(self): # Окно добавления элемента в таблицу
        self.Forget_Main_Frame()
        self.root.geometry("500x250")
        self.Draw_Add_Frame()
        self.active_elements = [self.Main_Label, self.Add_Label1, self.Add_Label2, self.Add_Label3, self.Add_Label4,
                                self.Add_Label5, self.Add_Entry1, self.Add_Entry2, self.Add_Entry3, self.Add_Entry4,
                                self.Add_Entry5, self.Button_Add_Add, self.Button_Back]
        self.Main_Label.place(x=120, y=10)
        self.Add_Label1.place(x=10, y=40)
        self.Add_Label2.place(x=10, y=80)
        self.Add_Label3.place(x=10, y=120)
        self.Add_Label4.place(x=10, y=160)
        self.Add_Label5.place(x=10, y=200)
        self.Add_Entry1.place(x=200, y=40)
        self.Add_Entry2.place(x=200, y=80)
        self.Add_Entry3.place(x=200, y=120)
        self.Add_Entry4.place(x=200, y=160)
        self.Add_Entry5.place(x=200, y=200)
        self.Button_Add_Add.place(x=370, y=60)
        self.Button_Back.place(x=370, y=130)

    def Info(self): # информация о программе
        messagebox.showinfo("Информация", """   Создать программное обеспечение учета грузового транспорта для Автотранспортного отдела логистической компании.
        Задача подобрать доступный грузовой транспорт в зависимости от размера (веса) перевозимого груза, приложение реализовать с помощью ООП, БД, графического интерфейса. """)

    def Develop_Upload(self): # Откат таблицы до базовой (Инуструмент разработчика)
        self.data.Delete_Table()
        self.data.Create_Table()
        self.data.Test_Upload()
        self.data.Commit_Table()
        self.Upload_Table(self.data.Output("all_transport"), self.table)
        try:
            self.Upload_Table(self.ID_connection(self.data.Output("all_reports"), self.data.Output("all_transport")), self.table_information)
        except:
            pass

    def Develop_Output(self): # Вывод таблиц БД в консоль для проверки
        print(self.data.Output("all_transport"))
        print(self.data.Output("all_reports"))

class Elements(Commands):

    def __init__(self): # инициализация элементов главного окна
        self.root = Tk()

        # Инициализация базы данных
        self.data = DataBase()

        #Инициализация элементов меню
        self.main_menu = Menu()
        self.file_menu = Menu()
        self.command_menu = Menu()
        self.info_menu = Menu()
        self.devtools_menu = Menu()

        self.devtools_menu.add_command(label="Обновить базу данных", command=self.Develop_Upload)
        self.devtools_menu.add_command(label="Вывести таблицы из БД", command=self.Develop_Output)
        self.file_menu.add_command(label="Выход", command=lambda: self.root.destroy())
        self.command_menu.add_command(label="Добавить транспорт", command=super().Add_Element)
        self.command_menu.add_command(label="Удалить транспорт", command=super().Delete_Element)
        self.command_menu.add_command(label="Отсортировать таблицу", command=super().Sort_Table)
        self.info_menu.add_command(label="Больше информации", command=super().More_Information)
        self.info_menu.add_command(label="Составить заявку", command=super().Add_Report)
        self.info_menu.add_command(label="Больше о программе", command=super().Info)
        self.info_menu.add_cascade(label="Инструменты разработчика", menu=self.devtools_menu)

        self.main_menu.add_cascade(label="Программа", menu=self.file_menu)
        self.main_menu.add_cascade(label="Функции", menu=self.command_menu)
        self.main_menu.add_cascade(label="Информация", menu=self.info_menu)
        self.root.config(menu=self.main_menu)

        # Задний фон
        self.img = ImageTk.PhotoImage(Image.open("img\Fura.png"))
        self.bg_image = Label(image=self.img)
        self.bg_image.place(x=-2, y=-2)

        self.Button_Add = Button(self.root, width=20, height=1, text="Добавить транспорт", command=super().Add_Element)
        self.Button_Delete = Button(self.root, width=21, height=1, text="Удалить транспорт", command=super().Delete_Element)
        heads = ["ID", "Тип", "Грузоподьемность, тонн", "Длина, м", "Ширина, м", "Высота, м"]  # Заголовки таблицы
        self.table = ttk.Treeview(self.root, columns=heads, show="headings", height=16)  # Создание элемента таблицы
        for head in heads:
            if head == "ID":
                self.table.column(head, width=30)
            elif head == "Грузоподьемность, тонн":
                self.table.column(head, width=150)
            else:
                self.table.column(head, width=73)
            self.table.heading(head, text=head, anchor="center")
        self.Button_Sort = Button(self.root, width=23, height=1, text="Отсортировать таблицу по", command=super().Sort_Table)
        self.Sort_List = Combobox(self.root, width=25,  values=("ID", "Типу", "Грузоподьёмности", "Длине", "Ширине", "Высоте"), state='readonly')
        self.Sort_List.current(0)
        self.Button_Info = Button(self.root, width=23, height=1, text="Больше информации", command=super().More_Information)
        self.Button_Report = Button(self.root, width=23, height=1, text="Составить заявку", command=super().Add_Report)
        self.Button_Quit = Button(self.root, width=23, height=1, text="Выйти", command=lambda: self.root.destroy())

    def frame_draw(self): # отрисовка главного окна
        self.root.geometry("700x450")
        self.root.iconbitmap("img\Fura.ico")
        self.root.resizable(width=False, height=False)
        self.root.title("Transport Accounting")

        self.active_elements = [self.Button_Add, self.Button_Delete, self.table, self.Button_Sort, self.Sort_List,
                                self.Button_Info, self.Button_Report, self.Button_Quit] # список всех элементов в текущем окне для последующего скрытия
        super().Draw_Main_Frame()

        self.Upload_Table(self.data.Output("all_transport"), self.table) # Обновление таблицы
        self.root.mainloop()

frame = Elements()
frame.frame_draw()
