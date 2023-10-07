# --------------Импортирование нужных библиотек для разработки приложения---------------------#
from tkinter import *
from tkinter import ttk
import os


class App:
    def __init__(self, root):
# --------------Инициализация массивов для хранения данных---------------------#
        self.dir_list = []
        self.files_list = []
        self.chosen_files = []
        self.chosen_word = ""
        self.words_list = []
# --------------Поиск всех текстовых файлов и папок в корневой директории---------------------#
        for address, dirs, files in os.walk("."):
            for dir in dirs:
                self.dir_list.append(os.path.join(address, dir))
            for file in files:
                if ".txt" in file:
                    self.files_list.append(os.path.join(address, file))
# --------------Создание графического интерфейса---------------------#
        self.root = root
        self.root.title("Курсовая работа. Вариант 49")
        self.root.geometry('1024x768')
        self.tab_control = ttk.Notebook(root)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab1, text='Папки' )
        self.tab_control.add(self.tab2, text='Файлы')
        self.tab_control.add(self.tab3, text='Поиск')
        self.tab_control.pack(fill='both')

        self.dir_list_var = Variable(value=self.dir_list)
        # --------------Создание первой вкладки---------------------#
        self.label_folders = Label(master=self.tab1, text='Cписок папок')
        self.label_folders.pack()
        self.list_folders = Listbox(master=self.tab1, listvariable=self.dir_list_var, selectmode=MULTIPLE, height=30)
        self.list_folders.pack(fill=BOTH)
        self.btn_choose = Button(master=self.tab1, text="Выбрать", command=self.selected_dirs)
        self.btn_choose.pack()
        self.btn_choose_all = Button(master=self.tab1, text="Выбрать все папки", command=self.selected_all_dirs)
        self.btn_choose_all.pack()
        # --------------Создание второй вкладки---------------------#
        self.label_files = Label(master=self.tab2, text='Cписок файлов в папках')
        self.label_files.pack()
        self.list_files = Listbox(master=self.tab2)
        self.list_files.pack(fill=BOTH, expand=1)
        # --------------Создание третей вкладки---------------------#
        self.frame_words_btns = Frame(master=self.tab3)
        self.frame_words_btns.pack()

        self.btn_add = Button(master=self.frame_words_btns, text="Добавить", width=20, command=self.btn_add_clicked)
        self.btn_del = Button(master=self.frame_words_btns, text="Удалить", width=20, command=self.btn_del_clicked)

        self.key_words = LabelFrame(master=self.tab3, text='Выбор ключевого слова', relief=SOLID, borderwidth=2)
        self.key_search = LabelFrame(master=self.tab3, text='Поиск выбранного слова', relief=SOLID, borderwidth=2)

        self.btn_add.pack(padx=10, side=LEFT)
        self.btn_del.pack(padx=5, side=LEFT)

        self.key_words.pack(fill=BOTH, side=TOP, padx=10)
        self.key_search.pack(fill=BOTH, side=TOP, padx=10, expand=1)

        self.list_words = Listbox(master=self.key_words, width=35, height=15)
        self.list_words.pack(side=TOP, pady=5, fill=BOTH, expand=1)
        self.btn_find = Button(master=self.key_search, text="Найти", width=30, command=self.btn_find_clicked)
        self.btn_find.pack(side=TOP)
        self.list_search = Listbox(master=self.key_search, width=35, height=25)
        self.list_search.bind("<Double-1>", self.list_double_clicked)
        self.list_search.pack(side=TOP, pady=5, fill=BOTH, expand=1, padx=5)

        self.load_list()

# --------------Загрузка ключевых слов текстового файла---------------------#
    def load_list(self):
        try:
            with open("KeyList.txt", "r") as file:
                for word in file:
                    self.words_list.append(word.strip())
                    self.list_words.insert(END, word)
        except:
            with open("KeyList.txt", "w") as file:
                pass

 # --------------Функция отбора необходимых папок и их сохранения---------------------#
    def selected_dirs(self):
        self.list_files.delete(0, END)
        self.chosen_files.clear()
        selected_indices = self.list_folders.curselection()
        selected_dirs = ([self.list_folders.get(i) for i in selected_indices])
        for dir in selected_dirs:
            for file in self.files_list:
                if dir in file:
                    self.chosen_files.append(file)
                    self.list_files.insert(END, file)

# --------------Функция отбора всех файлов в папках---------------------#
    def selected_all_dirs(self):
        self.list_files.delete(0, END)
        for dir in self.dir_list:
            for file in self.files_list:
                if dir in file:
                    self.chosen_files.append(file)
                    self.list_files.insert(END, file)

# --------------Функция добавления ключевого слова---------------------#
    def btn_add_clicked(self):
        window = Toplevel(self.root)
        window.title("Добавить ключевое слово")
        window.attributes('-toolwindow', True)
        label = Label(window, text="Новое ключевое слово")
        entry = Entry(window, width=20)
        button = Button(window, text="Сохранить", command=lambda: self.btn_add_confirm(window, entry.get()))
        label.pack(side=LEFT, padx=5, pady=5)
        entry.pack(side=LEFT, padx=5, pady=5)
        button.pack(side=LEFT, padx=5, pady=5)

# --------------Функция подтверждения добавления ключевого слова---------------------#
    def btn_add_confirm(self, window, text):
        if text == "":
            window.destroy()
        else:
            self.words_list.append(text)
            self.list_words.insert(END, text)
            with open("KeyList.txt", "w") as file:
                for word in self.words_list:
                    file.write(word.strip() + "\n")
            window.destroy()

# --------------Функция удаления ключевого слова---------------------#
    def btn_del_clicked(self):
        if self.words_list:
            self.words_list.remove(self.list_words.get(self.list_words.curselection()).strip())
            with open("KeyList.txt", "w") as file:
                for word in self.words_list:
                    file.write(word.strip() + "\n")
            self.list_words.delete(self.list_words.curselection())

    # --------------Функция для выбора ключевого слова---------------------#
    def btn_find_clicked(self):
        self.chosen_word=""
        self.list_search.delete(0, END)
        i = self.list_words.curselection()
        word = self.list_words.get(i).rstrip()
        self.chosen_word=word
        for file in self.chosen_files:
            f = open(file, encoding='utf-8')
            for row in f:
                if str(word) in row:
                    self.list_search.insert(END, file)
                    break

# --------------Функция для поиска ключевого слова в выбранных файлах ---------------------#
    def list_double_clicked(self,event):
        if self.list_search.get(0) != "":
            window = Toplevel(self.root)
            window.title("Результат поиска")
            window.attributes('-toolwindow', True)
            text_box = Text(master=window)
            text_box.pack()
            text_box.bindtags((text_box, window, "all"))
            index_of_word = self.list_search.curselection()
            file = self.list_search.get(index_of_word)
            word = self.chosen_word

            str = 0
            i = 0
            with open(file, "r", encoding="utf-8") as f:
                for row in f:
                    str += 1
                    if word in row:
                        i = row.find(word)
                        break

            with open(file, "r", encoding="utf-8") as f:
                first = f"{str}.{i}"
                last = f"{str}.{i + len(word)}"
                text_box.insert(END, f.read())
                text_box.tag_add("highlightline", first, last)
                text_box.tag_config("highlightline", background="yellow")

# --------------Инициализация приложения---------------------#
if __name__ == '__main__':
    root = Tk()
    app = App(root)
    root.mainloop()

