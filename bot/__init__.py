from flask import Flask
from gunicorn.glogging import Logger

from bot import webhook
from bot.api_helper import TeleBot
from config import active_config_name, app_config, Config
from util import Utils

# Initialize globals
app: Flask
config: Config
logger: Logger
utils: Utils
telebot: TeleBot


def init(config_name=active_config_name()):
    global app, config, logger, utils, telebot

    config = Config()
    app = Flask(__name__)
    # app = Flask(__name__.split(".")[0])
    app.config.from_object(app_config[config_name])
    telebot = TeleBot(config.TOKEN)
    utils = Utils(telebot)
    # Create logger
    logger = config.create_logger(app)

    with app.app_context():
        register_extensions()
        register_blueprints()
        register_bot(config_name)

        # atexit.register(_handle_exit(app))

        return app


def register_bot(config_name):
    """
    app.bot_instance = HCaptchaBot(get_active_config().TELEGRAM_TOKEN, app)

    # Don't explicitly run the bot in testing env
    if config_name != "testing":
        app.bot_instance.setup()
        app.bot_instance.run()
    :param config_name:
    :return:
    """


def _handle_exit():
    """
        def hanlder():
        app.bot_instance.exit()

    return hanlder
    :return:
    """


def register_extensions():
    """
    db = SQLAlchemy()

    with app.app_context():
        db.init_app(app)
    :return:
    """


def register_blueprints():
    # app.register_blueprint(captcha.views.blueprint)
    app.register_blueprint(webhook.blueprint)



