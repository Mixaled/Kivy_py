from kivy.app import App
from kivy.clock import Clock
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.utils import get_color_from_hex
from kivy.uix.boxlayout import BoxLayout


import random

from functools import partial

from sql_setup import sql_dict_with_words


class Words(BoxLayout):
    def __init__(self, **kwargs):
        super(Words, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [10, 10, 10, 10]

        # Создаем ScrollView для отображения слов
        scrollview = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.grid_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, row_force_default=True, row_default_height=40)
        self.grid_layout.bind(minimum_height=self.grid_layout.setter('height'))

        self.update()

        scrollview.add_widget(self.grid_layout)
        self.add_widget(scrollview)

        # Создаем BoxLayout для кнопок
        buttons_layout = BoxLayout(size_hint_y=None, height=100, spacing=10)
        
        # Кнопка START
        self.start = Button(text='START', size_hint_y=None, height=50)
        self.start.bind(on_press=self.start_pressed)
        buttons_layout.add_widget(self.start)
        
        # Кнопка НАЗАД
        self.back = Button(text='НАЗАД', size_hint_y=None, height=50)
        self.back.bind(on_press=self.back_pressed)
        buttons_layout.add_widget(self.back)
        
        # Добавляем кнопки в основной layout
        self.add_widget(buttons_layout)
    def back_pressed(self,isintence):
        app = App.get_running_app()
        app.root.current = 'main'
    
    def start_pressed(self,isintence):
        app = App.get_running_app()
        app.root.current = 'learn'
    
    def update(self):
        self.word_dict = sql_dict_with_words()
        for rus, eng in self.word_dict.items():
            label_rus = Label(text=rus, size_hint_y=None, height=40)
            label_eng = Label(text=eng, size_hint_y=None, height=40)
            self.grid_layout.add_widget(label_rus)
            self.grid_layout.add_widget(label_eng)

    
class Learning(GridLayout):
    def __init__(self, **kwargs):
        super(Learning, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 10
        self.padding = [15, 300, 10, 250] 

        # получаем данные из БД и образуем временный словарь {русский:английский}
        self.word_dict = sql_dict_with_words()
        
        self.ini()

        # выводим англйиское слово в центре
        self.word = Label(text=correct_eng, size_hint_y=None, height=50, halign='center')
        self.word.bind(size=self.word.setter('text_size'))  # Привязываем размер для выравнивания текста
        self.add_widget(self.word)

        # горизонатльный слой с кнопками
        button_layout = GridLayout(cols=3, spacing=10, size_hint_y=None, height=50)
        
        self.variant1 = Button(text=self.stack[0])      
        self.variant2 = Button(text=self.stack[1])
        self.variant3 = Button(text=self.stack[2])


        self.variant1.bind(on_press=lambda instance: self.check_answer(self.stack[0], instance))
        self.variant2.bind(on_press=lambda instance: self.check_answer(self.stack[1], instance))
        self.variant3.bind(on_press=lambda instance: self.check_answer(self.stack[2], instance))

        self.variant3.bind(on_press=partial(self.check_answer, self.stack[2]))

        button_layout.add_widget(self.variant1)
        button_layout.add_widget(self.variant2)
        button_layout.add_widget(self.variant3)

        # main layout
        self.add_widget(button_layout)

        # Back button
        self.back = Button(text='НАЗАД', size_hint_y=None, height=50)
        self.back.bind(on_press=self.back_pressed)
        self.add_widget(self.back)
    
    def back_pressed(self, instance):
        app = App.get_running_app()
        app.root.current = 'words'
    
    #def rand_word(self, stack: list):
    #    a = random.choice(stack)
    #    if a == self.correct_rus:
    #        self.correct_variant = stack.index(a)
    #    stack.remove()
    #    return a

    def check_answer(self, word, instance):
        #print(word)
        #print(self.correct_rus)
        if word == self.correct_rus:
            #print("Correct!")
            instance.background_color = get_color_from_hex("#00FF00")
        else:
            #print("Incorrect!")
            instance.background_color = get_color_from_hex("#FF0000")
        Clock.schedule_once(lambda dt: self.reset_learning(), 1)

    def reset_learning(self):
        self.variant1.background_color = (1, 1, 1, 1)
        self.variant2.background_color = (1, 1, 1, 1)
        self.variant3.background_color = (1, 1, 1, 1)
        self.ini()

        self.word.text = correct_eng
        self.variant1.text = self.stack[0]
        self.variant2.text = self.stack[1]
        self.variant3.text = self.stack[2]

    def ini(self):
        global correct_eng

        self.correct_rus = random.choice(list(self.word_dict.keys()))
        keys_list = list(self.word_dict.keys())
        correct_eng = self.word_dict[self.correct_rus]
        incorrect_words = random.sample([word for word in keys_list if word != self.correct_rus], 2)
        wrong_rus = incorrect_words[0]
        wrong_rus2 = incorrect_words[1]

        #self.correct_variant = None

        self.stack = [self.correct_rus, wrong_rus, wrong_rus2]
        random.shuffle(self.stack)          