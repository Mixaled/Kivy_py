from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


from sql_setup import sql_login_check, sql_user_logined, sql_is_admin_loggined

class Login(GridLayout):
    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10  # Добавляем пространство между виджетами
        self.padding = [15, 250, 10, 250]  # Добавляем внешний отступ

        label_layout = BoxLayout(orientation='vertical', spacing=1)

        label_layout.add_widget(Label(text='Логин'))
        self.username = TextInput(multiline=False)
        label_layout.add_widget(self.username)

        label_layout.add_widget(Label(text='Пароль'))
        self.password = TextInput(password=True, multiline=False)
        label_layout.add_widget(self.password)

        self.message_label = Label(text='', color=(1, 0, 0, 1))
        label_layout.add_widget(self.message_label)

        self.login = Button(text='Войти')
        self.login.bind(on_press=self.callback_login)
        label_layout.add_widget(self.login)
        
        self.register = Button(text='Регистрация')
        self.register.bind(on_press=self.callback_register)
        label_layout.add_widget(self.register)

        self.add_widget(label_layout)

    def callback_register(self,instance):
        app = App.get_running_app()
        app.root.current = 'registration'
    
    def callback_login(self, instance):
        username = self.username.text
        password = self.password.text
        if sql_login_check(username, password) is True:
            self.message_label.text = ""
            sql_user_logined(username)
            
            if sql_is_admin_loggined() == True:
                app = App.get_running_app()
                app.root.current = 'admin'
            else:
                app = App.get_running_app()
                app.root.current = 'main'

        else:
            self.message_label.text = "Логин или пароль неверный"
            self.password.text = ''
            self.message_label.color = (1, 0, 0, 1)
    def ret_nickname(self):
        return self.username.text