#!/usr/bin/env python3

from ideone import ideone_automation
from db_model import manage_db
import os
import time
import webbrowser


usr = ideone_automation()
db = manage_db()

home_page = "https://ideone.com/"

def header():
	print("----------------------------------------------------\n")
	print("----------------- Automated Ideone -----------------\n")
	print("----------------------------------------------------\n")

def clear():
	os.system("clear")

def check_login():
	cu = db.get_current_user()
	if cu is not None:
		return cu;
	else:
		while True:
			clear()
			header()
			print("1. Login\n2. Back")
			print("----------------------------------------------------\n")
			choose = input("__ ")
			if choose == "" or int(choose) == 2:
				return None
			else:
				clear()
				header()
				print("Please provide correct Username and Password")
				print("----------------------------------------------------\n")
				usr = input("Username : ")
				pas = input("Password : ")
				id = db.get_user_id([usr, pas])
				db.set_current_user(id)
				return id

def handle_code(code):
	clear()
	header()
	print("Name: ", code[1])
	print("Tag:  ", code[3])
	print("Date: ", code[2].split()[0])
	print("----------------------------------------------------\n")

	print("1. Download the Code")
	print("2. Open in Browser")
	print("3. Submit in vjudge")
	print("4. Back")
	print("----------------------------------------------------\n")

	choose = input("__ ")
	try:
		if choose == "" or int(choose) == 4:
			return
		choose = int(choose)
	except:
		return

	if choose == 2:
		webbrowser.open(home_page+code[0])
	elif choose == 1:
		try:
			usr.download(code[0], code[1], code[4])
			clear()
			header()
			print("----------------------------------------------------\n")
			print("Code saved in:", usr.current_dir()+"/downloads/\n")
			print("----------------------------------------------------\n")
			input(".\n.\npress enter to continue _ ")
		except:
			clear()
			header()
			print("----------------------------------------------------\n")
			print("Error occured!! please try again.")
			print("----------------------------------------------------\n")
			input(".\n.\npress enter to continue _ ")
	elif choose == 3:
		webbrowser.open(home_page+code[0])
		webbrowser.open("https://www.google.com/search?q=vjudge+"+code[1].replace(' ','+'))

	handle_code(code)


def search_code(user_id):
	clear()
	header()
	search_text = input("Search : ")
	search_result = db.get_codes(search_text, user_id)

	while True:
		clear()
		header()

		a = len(str(len(search_result) + 1)) + 2;
		b = 0
		c = 0

		for i in range(len(search_result)):
			b = max(b, len(search_result[i][3]) + 1)
			c = max(c, len(search_result[i][1]) + 1)

		for i in range(len(search_result)):
			p1 = str(i+1)+'.';
			p2 = search_result[i][3]
			p3 = search_result[i][1]
			p4 = search_result[i][2]

			print(p1, end = "")
			for j in range(a-len(p1)):
				print(" ", end="")

			print(p2, end = "")
			for j in range(b-len(p2)):
				print(" ", end="")

			print(p3, end = "")
			for j in range(c-len(p3)):
				print(" ", end="")

			print(p4)

		print("----------------------------------------------------")
		print(str(len(search_result)+1)+'. Back')
		print("----------------------------------------------------\n")

		choose = input("__ ")
		if choose == "" or int(choose) == len(search_result)+1:
			return
		choose = int(choose)
		handle_code(search_result[choose-1])

def add_new_codes(log):
	try:
		usr.add_new_codes(log, db)
	except:
		clear()
		header()
		print("----------------------------------------------------\n")
		print("Error occured!! please try again.")
		print("----------------------------------------------------\n")
		input(".\n.\npress enter to continue _ ")

def main():

	log = check_login()
	if log is None:
		clear()
		return

	while True:
		clear()
		header()
		print("1. Search Code\n2. Add New Codes\n3. Logout\n4. Back")
		print("----------------------------------------------------\n")
		choose = input("__ ")
		if choose == "" or int(choose) == 4:
			clear()
			return
		choose = int(choose)

		if choose == 1:
			search_code(log)
		elif choose == 2:
			add_new_codes(log)
		else:
			db.erase_current_user()
			clear()
			return





if __name__ == "__main__":
	main()

