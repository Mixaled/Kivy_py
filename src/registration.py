from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from functools import partial

from sql_setup import sql_add_new_user

class Registration(GridLayout):
    def __init__(self, **kwargs):
        super(Registration, self).__init__(**kwargs)
        self.cols = 4
        self.spacing = 10  # Добавляем пространство между виджетами
        self.padding = [10, 250, 10, 250]  # Добавляем внешний отступ

        label_layout = BoxLayout(orientation='vertical', spacing=1)

        #label_layout.add_widget(Label(text='Почта'))
        #self.password = TextInput(password=False, multiline=False)
        #label_layout.add_widget(self.password)

        label_layout.add_widget(Label(text='Логин'))
        self.username = TextInput(multiline=False)
        label_layout.add_widget(self.username)

        label_layout.add_widget(Label(text='Пароль'))
        self.password = TextInput(password=False, multiline=False)
        label_layout.add_widget(self.password)

        self.message_label = Label(text='', color=(1, 0, 0, 1))
        label_layout.add_widget(self.message_label)

        self.login = Button(text='Создать аккаунт')
        self.login.bind(on_press=self.create_account_pressed)
        label_layout.add_widget(self.login)

        self.login = Button(text='Вернуться назад')
        self.login.bind(on_press=self.callback_turn_back)
        label_layout.add_widget(self.login)

        self.add_widget(label_layout)
    
    def create_account_pressed(self, instance):
        username = self.username.text
        password = self.password.text
        if username == '' or password == '':
            self.message_label.text = "Поля не должны быть пустыми"
            self.message_label.color = (1, 0, 0, 1)
            return
        res = sql_add_new_user(username, password)
        if res:
            self.message_label.text = "Пользователь создан"
            self.message_label.color = (0, 1, 0, 1)
        else:
            self.message_label.text = "Пользователь с таким именем уже существует"
            self.message_label.color = (1, 0, 0, 1)

    def callback_turn_back(self, instance):
        app = App.get_running_app()
        app.root.current = 'login'