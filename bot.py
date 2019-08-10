from telegram.ext import Updater, InlineQueryHandler, \
    MessageHandler, CommandHandler
from telegram.ext.filters import Filters
import requests
import re
# from utils import *

import logging
import telegram

courseCode = None
courseSection = None

def start(bot, update):
    start_msg = """
    Hi! I am bot specifically designed to track enrolled capacity of courses!
	
	1) Just wrote me your course code with /set_coursecode 
	Like this:
	/set_coursecode MATH 161
	2) Add the section which you want to track
	Like this:
	/set_coursesection 1L
    """
    update.message.reply_text(start_msg)

def set_coursecode(bot, update):
	error_msg = """
	It seems you did not enter properly courseCode. Please try again!
	"""
	courseCode = update.message.text[16: ]
	print(courseCode)
	if (len(courseCode) != 8):
		update.message.reply_text(error_msg)

def set_coursesection(bot, update):
	error_msg = """
	It seems you did not enter properly courseSection. Please try again!
	"""
	courseSection = update.message.text[19:]
	if (len(courseSection)>3 or len(courseSection) < 2):
		updade.message.reply_text(error_msg)
	print(courseSection)


def main():
	updater = Updater(token='776447650:AAFsgQnnNAMJ4ng5KgyHhBE9qOYRVFCJMFA')
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('set_coursecode', set_coursecode))
	dispatcher.add_handler(CommandHandler('set_coursesection', set_coursesection))

	updater.start_polling()
	updater.idle	


if __name__ == '__main__':
    main()