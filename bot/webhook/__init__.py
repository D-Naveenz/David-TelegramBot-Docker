import json
import socket
import traceback

from flask import Blueprint, request
from telegram import Update

from bot import app, config, logger, utils, telebot

blueprint = Blueprint('webhook', __name__)
ADMIN_LEVEL = 1  # 1=Channel admins + Owner, 2=Channel admins, 3=Owner only

# shortening variables of Config object
BOTNAME = config.BOTNAME
TOKEN = config.TOKEN
SOURCE_TOKEN = config.SOURCE_TOKEN
HOST = config.HOST
PORT = config.PORT
CERT = config.CERT
CERT_KEY = config.CERT_KEY
DISABLE_SSL = config.DISABLE_SSL
PERMANENT_CHATS = config.PERMANENT_CHATS
OWNER_ID = config.OWNER_ID


@blueprint.route('/')
def load():
    return "{} bot is here! :-)".format(BOTNAME)


@blueprint.route('/relay/{}'.format(SOURCE_TOKEN), methods=['POST'])
def relay():
    try:
        # retrieve the message in JSON and then transform it to Telegram object
        update = Update.de_json(request.get_json(force=True), telebot)

        chat_id = update.message.chat.id
        msg_id = update.message.message_id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        request_data = update.message.text.encode('utf-8').decode()
        # for debugging purposes
        logger.debug("request data: {}".format(request_data))
        parsed_json = json.loads(request_data, strict=False)
    except:
        traceback.print_exc()
        return "ERROR"
    utils.send_message(chat_id=chat_id, text=parsed_json['message'])
    return "OK", 200


@app.route('/relay/{}'.format(TOKEN), methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telebot)
    logger.debug("webhook update: {}".format(update))

    utils.set_update(update)
    # bot_dispatcher.process_update(update)
    return "OK"


@blueprint.route('/install')
def set_webhook():
    if DISABLE_SSL:
        cert = None
    else:
        cert = open(CERT, 'rb')

    # for debugging perpose
    logger.debug('webhook url is: https://%s:%s/relay/%s\ncrtificate: %s' % (HOST, PORT, TOKEN, cert))
    logger.debug('genarated FQDN: {} / hostname: {}'.format(socket.getfqdn(), socket.gethostname()))

    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    response = bot.set_webhook(url='https://%s:%s/relay/%s' % (HOST, PORT, TOKEN),
                               certificate=cert, timeout=20)
    if response:
        logger.debug("webhook setup succeeded!")
    else:
        logger.debug("webhook setup: failed!")


def has_permission():
    if ADMIN_LEVEL == 1:
        return utils.is_user_admin() or utils.is_chat_all_admins() or utils.matches_user_id(OWNER_ID)
    elif ADMIN_LEVEL == 2:
        return utils.is_user_admin() or utils.is_chat_all_admins()
    elif ADMIN_LEVEL == 3:
        return utils.matches_user_id(OWNER_ID)


def permission_denied():
    utils.send_message(chat_id=utils.get_chat().id,
                       reply_to_message_id=utils.get_message().message_id,
                       text="You're not my mom!")
