from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout

from lectures import lecture_1_eng, lecture_1_rus

from sql_setup import sql_return_username, sql_user_unlogined



class MainPage(GridLayout):
    def __init__(self, username, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 10
        self.padding = [10, 10, 10, 100]
        self.user = username

        self.nick_label = Label(text=self.user)
        self.label_layout = BoxLayout(orientation='vertical', spacing=1)
        self.label_layout.add_widget(self.nick_label)

        words_button = Button(text='WORDS LEARNING')
        words_button.bind(on_press=self.words_start)
        self.label_layout.add_widget(words_button)

        for lesson_number in range(1, 19):
            lesson_button = Button(text=f'{lesson_number} Lesson')
            lesson_button.bind(on_press=self.lecture)
            self.label_layout.add_widget(lesson_button)
        
        self.exit_b = Button(text='Выйти из аккаунта')
        self.exit_b.bind(on_press=self.exit_tomen)
        self.label_layout.add_widget(self.exit_b)

        self.add_widget(self.label_layout)


    def update(self):
        self.user = sql_return_username()[0]
        self.nick_label.text = self.user
    
    def exit_tomen(self, instance):
        sql_user_unlogined()
        app = App.get_running_app()
        app.root.current = 'login'

    def words_start(self, instance):
        app = App.get_running_app()
        app.root.current = 'words'
    
    def lecture(self, isintence):
        app = App.get_running_app()
        app.root.current = 'l1'

class Lecture1(BoxLayout):
    def __init__(self, **kwargs):
        super(Lecture1, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 10
        self.padding = [10, 10, 10, 10]

        self.scroll_view = ScrollView(size_hint=(1, 1)) 
        self.text_label = Label(text=lecture_1_eng, size_hint_y=None, valign='top')
        self.text_label.bind(width=lambda *x: self.text_label.setter('text_size')(self.text_label, (self.text_label.width, None)))
        self.text_label.bind(texture_size=self.text_label.setter('size'))
        self.text_label.height = self.text_label.texture_size[1]
        self.scroll_view.add_widget(self.text_label)
        self.add_widget(self.scroll_view)

        buttons_layout = BoxLayout(size_hint_y=None, height=150, spacing=10)

        self.language_button = Button(text='Русский', size_hint_y=None, height=50)
        self.language_button.bind(on_press=self.toggle_language)
        buttons_layout.add_widget(self.language_button)

        self.practice1 = Button(text='Practice', size_hint_y=None, height=50)
        self.practice1.bind(on_press=self.practice)
        buttons_layout.add_widget(self.practice1)

        self.back = Button(text='Назад', size_hint_y=None, height=50)
        self.back.bind(on_press=self.back_to_screen)
        buttons_layout.add_widget(self.back)

        self.add_widget(buttons_layout)

    def toggle_language(self, instance):
        if self.language_button.text == 'Русский':
            self.text_label.text = lecture_1_rus
            self.language_button.text = 'English'
        else:
            self.text_label.text = lecture_1_eng
            self.language_button.text = 'Русский'
    def back_to_screen(self, instance):
        app = App.get_running_app()
        app.root.current = 'main'

    def practice(self, instance):
        app = App.get_running_app()
        app.root.current = 'p1'

class Practice1(GridLayout):
    def __init__(self, **kwargs):
        super(Practice1, self).__init__(**kwargs)
        self.cols = 1
        self.spacing = 10
        self.padding = [15, 300, 10, 250] 

        self.word = Label(text="She ___ books every day", size_hint_y=None, height=50, halign='center')
        self.word.bind(size=self.word.setter('text_size'))
        
        button_layout = GridLayout(cols=3, spacing=10, size_hint_y=None, height=50)
        
        self.variant1 = Button(text="read")      
        self.variant2 = Button(text="eat")
        self.variant3 = Button(text="reads")
        button_layout.add_widget(self.variant1)
        button_layout.add_widget(self.variant2)
        button_layout.add_widget(self.variant3)


        self.variant1.bind(on_press=lambda instance: self.check_answer("read", instance))
        self.variant2.bind(on_press=lambda instance: self.check_answer("eat", instance))
        self.variant3.bind(on_press=lambda instance: self.check_answer("reads", instance))

        # Back button
        self.back = Button(text='НАЗАД', size_hint_y=None, height=50)
        self.back.bind(on_press=self.back_pressed)

        self.add_widget(self.word)
        self.add_widget(button_layout)
        self.add_widget(self.back)
        
    
    def back_pressed(self, instance):
        app = App.get_running_app()
        app.root.current = 'l1'
    
    def check_answer(self, word, instance):
        if word == "reads":
            instance.background_color = get_color_from_hex("#00FF00")
            self.word.text = "She reads books every day"
            Clock.schedule_once(lambda dt: self.back_pressed(instance), 1)
        else:
            instance.background_color = get_color_from_hex("#FF0000")
        



