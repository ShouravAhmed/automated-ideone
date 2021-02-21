#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import pathlib
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



#------------------------------------------------------------------------------------------------

class ideone_automation(object):

	def __init__(self):

		user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"

		self.__options = webdriver.ChromeOptions()
		self.__options.headless = True
		self.__options.add_argument(f'user-agent={user_agent}')
		self.__options.add_argument("--window-size=1920,1080")
		self.__options.add_argument('--ignore-certificate-errors')
		self.__options.add_argument('--allow-running-insecure-content')
		self.__options.add_argument("--disable-extensions")
		self.__options.add_argument("--proxy-server='direct://'")
		self.__options.add_argument("--proxy-bypass-list=*")
		self.__options.add_argument("--start-maximized")
		self.__options.add_argument('--disable-gpu')
		self.__options.add_argument('--disable-dev-shm-usage')
		self.__options.add_argument('--no-sandbox')

		self.__dir_path = str(pathlib.Path().absolute())
		self.__chrome_driver = self.__dir_path + '/chromedriver'
		self.__driver = None
	
		self.__home_page = "https://ideone.com/"
		self.__login_page = self.__home_page + "account/login/"

	# -----------------------------------------------------------------------------------------------------------------
	# add new codes 
	def __ideone_login(self):
		usr = self.__driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/form/div[1]/div/div/input")
		usr.send_keys(self.__usrn)

		pas = self.__driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/form/div[2]/div/div/input")
		pas.send_keys(self.__pasw)

		lgn = self.__driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div/div/form/div[3]/div/button")
		lgn.send_keys(Keys.RETURN)
		os.system("clear")
		print(".\n.\n.\n.\n.\nloged in !!")

		myrec = self.__driver.find_element_by_xpath("/html/body/div[1]/div[1]/div/div/div/ul/li[2]/a")
		myrec.click()
		os.system("clear")
		print(".\n.\n.\n.\n.\nopening my codes.")

		lim = self.__driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/button")
		lim.click()
		lim = self.__driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[2]/ul/li[3]/a")
		lim.click()

		time.sleep(10)
		#self.__driver.implicitly_wait(120)

		os.system("clear")
		print(".\n.\n.\n.\n.\npage limit 100 selected.")
		time.sleep(1)


	def __get_data(self, page_no):
		page = self.__driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div/button")
		page.click()

		path = "/html/body/div[1]/div[3]/div[1]/div[2]/div[2]/div[1]/div[1]/div/ul/li["+page_no+"]/a"
		page = self.__driver.find_element_by_xpath(path)
		page.click()

		os.system("clear")
		print(".\n.\n.\n.\n.\nprocessing page",page_no,".....")
		
		time.sleep(10)
		#self.__driver.implicitly_wait(120)

		soup = BeautifulSoup(self.__driver.page_source, "lxml")
		return self.__process_data(soup)
		input("__ ")

	def __page_count(self):
		soup = BeautifulSoup(self.__driver.page_source, 'lxml')
		ul = soup.find_all('ul', {'class':'dropdown-menu'})
		soup = BeautifulSoup(str(ul[1]), 'lxml')
		li = soup.find_all('li')
		return len(li)

	def __process_data(self, soup):
		prob_info = soup.find_all('tr', {'class':'chk'})
		
		for tr in prob_info:
			prob_link = tr.find('a', {'class':'link'})
			prob_link = prob_link.text.strip()

			prob_tags = tr.find_all('a', {'class':'tag'})
			prob_tags = [x.text.strip() for x in prob_tags]

			prob_name = tr.find('span', {'class':'note_label'})
			prob_name = prob_name.text.strip()

			prob_lang = tr.find('span', {'class':'rel-tooltip'})
			prob_lang = prob_lang.text.strip()

			prob_sub_date = tr.find_all('a', {'href':'/'+str(prob_link)})
			prob_sub_date = prob_sub_date[1].get('title').strip()

			ls = [prob_link, prob_tags, prob_name, prob_lang, prob_sub_date]
			if ls[0] not in self.__codeset:
				self.__codes.append(ls)
			else:
				return False
		return True

	def add_new_codes(self):
		self.__driver = webdriver.Chrome(executable_path=self.__chrome_driver, options=self.__options)

		try:
			self.__driver.get(self.__login_page)
			self.__ideone_login()

			total_page = self.__page_count()

			for page_no in range(1, 101):
				if not self.__get_data(str(page_no)):
					os.system("clear")		
					print(".\n.\n.\n.\n.\npage",page_no,"was previously processed.")
					time.sleep(2)
					break
		except:
			ok = 1
		
		self.__driver.close()
		self.__save_data()	

		os.system("clear")
		print(".\n.\n.\n.\n.\nAll data processed!!")
		time.sleep(2)

	# -----------------------------------------------------------------------------------------------------------------

	#------------------------------------------------------------------------------------------------------------------
	# code download

	def __file_entension(self, lang):
		if 'py' in lang:
			return '.py'
		elif 'c' in lang or 'C' in lang:
			return '.cpp'
		elif lang == 'bash':
			return '.sh'
		elif lang == 'java':
			return '.java'

	def download(self, link, name, lang):
		self.__driver = webdriver.Chrome(executable_path=self.__chrome_driver, options=self.__options)

		self.__driver.get(self.__home_page+link)
		soup = BeautifulSoup(self.__driver.page_source, "lxml")
		self.__driver.close()

		data = soup.find('pre', {'class':'source', 'id':'source'})
		data = data.find('ol')
		data = data.find_all('li')
		data = [x.text for x in data]

		with open(self.__dir_path+"/downloads/"+name+self.__file_entension(lang), 'w') as f:
			for i in data:
				f.write(i)
				f.write("\n")
	#------------------------------------------------------------------------------------------------------------------
	

#------------------------------------------------------------------------------------------------



