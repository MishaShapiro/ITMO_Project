from tkinter import *
from tkinter.ttk import Combobox
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import messagebox as mb
import datetime

def Money_Upload(): # Обновление счётчика потраченных денег
    lens = Open_File()
    res = 0
    for i in lens:
        if i != "":
            res += int(i.split(" ")[2])
    lbl_4["text"] = "Всего потрачено {0} рублей".format(res)

def Open_File(): # Просмотр файла и вывод массива всех строк
    files = open("C:/Users/GANSOR/PycharmProjects/pythonProject/List.txt", "r")
    lens = list(map(str, files.read().split("\n")))
    files.close()
    return lens

def Tabl_Upload(): # Заполнение таблицы
    dates, categories = [""], [""]
    lens = Open_File()
    for i in table.get_children():  # Удалить из таблицы все элементы
        table.delete(i)
    for i in lens:  # Добавить в таблицу новые элементы
        table.insert("", END, values=list(map(str, i.split(" "))))
        if i != '':  # Используется для всес кроме последнего, пустого элемента
            k = list(map(str, i.split(" ")))  # Разделяем строки на массив
            dates.append(k[4])  # Добавляем новую дату для фильтрования
            categories.append(k[3])  # Добавляем новую категорию для фильтрования
            filer["values"] = list(set(categories))
            filer_1["values"] = list(set(dates))

def Button_Click(): # Кнопка добавления в список нового элемента
    if entr_name.get() == "" or entr_price.get() == "" or category.get() == "": # Проверка на заполненость ячеек
        mb.showerror("Ошибка данных", "Заполните все окна!")
        return None

    try: # Проверяем, является ли значение цены числовым
        int(entr_price.get())
    except: # Если нет, выводится ошибка
        mb.showerror("Ошибка данных", "Укажите цену числом!")
        return None

    lens = Open_File() # Нахождение количества элементов для последующего использования в добавлении нового

    files = open("C:/Users/GANSOR/PycharmProjects/pythonProject/List.txt", "a") # Добавление нового элемента ID (Количество предыдущих + Пустой), Информация из выпадающих списков, Дата через datetime и перенос строки
    files.write(str(len(lens)) + " " + entr_name.get() + " " + entr_price.get() + " " + category.get() + " " + str((datetime.datetime.now()).strftime("%d-%m-%Y")) + "\n")
    files.close()
    Money_Upload()
    Tabl_Upload()

def Button_Click2(): # Сортируем список по различным параметрам
    lens = Open_File()
    key = {} # Словарь со значениями элементов, по которым будет происходить сортировка
    Contr_num = 0 # Контрольное значение для упрощения задавания словарей
    # Приравниваем контрольное значение к соответствующей позицуии элемента из строки (Исходя из выбранного типа сортировки)
    if sorter.get() == "По ID":
        Contr_num = 0
    elif sorter.get() == "По цене от макс." or sorter.get() == "По цене от мин.":
        Contr_num = 2
    elif sorter.get() == "По категории":
        Contr_num = 3
    elif sorter.get() == "По дате":
        Contr_num = 4
    for i in lens:
        if i == "":
            continue
        if i.split(" ")[Contr_num] in key.keys(): # Добавляем в словарь по кючу (Выбранному элементу от Contr_num), массив со строками, соответствующими ключу
            key[i.split(" ")[Contr_num]].append(i)
        elif Contr_num == 0 or  Contr_num == 1 or Contr_num == 2: # В случае с числами (Мин, Макс и ID) переводим str в int для сортировки
            key[int(i.split(" ")[Contr_num])] = [i]
        else:
            key[i.split(" ")[Contr_num]] = [i] # Остальное остаётся в строковом виде
    if sorter.get() == "По цене от макс.": # Особоя сортировка от макс к мин
        mass = sorted(key.keys(), reverse=True)
    else:
        mass = sorted(key.keys()) # Сортируем ключи

    for i in table.get_children():  # Удалить из таблицы все элементы
        table.delete(i)

    for j in mass: # Проходимся по отсортированным ключам
        for i in key[j]: # Проходимся по элементам заданных ключей
            table.insert("", END, values=list(map(str, i.split(" "))))

def Button_Click3(): # Кнопка для фильтрования
    for i in table.get_children(): # Удаляем всё старое из таблицы
        table.delete(i)
    lens = Open_File()
    for i in lens: # Проходимся по строкам
        if i != "" and i.split(" ")[3] == filer.get() and i.split(" ")[4] == filer_1.get(): # Проверяем, чтоб элементы строк были равны выбранным из выпадающего списка элементам
            table.insert("", END, values=list(map(str, i.split(" "))))
        elif i != "" and "" == filer.get() and i.split(" ")[4] == filer_1.get():
            table.insert("", END, values=list(map(str, i.split(" "))))
        elif i != "" and i.split(" ")[3] == filer.get() and "" == filer_1.get():
            table.insert("", END, values=list(map(str, i.split(" "))))
        elif i != "" and "" == filer.get() and "" == filer_1.get():
            table.insert("", END, values=list(map(str, i.split(" "))))

def Button_Click4():
    res = []
    dell_num = 0 # Значение для того, чтобы определить, какой элемент будет удалён
    if dell_ID.get() == "": # Если не указан ID элемента, который нужно удалить, то высвечивается ошибка
        mb.showerror("Ошибка!", "Не введён ID!")
        return None
    lens = Open_File()
    for i in lens:
        if i.split(" ")[0] != dell_ID.get(): # Проходимся по первым элементам строк (ID) и сравниваем их с искомым элементом
            if dell_num == 0: # Если элемент ещё не был удалён, то просто добавляем строки
                res.append(i)
            elif i != "":
                res.append(str(int(i.split(" ")[0])-1) + " " + " ".join(i.split(" ")[1::])) # Если элемент был удалён, то нужно сдвинуть все индексы строк на 1 и добавить их в res
        else: # Если искомый элемент найден, изменяем значение dell_num для сдвига индексов (Искомый элемент не добавляем в массив)
            dell_num = 1
    if dell_num == 0: # Если к концу выполнения не был удалён ни один элемент, значит было введено несуществующее ID для удаления
        mb.showerror("Ошибка!", "Неверно указан ID!") # Выводим ошибку
        return None

    files = open("C:/Users/GANSOR/PycharmProjects/pythonProject/List.txt", "w") # Переписываем все элементы в файл, без удалённого
    for i in res:
        files.write(i + "\n")
    files.close()
    Money_Upload()
    Tabl_Upload() # Обновляем таблицу

# ИНТЕРФЕЙС

root = Tk()
root.geometry("500x450")
root.title("Money Control")

# Задаём элементы визуала

btn_vvod = Button(root, width = 20, height = 1, text = "Внести в список", command = Button_Click)
entr_name = Entry(root, width = 15)
entr_price = Entry(root, width = 15)
category = Combobox(root, width = 10,  values = ("Одежда", "Еда", "Быт.техника", "Электр.техника", "Канцелярия"))
sorter = Combobox(root, width = 20, values = ("По ID", "По цене от мин.", "По цене от макс.", "По категории", "По дате"))
btn_vivod = Button(root, width = 20, height = 1, text = "Отсортировать покупки:", command = Button_Click2)
choice = Button(root, width = 20, height = 1, text = "Выбрать фильтр:", command = Button_Click3)
btn_dell = Button(root, width = 20, height = 1, text = "Удалить элемент c ID:", command = Button_Click4)
dell_ID = Entry(root, width = 15)
quit_btn = Button(root, width = 20, height = 1, text = "Выход из программы", command = root.destroy)
lbl_1 = Label(root, text = "Категория")
lbl_2 = Label(root, text = "Название")
lbl_3 = Label(root, text = "Цена")
lbl_4 = Label(root, text = "Всего потрачено: 0 рублей")

heads = ["ID", "Название",  "Цена", "Категория", "Дата"] # Заголовки таблицы
table = ttk.Treeview(root, columns = heads, show = "headings") # Создание элемента таблицы

for i in heads: # Cоздание колонок определённой ширины
    table.column(i, width = 80)

for head in heads: # Заполнение заголовков таблиц и заполнение
    table.heading(head, text = head, anchor = "center")

Money_Upload() # Обновляем счётчик потраченных денег

dates, categories = [""], [""] # Создаём списки для фильтрации (По умолчанию с пустыми элементами)

lens = Open_File()

for i in lens: # Проходимся по элементам списка
    table.insert("", END, values = list(map(str, i.split(" "))))
    if i != '':
        k = list(map(str, i.split(" "))) # Добавляем в фильтр все категории и даты, которые есть
        dates.append(k[4])
        categories.append(k[3])

# Создаём и располагаем выпадающие списки для фильтра

filer = Combobox(root, width=15, values=(list(set(categories))))
filer.place(x=180, y=90)
filer_1 = Combobox(root, width=15, values=(list(set(dates))))
filer_1.place(x=300, y=90)

# Располагаем в интерфейсе все элементы

lbl_1.place(x = 10, y = 9)
lbl_2.place(x = 100, y = 9)
lbl_3.place(x = 200, y = 9)
btn_vvod.place(x = 300, y = 30)
entr_name.place(x = 100, y = 30)
entr_price.place(x = 200, y = 30)
category.place(x = 10, y = 30)
sorter.place(x = 180, y = 60)
btn_vivod.place(x = 10, y = 60)
table.place(x = 10, y = 120)
choice.place(x = 10, y = 90)
btn_dell.place(x = 10, y = 370)
dell_ID.place(x = 180, y = 370)
quit_btn.place(x = 300, y = 370)
lbl_4.place(x = 18, y = 410)

root.mainloop()
