from telegram.ext import Updater, InlineQueryHandler, \
    MessageHandler, CommandHandler
from telegram.ext.filters import Filters
import requests
import re
# from utils import *
import urllib
import logging
import telegram
import wget
import os
import tabula
import sqlite3
import threading
from dbhelper import DBHelper

TOKEN = "776447650:AAFsgQnnNAMJ4ng5KgyHhBE9qOYRVFCJMFA"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

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

def download():
	url = "http://registrar.nu.edu.kz/registrar_downloads/json?method=printDocument&name=school_schedule_by_term&termid=421&schoolid=11"
	filename = wget.download(url)
	print("newschedule was downloaded")
	os.rename("school_schedule_by_term.pdf", "newschedule.pdf")

def checkcapacity(name, section, schedule):
	df = tabula.read_pdf(schedule, pages = "all")
	newdf = df.loc[df["Course Abbr"] == name]
	if newdf.size == 0:
		print("Course was not found")
	newdf =  newdf.loc[newdf["S/T"] == section]
	if newdf.size == 0:
		print("SECTION was not found")
		return None, None
	enr = newdf["Enr"]
	cap = newdf["Cap"]
	print(enr.item(), cap.item())
	return enr.item(), cap.item()

def read_db():
	conn=sqlite3.connect('todo.sqlite')
	cursor = conn.cursor()
	cursor.execute("SELECT * FROM items")
	rows = cursor.fetchall()
	lst = []
	for row in rows:
		lst.append(list(row))
	return lst

def send_message(chat_id, coursecode, oldcap, newcap):
	text = "There is a change in " + coursecode + "!!!\n"
	text += "It changed from " + str(oldcap) + " to " + str(newcap) + "!!!"
	text = urllib.parse.quote_plus(text)
	url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
	get_url(url)


def main():
	updater = Updater(token='776447650:AAFsgQnnNAMJ4ng5KgyHhBE9qOYRVFCJMFA')
	dispatcher = updater.dispatcher
	dispatcher.add_handler(CommandHandler('start', start))
	dispatcher.add_handler(CommandHandler('set_coursecode', set_coursecode))
	dispatcher.add_handler(CommandHandler('get_list', get_list))
	dispatcher.add_handler(CommandHandler('delete', delete))
	dispatcher.add_handler(CommandHandler('help', help))
	while True:
		download()
		lsts = read_db()
		for lst in lsts:
			name = lst[0][:8]
			section = lst[0][9:]
			print(name , section)
			oldenr, oldcap = checkcapacity(name, section, "oldschedule.pdf")
			newenr, newcap = checkcapacity(name, section, "newschedule.pdf")
			if (oldenr != newenr):
				send_message(lst[1], coursecode, oldcap, newcap)
				print("There is a change. Fast Register it")
	updater.start_polling()
	updater.idle	


if __name__ == '__main__':
	main()