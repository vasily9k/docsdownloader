import telebot
import cfg
import urllib
import os
from telebot import types

bot = telebot.TeleBot(cfg.token)



'''#########################################################################
                        ANSWERS AND OTHER
#########################################################################'''


    ############# START COMMAND ################
@bot.message_handler(commands=['start'])
def start(message):
    hi_message = 'Hi '+ str(message.from_user.username) + "! \n \n This bot is downloading all files on my host computer. \n !important You need to send all files as files max file size = 20mb! or You\'ll be ignored . Nothing personal :). \n \nI hope you'll enjoy"
    bot.send_message(message.chat.id, hi_message)


    ############# HELP COMMAND ################
@bot.message_handler(commands=['help'])
def idk(message):
    bot.send_message(message.chat.id, 'Have a question or suggestions? - /start or write to this guy @tilliknow')


    ############# IF PHOTO ################
@bot.message_handler(content_types=['photo'])
def issue(message):
    bot.send_message(message.chat.id, 'Am i joke to you?')


############# NOT SUPPORTS ################
def wrong_extension(file_extension, message):
    wrong_message = 'Sorry but '+file_extension+' type file doesnt supports. Try other filetype'
    bot.send_message(message.chat.id, wrong_message)


############# TOO BIG ################
def toobig(message):
    bot.send_message(message.chat.id, 'File is too big :) There\'s no way')






'''#########################################################################
                            CHECK AND DOWNLOAD
#########################################################################'''


document_id = ''
mssg_id = ''
copy = 1
############# FILE CHECK ################
@bot.message_handler(content_types=["document"])
def handle_docs(message):
    DB(message)
    if message.document.file_size >= 20971520:                 #Is file too big?
        toobig(message)
    else:
        global document_id
        global mssg_id
        mssg_id = message.message_id
        document_id = message.document.file_id
        file_info = bot.get_file(document_id)
        useless, file_extension = os.path.splitext(file_info.file_path)
        if file_extension not in cfg.allowedfiles:            #Is file unsupported
            wrong_extension(file_extension, message)
        else:
            hope(message)                                              #User opinion


def hope(message):
    def areusure(message):
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Yes', callback_data='yes')
        keyboard.add(key_yes)
        key_no= types.InlineKeyboardButton(text='No', callback_data='no')
        keyboard.add(key_no)
        key_not_one= types.InlineKeyboardButton(text='Not one', callback_data='not_one')
        keyboard.add(key_not_one)
        global copy
        str4ka= 'Are you sure you want to print one ' + str(copy) + ' copy'
        bot.send_message(message.chat.id, text=str4ka, reply_markup=keyboard)
    def call():
        @bot.callback_query_handler(func=lambda call: True)
        def callback_worker(call):
            bot.delete_message(call.message.chat.id, call.message.message_id)
            if call.data == 'yes':
                download(call.message.chat.id)
            elif call.data == 'no':
                bot.send_message(call.message.chat.id, 'Ok then')
                pass
            elif call.data == 'not_one':
                bot.send_message(call.message.chat.id, 'And how much?')
                bot.register_next_step_handler(message, how_much)
                print('my v callback')
                pass
    areusure(message)
    call()


############# HOW MUCH ################
def how_much(message):
    print('my sprashivaem')
    global copy
    while copy == 1:
        try:
            copy = int(message.text)
            if copy > 20:
                bot.send_message(message.chat.id, 'Too much')
                copy = 1
        except Exception:
            bot.send_message(message.chat.id, 'Write in numbers please')
    hope(message)



############# DOWNLOAD ################
def download(userid):
    global document_id
    global mssg_id
    global copy
    file_info = bot.get_file(document_id)
    useless, file_extension = os.path.splitext(file_info.file_path)
    file_path = 'documents/' + str(copy) + '.' + str(userid) + '.' + str(mssg_id) + str(file_extension)
    print(file_path)
    link = 'https://api.telegram.org/file/bot' + cfg.token + '/' + str(file_info.file_path)
    urllib.request.urlretrieve(link, file_path)
    bot.send_message(userid, 'Success. You did it')
    copy = 1


############# LOG ################
def DB(message):
    log = open('DB.txt', 'a')
    newstr = str(message.from_user.id) + '  ' + str(message.message_id) + '  ' + '@' + str(message.from_user.username) +  '  ' + str(message.from_user.first_name) + '  ' + str(message.from_user.last_name)
    log.write(newstr+'\n')
    log.close()


bot.polling()
