import wget
import os
import tabula


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
		return None
	enr = newdf["Enr"]
	cap = newdf["Cap"]
	print(enr.item())
	print(cap.item())
	return enr.item(), cap.item()


if __name__ == "__main__":
	name = "GEOL 202"
	section = "1L"
	download()
	oldenr, oldcap = checkcapacity(name, section, "oldschedule.pdf")
	newenr, newcap = checkcapacity(name, section, "newschedule.pdf")
	if (oldenr != newenr):
		print("There is a change. Fast Register it")
	os.remove("oldschedule.pdf")
	os.rename("newschedule.pdf", "oldschedule.pdf")