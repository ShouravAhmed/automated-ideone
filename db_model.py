import sqlite3

class manage_db(object):
	def __init__(self):
		self.conn = sqlite3.connect("ideone_db.sqlite")
		self.cur = self.conn.cursor()
		self.cur.execute("select count(*) from sqlite_master where type='table' and name = 'user'")
		row = self.cur.fetchone()
		if row[0] == 0:
			self.cur.execute('''
				create table user (
					id int(6) not null auto increment,
					username varchar(50) not null,
					password varchar(50) not null,
					total_page_loaded int(3) not null,
					primary key(id)
				);'''
			)
			self.cur.execute('''
				create table tags (
					id int(3) not null auto increment,
					name varchar(50) not null,
					primary key(id)
				);'''
			)
			self.cur.execute('''
				create table codes (
					id int(20) not null auto increment,
					link varchar(10) not null,
					name varchar(50) not null,
					lang varchar(50) not null,
					submission_date date,
					user_id int(6) referance user(id),
					primary key(id)
				);'''
			)
			self.cur.execute('''
				create table codes_tag (
					code_id int(20) referance codes(id),
					tag_id int(3) referance tags(id),
					primary key(code_id, tag_id)					
				);'''
			)
			self.cur.execute('create table current_user(id int(6) not null);')

	def insert_code(self, code, tag, u_id):
		self.cur.execute("select count(*) from code where link = code[0]")
		row = self.cur.fetchone()
		if row[0] == 0:
			self.cur.execute('''
				insert into code (link, name, lang, date, user_id)
					values(code[0], code[1], code[2], code[3], u_id);'''
			)
			self.cur.execute("select id from code where link = code[0];")
			row = self.cur.fetchone()
			c_id = row[0]

			for i in tag:
				self.cur.execute('''
					insert into codes_tag (code_id, tag_id)
						values(c_id, u_id);'''
				)	
			return 0
		else:
			return 1

	def get_user_id(self, user):
		self.cur.execute("select id from user where username=user[0] and password=user[1];")
		row = self.cur.fetchone()
		if row is not None:
			return row[0]
		else:
			self.cur.execute('''
				insert into user (username, password, total_page_loaded)
					values (user[0], user[1], 0);'''
			)
			self.cur.execute("select id from user where username=user[0] and password=user[1];")
			row = self.cur.fetchone()
			return row[0]

	def update_total_page_loaded(self, user):
		self.cur.execute("update user set total_page_loaded = user[1] where id = user[0];")


	def search_a_code(self, user_id, search_text):
		condition = ""
		search_text = search_text.split()
		for i in search_text:
			condition = condition + "or name like '%" + i + "%'"
		condition = '('+condition[2:]+')'

		self.cur.execute(''' select link, name, lang, date from codes where ? and user_id = ? ;''',(condition, user_id, ))
		return self.cur.fetchall()

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

	def erase_current_user(self):
		self.cur.execute("delete from current_user;")

# ----------------------------------------------------------------------------------------------
	
