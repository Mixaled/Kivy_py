import sqlite3

word_dict = {
    'дом': 'house', 'солнце': 'sun', 'книга': 'book', 'стол': 'table', 'яблоко': 'apple', 'дорога': 'road', 'гора': 'mountain', 'океан': 'ocean', 
    'глаз': 'eye', 'музыка': 'music', 'рука': 'hand', 'небо': 'sky', 'кофе': 'coffee', 'птица': 'bird', 'день': 'day', 'ночь': 'night', 'время': 'time', 
    'цветок': 'flower', 'человек': 'person', 'звезда': 'star', 'вода': 'water', 'земля': 'earth', 'ветер': 'wind', 'дождь': 'rain', 'огонь': 'fire', 
    'красный': 'red', 'жизнь': 'life', 'голова': 'head', 'рыба': 'fish', 'красивый': 'beautiful', 'дружба': 'friendship', 'работа': 'work', 
    'город': 'city', 'машина': 'car', 'телефон': 'phone', 'путешествие': 'journey', 'учеба': 'study', 'здоровье': 'health', 'еда': 'food', 'семья': 
    'family', 'любовь': 'love', 'игра': 'game', 'лето': 'summer', 'зима': 'winter', 'весна': 'spring', 'осень': 'autumn', 'пространство': 'space', 
    'кресло': 'chair', 'облако': 'cloud', 'зеркало': 'mirror'
}


conn = sqlite3.connect('data.db')
cursor = conn.cursor()


def commit_decorator(funct):
    def wrapper(*arg, **kwarg):
        result = funct(*arg, **kwarg)
        conn.commit()
        return result
    return wrapper

def sql_init(cursor):
    cursor.execute('''
    create table if not exists users (
        id seral,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        login integer default 0 
    )
''')
    cursor.execute('''
    create table if not exists words (
        id seral,
        rus TEXT NOT NULL,
        eng TEXT NOT NULL
    )
''')
    cursor.execute(f"insert or ignore into users (username, password) VALUES ('admin', 'admin')")
    for rus,eng in word_dict.items():
        cursor.execute(f"insert or ignore into words (rus, eng) VALUES ('{rus}', '{eng}')")

def sql_exist_user(username):
    cursor.execute(f"select 1 from users where username='{username}'")
    return cursor.fetchone() is not None

def sql_login_check(username, password):
    cursor.execute(f"select 1 from users where username='{username}' and password='{password}'")
    return cursor.fetchone() is not None

def sql_add_new_user(username, password):
    if not sql_exist_user(username):
        cursor.execute(f"insert into users (username, password) VALUES ('{username}', '{password}')")# hashing todo
        return True
    else:
        return False

@commit_decorator
def sql_user_logined(username):
    cursor.execute(f"update users set login=1 where username='{username}'")
    #conn.commit()

@commit_decorator
def sql_user_unlogined():
    cursor.execute(f"update users set login=0")
    #conn.commit()

def sql_return_username():
    try:
        text = cursor.execute(f"select username from users where login=1").fetchall()[0]
        return text
    except:
        return ''

def sql_dict_with_words():
    words = {}
    result = cursor.execute("select rus, eng from words").fetchall()
    for row in result:
        rus_word, eng_word = row
        words[rus_word] = eng_word
    return words

def sql_was_loggined():
    cursor.execute(f"select 1 from users where login=1")
    return cursor.fetchone() is not None

@commit_decorator
def sql_add_new_words(rus, eng):
    cursor.execute(f"insert or ignore into words (rus, eng) VALUES ('{rus.text}', '{eng.text}')")


def sql_is_admin_loggined():
    cursor.execute(f"select 1 from users where username='admin' and login=1")
    return cursor.fetchone() is not None