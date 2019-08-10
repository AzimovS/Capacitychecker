import wget
import os
import tabula
import sqlite3

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



if __name__ == "__main__":
	download()
	lsts = read_db()
	for lst in lsts:
		name = lst[0][:8]
		section = lst[0][9:]
		print(name , section)
		oldenr, oldcap = checkcapacity(name, section, "oldschedule.pdf")
		newenr, newcap = checkcapacity(name, section, "newschedule.pdf")
		if (oldenr != newenr):
			print("There is a change. Fast Register it")
	os.remove("oldschedule.pdf")
	os.rename("newschedule.pdf", "oldschedule.pdf")