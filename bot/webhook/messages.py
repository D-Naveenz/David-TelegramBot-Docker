from bot.webhook import utils
from bot import telebot


@telebot.message_handler(commands=['start'])
def start(message):
    # bot.reply_to(message, 'Hello, ' + message.from_user.first_name)
    utils.send_message(chat_id=utils.get_chat().id,
                       text="Unregistered <code>{}</code>. Bye!".format(utils.get_chat().title))

