from telegram.ext import Updater, InlineQueryHandler, \
    MessageHandler, CommandHandler
from telegram.ext.filters import Filters
import requests
import re
# from utils import *

import logging
import telegram

from dbhelper import DBHelper

def start(bot, update):
	start_msg = """
	Hi! I am bot specifically designed to track enrolled capacity of courses!

	Just wrote me your course code with /set_coursecode  
	Like this:
	/set_coursecode MATH 161 1L

	Write /help for more information
	"""
	update.message.reply_text(start_msg)

def help(bot, update):
	msg = """
	/set_coursecode - to add the course you to track
	Like this:
	/set_coursecode MATH 161 1L

	/get_list - to get the list of courses you are tracking

	/delete - to delete the course from your list
	Like this:
	/delete MATH 161 1L

	"""
	update.message.reply_text(msg)

def set_coursecode(bot, update):
	db = DBHelper()
	db.setup()
	error_msg = """
	It seems you did not enter properly courseCode. Please try again!
	"""
	courseCode = update.message.text[16: ]
	if (len(courseCode) < 11 or (len(courseCode) > 22)):
		update.message.reply_text(error_msg)
		return None
	chat = update.message.chat_id
	db.add_item(courseCode, chat)
	update.message.reply_text("Great, I added this course to list. To see the full list enter /get_list")

def get_list(bot, update):
	db = DBHelper()
	db.setup()
	chat = update.message.chat_id
	items = db.get_items(chat)
	message = "\n".join(items)
	update.message.reply_text(message)

def delete(bot, update):
	db = DBHelper()
	db.setup()
	chat = update.message.chat_id
	courseCode = update.message.text[8: ]
	db.delete_item(courseCode, chat)
	update.message.reply_text("I deleted " + courseCode + " from the list")


def main():
	updater = Updater(token='776447650:AAFsgQnnNAMJ4ng5KgyHhBE9qOYRVFCJMFA')
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('set_coursecode', set_coursecode))
	dispatcher.add_handler(CommandHandler('get_list', get_list))
	dispatcher.add_handler(CommandHandler('delete', delete))
	dispatcher.add_handler(CommandHandler('help', help))

	updater.start_polling(0.5)
	updater.idle	


if __name__ == '__main__':
	main()