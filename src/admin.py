from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock


from sql_setup import sql_add_new_words, sql_user_unlogined

class Admin(GridLayout):
    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
        self.cols = 2
        self.spacing = 10  # Добавляем пространство между виджетами
        self.padding = [15, 250, 10, 250]  # Добавляем внешний отступ

        label_layout = BoxLayout(orientation='vertical', spacing=1)

        label_layout.add_widget(Label(text='Русское'))
        self.rus = TextInput(multiline=False)
        label_layout.add_widget(self.rus)

        label_layout.add_widget(Label(text='Английское'))
        self.eng = TextInput(password=False, multiline=False)
        label_layout.add_widget(self.eng)

        self.message_label = Label(text='', color=(1, 0, 0, 1))
        label_layout.add_widget(self.message_label)

        self.add_b = Button(text='Добавить слова')
        self.add_b.bind(on_press=self.callback_add_words)
        label_layout.add_widget(self.add_b)
        
        self.register = Button(text='Выйти из админки')
        self.register.bind(on_press=self.exit_)
        label_layout.add_widget(self.register)

        self.add_widget(label_layout)
    
    def callback_add_words(self, instance):
        try:
            sql_add_new_words(self.rus, self.eng)
            self.message_label.text = "Слова добавлены"
            self.message_label.color = (0, 1, 0, 1)
            Clock.schedule_once(lambda dt: self.drop_text(), 2)
        except Exception as e:
            self.message_label.text = "Не удалось добавить слова"
            self.message_label.color = (1, 0, 0, 1)
            print(f"ERR: {e}")

    def drop_text(self):
        self.message_label.text = ''
    
    def exit_(self, isintence):
        sql_user_unlogined()
        app = App.get_running_app()
        app.root.current = 'login'
    