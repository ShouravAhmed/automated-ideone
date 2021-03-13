import sqlite3
import time

class manage_db(object):
	def __init__(self):
		
		self.conn = sqlite3.connect("ideone_db.sqlite")
		self.cur = self.conn.cursor()
		
		self.cur.execute("select count(*) from sqlite_master where type='table' and name = 'user'")
		row = self.cur.fetchone()
		
		if row[0] == 0:
			self.cur.execute('''
				create table user (
					id integer not null primary key autoincrement unique,
					username text,
					password text,
					total_page_loaded integer
				);'''
			)

			self.cur.execute('''
				create table codes (
					id integer not null primary key autoincrement unique,
					link text,
					name text,
					lang text,
					submission_date text,
					tag text,
					user_id integer
				);'''
			)
			self.cur.execute('''
				create table current_user(id integer);'''
			)

	def insert_code(self, code, u_id):
		# prob_link, prob_tags, prob_name, prob_lang, prob_sub_date

		code[2] = code[2].replace('\t', ' ')

		self.cur.execute("select count(*) from codes where link = ?", (code[0], ))
		row = self.cur.fetchone()
		
		if row[0] == 0:

			self.cur.execute('''
				insert into codes (link, tag, name, lang, submission_date, user_id) 
				values(?, ?, ?, ?, ?, ?)''', 
				(str(code[0]), str(code[1]), str(code[2]), str(code[3]), str(code[4]), str(u_id),) 
			)

			print("saving code :", code[0])
			time.sleep(0.025)

			return 1
		else:
			print("\n\ncode already saved :", code, "\n\n")
			time.sleep(3)
			return 0


	def get_user_id(self, user):
		self.cur.execute("select id from user where username = ? and password = ?;",(user[0], user[1], ))
		row = self.cur.fetchone()
		if row is not None:
			return row[0]
		else:
			self.cur.execute('''
				insert into user (username, password, total_page_loaded)
					values (?, ?, ?);''',(user[0], user[1], 0))

			self.cur.execute("select id from user where username = ? and password = ?;",(user[0], user[1], ))
			row = self.cur.fetchone()
			
			self.conn.commit()
			return row[0]

	def update_total_page_loaded(self, page_cnt, id):
		self.cur.execute("update user set total_page_loaded = ? where id = ?;",(page_cnt, id, ))
		

	def get_codes(self, search_text, user_id):
		# condition = ""
		# condition_text = search_text.split()
		# for i in condition_text:
		# 	condition = condition + " or name like '%" + i + "%'"
		# condition = '('+condition[3:]+')'

		# print("select * from codes where (", condition, " and user_id = ", user_id, ");")

		search_text = search_text.split()

		self.cur.execute("select * from codes where user_id = ?;", (user_id, ))
		rows = self.cur.fetchall()

		ret = []

		for row in rows:
			flg = 0
			txt = row[2].lower()
			for i in search_text:
				if i in txt:
					flg = 1;
					break;
			if flg:
				ret.append([row[1], row[2], row[4], row[5], row[3]])
			# print(row)

		return ret


	def get_current_user(self):
		self.cur.execute("select id from current_user;")
		row = self.cur.fetchone()
		if row is not None:
			return row[0]
		else:
			return None

	def set_current_user(self, id):
		self.cur.execute("delete from current_user;")
		self.cur.execute("insert into current_user(id) values(?)",(id, ))
		self.conn.commit()

	def erase_current_user(self):
		self.cur.execute("delete from current_user")
		self.conn.commit()

	def username(self, id):
		self.cur.execute("select username from user where id = ?", (id, ))
		row = self.cur.fetchone()
		
		return row[0]

	def password(self, id):
		self.cur.execute("select password from user where id = ?", (id, ))
		row = self.cur.fetchone()
		
		return row[0]

# ----------------------------------------------------------------------------------------------
	
