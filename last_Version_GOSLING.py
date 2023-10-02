import telebot
from telebot import types
import pickle
import os
from setting import TG_TOKEN

bot = telebot.TeleBot(TG_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    question_index = 0
    score = {'Driver': 0, 'Ken': 0, 'Blade': 0, 'SOSNA': 0, 'JazzMan': 0, 'Alpha': 0, 'Noy': 0, 'Lars': 0, 'index': 0}
    save_user_data(message.chat.id, score)
    bot.send_message(message.chat.id,'Приветсвую, это телеграм бот с тестами.')
    bot.send_message(message.chat.id, 'Выбери какой тест хочешь пройти во вкладке Menu.')



def load_hero_data():
    """
    The function opens a file that contains a scoring table.
    """
    global user_data
    if not os.path.isfile('.pickle'):
        with open('.pickleGOS.pkl', 'rb') as handle:
            user_data = pickle.load(handle)
            return user_data



def save_user_data(user_id: int, score):
    '''
    The function collects one from two dictionaries.
    Unloads data from the pickle file, adds new data, and saves it to the pickle file.
    '''

    with open('.pickle.pkl', 'rb') as handle:
        data = pickle.load(handle)
    if user_id not in data:
        user_data = {user_id: score}
        newDATA = user_data | data
        print(newDATA)

    else:
        data[user_id] = score
        newDATA = data
        print(newDATA)
    with open('.pickle.pkl', 'wb') as handle:
        pickle.dump(newDATA, handle, protocol=pickle.HIGHEST_PROTOCOL)



def load_user_data():
    """
    Function to load data from a .pickle file into memory.
    """
    global user_data
    if not os.path.isfile('.pickle'):
        with open('.pickle.pkl', 'rb') as handle:
            user_data = pickle.load(handle)
            return user_data


def answer_qustion():  # Чтение листа с вопросами по Python
    '''
    The function reads a txt file with questions
    '''
    quest = []
    with open('question.txt', 'r', encoding='utf-8') as file:
        for line in file:
            if line != '\n':
                quest += [line.strip()]
        return quest



@bot.message_handler(commands=['gosling'])
def send_question(message):
    '''Running the test'''

    chat_id = message.chat.id
    process = load_user_data()
    process = process[chat_id]

    process['index'] += 1

    if process['index'] == 34:   # The test has 34 questions.
        send_gif(chat_id)
        return


    save_user_data(message.chat.id, process)
    keyboard(message, chat_id, process)




def keyboard(message, chat_id, process):
    '''
    Reply buttons, for the user
    '''

    process = process['index']

    question = answer_qustion()
    sendQUEST = question[process]

    keyboard = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton(text=str("His literally me"), callback_data='0')
    button2 = types.InlineKeyboardButton(text=str("Возможно"), callback_data='1')
    button3 = types.InlineKeyboardButton(text=str("Скорее нет"), callback_data='2')
    button4 = types.InlineKeyboardButton(text=str("Нет"), callback_data='3')

    keyboard.add(button1, button2, button3, button4)
    bot.send_message(chat_id=message.chat.id, text=sendQUEST, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    '''
    Handler for callback requests from the user.
    '''

    user_id = call.from_user.id

    DATS = load_hero_data()
    ind = 0


    if call.data == '0':
        ind = 0
    if call.data == '1':
        ind = 1
    if call.data == '2':
        ind = 2
    if call.data == '3':
        ind = 3

    '''
    In the loop, for each hero from DATS a score is calculated and added to the user’s score
    '''

    a = load_user_data()
    userSCORE = a[user_id]
    NUM = userSCORE['index']
    for y in DATS:        # in a loop, for each hero from DATS the point score is calculated
        hero = DATS[y]
        score = hero[NUM][ind]
        userSCORE[y] += int(score)

    save_user_data(user_id, userSCORE)

    bot.answer_callback_query(callback_query_id=call.id, text='GOOD')
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    send_question(call.message)


def send_gif(chat_id):
    '''
    The function sends a GIF image depending on the points scored
    '''
    user = load_user_data()
    user = user[chat_id]
    name = max(user, key=user.get)


    gif_blade = 'gif/blade.gif'
    gif_Drive = 'gif/Drave.gif'
    gif_hot = 'gif/hot-ryan-gosling.gif'
    gif_ken = 'gif/ken.gif'
    gif_jazz = 'gif/la.gif'
    gif_lars = 'gif/lars.gif'
    gif_remember = 'gif/remember.gif'
    gif_sosna = 'gif/sosna.gif'

    if name == 'Driver':
        gif = open(gif_Drive, 'rb')
        bot.send_document(chat_id, gif)
        print('drive')
    if name == 'Ken':
        gif = open(gif_ken, 'rb')
        bot.send_document(chat_id, gif)
        print('ken')
    if name == 'Blade':
        gif = open(gif_blade, 'rb')
        bot.send_document(chat_id, gif)
        print('blade')
    if name == 'SOSNA':
        gif = open(gif_sosna, 'rb')
        bot.send_document(chat_id, gif)
        print('sosna')
    if name == 'JazzMan':
        gif = open(gif_jazz, 'rb')
        bot.send_document(chat_id, gif)
        print('JazzMan')
    if name == 'Alpha':
        gif = open(gif_hot, 'rb')
        bot.send_document(chat_id, gif)
        print('Alpha')
    if name == 'Noy':
        gif = open(gif_remember, 'rb')
        bot.send_document(chat_id, gif)
        print('Nuy')
    if name == 'Lars':
        gif = open(gif_lars, 'rb')
        bot.send_document(chat_id, gif)
        print('lars')


bot.infinity_polling()