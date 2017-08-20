#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import RegexHandler, ConversationHandler

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)


def start(bot, update):
    update.message.reply_text('Hi!' '你可以使用 /help 来获取所有指令。')

def hello(bot, update):
    update.message.reply_text('Hello, {}'.format(update.message.from_user.first_name))

def help(bot, update):
    update.message.reply_text('Help!' 
    '''
    /hello 向你问好
    /conv 开启一个交谈
    ''')

def echo(bot, update):
    update.message.reply_text('非常抱歉，我还不够聪明，听不懂你在说什么。你可以使用 /conv 来开启一个交谈。')

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))




# conversation start----------------------------------
GENDER, PHOTO, BIO = range(3)

def conv(bot, update):
    reply_keyboard = [['Boy', 'Girl', 'Other']]
    update.message.reply_text('Hi! My name is Find Fun Bot. I will hold a conversation with you.' 'Send /cancel to stop talking to me.\n\n' 'Are you a boy or a girl?', reply_markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard = True))
    return GENDER

def gender(bot, update):
    user = update.message.from_user
    logger.info("Gender of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('I see! Please send me a photo of yourself, ' 'so I know what you look like, or send /skip if you don\'t want to. ', reply_markup = ReplyKeyboardRemove())
    return PHOTO

def photo(bot, update):
    user = update.message.from_user
    photo_file = bot.get_file(update.message.photo[-1].file_id)
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s" % (user.first_name, 'user_photo.jpg'))
    update.message.reply_text('Gorgeous! Now, send me your bio please, ' 'or send /skip if you don\'t want to. ')
    return BIO

def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo." % user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your bio please.')
    return BIO

def bio(bot, update):
    user = update.message.from_user
    logger.info("Bio of %s: %s" % (user.first_name, update.message.text))
    update.message.reply_text('Thank you! I hope we can talk again some day.')
    return ConversationHandler.END

def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.', reply_markup = ReplyKeyboardRemove())
    return ConversationHandler.END
#conversation end----------------------------------




def main():
    updater = Updater("366339506:AAEYRx7lDHeCIgz37Luh4zOVBdvXnkBbRzk")
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("hello", hello))
    dp.add_handler(CommandHandler("help", help))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    # log all errors
    dp.add_error_handler(error)

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points = [CommandHandler('conv', conv)],
        states = {
            GENDER: [RegexHandler('^(Boy|Girl|Other)$', gender)],
            PHOTO: [MessageHandler(Filters.photo, photo),
                    CommandHandler('skip', skip_photo)],
            BIO: [MessageHandler(Filters.text, bio)]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    updater.idle()


if __name__ == '__main__':
    main()

