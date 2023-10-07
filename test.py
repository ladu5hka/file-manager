import unittest
from main import *


class Test(unittest.TestCase):
    def setUp(self):
        self.root=Tk()
        self.app=App(self.root)

    def test_dirs(self):
        self.assertListEqual(self.app.dir_list,['.\\1', '.\\2', '.\\3', '.\\4', '.\\5', '.\\__pycache__'])

    def test_files(self):
        self.assertListEqual(self.app.files_list,['.\\KeyList.txt', '.\\1\\1-2.txt', '.\\1\\1.txt', '.\\2\\fileInFolder2.txt', '.\\3\\3.txt', '.\\4\\4.txt', '.\\5\\5.txt'])

    def test_chosen_files(self):
        self.assertListEqual(self.app.words_list,['love', 'hey'])

    def test_btn_find(self):
        self.assertEqual(self.app.btn_find.cget("text"),'Найти')

    def test_btn_add(self):
        self.assertEqual(self.app.btn_add.cget("text"),"Добавить")

    def test_btn_del(self):
        self.assertEqual(self.app.btn_del.cget("text"),"Удалить")

    def test_key_words(self):
        self.assertEqual(self.app.key_words.cget("text"),'Выбор ключевого слова')

    def test_key_search(self):
        self.assertEqual(self.app.key_search.cget("text"),'Поиск выбранного слова')

    def test_label_folders(self):
        self.assertEqual(self.app.label_folders.cget("text"),'Cписок папок')

    def test_btn_choose(self):
        self.assertEqual(self.app.btn_choose.cget("text"),'Выбрать')


if __name__ == '__main__':
    unittest.main()





