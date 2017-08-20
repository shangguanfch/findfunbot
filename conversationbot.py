#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Simple Bot to reply to Telegram messages
"""
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler
import logging

# Enable logging
logging.basicConfig(format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s', level = logging.INFO)
logger = logging.getLogger(__name__)


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
    update.message.reply_text('Gorgeous! Now, send me your location please, ' 'or send /skip if you don\'t want to. ')
    return BIO

def skip_photo(bot, update):
    user = update.message.from_user
    logger.info("User %s did not send a photo." % user.first_name)
    update.message.reply_text('I bet you look great! Now, send me your location please, ' 'or send /skip.')
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

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater("366339506:AAEYRx7lDHeCIgz37Luh4zOVBdvXnkBbRzk")
    dp = updater.dispatcher

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
    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    updater.idle()


if __name__ == '__main__':
    main()
