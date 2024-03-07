from register_panel import *
from registration import *
from sql_setup import *
from mainpage import *
from words import *
from admin import *
from kivy.uix.screenmanager import ScreenManager, Screen


class MainPageScreen(Screen):
    def __init__(self, **kwargs):
        super(MainPageScreen, self).__init__(**kwargs)
        self.main_page = MainPage(username='')
        self.add_widget(self.main_page)
    def on_enter(self, *args):
        self.main_page.update()

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.add_widget(Login())

class RegistrationScreen(Screen):
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        self.add_widget(Registration())

class WordsScreen(Screen):
    def __init__(self, **kwargs):
        super(WordsScreen, self).__init__(**kwargs)
        self.main_words = Words()
        self.add_widget(self.main_words)
    def on_enter(self, *args):
        self.main_words.update()

class LearningScreen(Screen):
    def __init__(self, **kwargs):
        super(LearningScreen, self).__init__(**kwargs)
        self.add_widget(Learning())

class Lecture1Screen(Screen):
    def __init__(self, **kwargs):
        super(Lecture1Screen, self).__init__(**kwargs)
        self.add_widget(Lecture1())

class Practice1Screen(Screen):
    def __init__(self, **kwargs):
        super(Practice1Screen, self).__init__(**kwargs)
        self.add_widget(Practice1())

class AdminScreen(Screen):
    def __init__(self, **kwargs):
        super(AdminScreen, self).__init__(**kwargs)
        self.add_widget(Admin())

class MyApp(App):
    def build(self):
        sm = ScreenManager()
        if sql_was_loggined() == True: # если был залогинен, то открываем главную страницу, а не вход
            sm.add_widget(MainPageScreen(name='main'))
            sm.add_widget(LoginScreen(name='login'))
        else: # если нет то открываем страницу входа 
            sm.add_widget(LoginScreen(name='login'))
            sm.add_widget(MainPageScreen(name='main'))
        sm.add_widget(RegistrationScreen(name='registration'))
        sm.add_widget(WordsScreen(name='words'))
        sm.add_widget(LearningScreen(name='learn'))
        sm.add_widget(Lecture1Screen(name='l1'))
        sm.add_widget(Practice1Screen(name='p1'))
        sm.add_widget(AdminScreen(name='admin'))
        return sm

    def __del__(self): # деструтор коммитит и закрывает sql
        # uncomment for auto logout of an account
        #sql_user_unlogined()

        if sql_is_admin_loggined() == True:
            sql_user_unlogined()
        
        conn.commit()
        cursor.close()

if __name__ == '__main__':
    sql_init(cursor)
    #Window.size = (400, 800)
    MyApp().run()