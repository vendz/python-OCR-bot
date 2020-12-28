#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import logging
import constants
import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    name = update.message.from_user.first_name
    update.message.reply_text('Hello! '+name)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("/start : to start the bot")
    update.message.reply_text("/donate : to donate to the developer")
    update.message.reply_text("or just send me an image to recognize text from it")

def donate(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /denate is issued."""
    update.message.reply_text('Donate!')


def convert_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    try:
        file_id = update.message.photo[-1].get_file()
        img_name = str(chat_id)+'.jpg'
        file_id.download(img_name)
        extracted_sting = (pytesseract.image_to_string(Image.open(img_name)))
        if extracted_sting:
            update.message.reply_text('`'+str(extracted_sting)+'`\n\nImage to Text Generated using @advancedocr_bot', reply_to_message_id = update.message.message_id)
        else:
            update.message.reply_text(constants.no_text_found)
    
    except Exception as e:
        update.message.reply_text("Error Occured: `"+str(e)+"`")
    
    finally:
        try:
            os.remove(img_name)
        except Exception:
            pass

def reply_to_text_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(constants.reply_to_text_message)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1494839456:AAGiJYauonFAt_728j-KFFQD2ACpN-35wLo", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("donate", donate))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_text_message))
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, convert_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
