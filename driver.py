#!/usr/bin/env python3

from ideone import ideone_automation
from db_model import manage_db
import os
import time

usr = ideone_automation()
db = manage_db()

	
def header():
	print('''----------------------------------------------------\n
			----------------- Automated Ideone -----------------\n
			----------------------------------------------------\n''')
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
				return db.get_user_id([usr, pas])

def handle_code(code):
	clear()
	header()
	print(code)
	input("__ ")
	return

def search_code(log):
	clear()
	header()
	search_text = input("Search : ")
	search_result = db.search_a_code(log, search_text)
	while True:
		clear()
		header()
		for i in len(search_result):
			print(str(i+1)+'. ',end="")
			print(search_result[i])
		print(str(len(search_result)+1)+'. Back')
		print("----------------------------------------------------\n")
		
		choose = input("__ ")
		if choose == "" or int(choose) == len(search_result)+1:
			return
		choose = int(choose)
		handle_code(search_result[choose-1])

def add_new_codes(log):
	

def main():
	log = check_login()
	if log is None:
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

