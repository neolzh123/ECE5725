#!/usr/bin/env python
#coding=utf-8

import sqlite3
import subprocess
import logging
import random
import time
import os

 

class DB:

	''' DB 类 负责数据库操作'''
	db_name = "musicDB.db"
	def create_table(self):
		connection = sqlite3.connect(self.db_name)
		cursor = connection.cursor()
		sql_create = '''create table if not exists music
						(id integer primary key autoincrement,
						name text, url text)'''
		cursor.execute(sql_create)
		connection.commit()
		cursor.close()
		connection.close()
		return 0

	def insert(self, music_name, url):
		connection = sqlite3.connect(self.db_name)
		cursor = connection.cursor()
		sql_insert = 'insert into music(name, url) values ("%s","%s")'%(music_name, url)
		cursor.execute(sql_insert)
		connection.commit()
		cursor.close()
		connection.close()
		return 0

	def select(self, num):
		connection = sqlite3.connect(self.db_name)
		cursor = connection.cursor()
		sql_select = 'select url from music where id = %s'%(num)
		cursor.execute(sql_select)
		data = cursor.fetchall()
		cursor.close()
		connection.close()
		return data

	def getall(self):
		conn = sqlite3.connect(self.db_name)
		cursor = conn.cursor()
		sql_getall = 'select url from music'
		cursor.execute(sql_getall)
		data = cursor.fetchall()
		cursor.close()
		conn.close()
		return data

	def update(self, id):
		connection = sqlite3.connect(self.db_name)
		cursor = connection.cursor()
		sql_update = 'update music set status = "done" where id = %s'%id
		cursor.execute(sql_create)
		connection.commit()
		cursor.close()
		connection.close()
		return 0

class MusicPlay:
	'''音乐播放类，负责播放音乐，传入DB对象来操作数据库'''
	flag = False
	db = None
	def __init__(self,DB):
		global db
		db = DB
		if db is not None:
			self.files = db.getall()
			#print self.files
		else:
			self.files = []

	def play(self, url):
		cmd1 = 'mpg123 -C %s' % url
		self.p = subprocess.Popen(cmd1,shell=True)
		self.p.wait()

	# 播放所有音乐
	def playAll(self):
		global db
		self.files = db.getall()
		while True:			
			try:
				one = self.files[0]
			except:
				one = None
			os.system("")
			if one is not None:
				logging.info('>>>>> Now playing %s' % one)
			size = len(self.files)
			x = 0
			while True:
				self.play(self.files[x])
				x+=1
				if x == size-1: #播放结束后回到起点
					x = 0
			# for x in range(0,size):				
			# 	self.play(self.files[x])
				
			time.sleep(1)		


	def shuffle(self):
		size = len(self.files)
		r = random.randint(0, (size -1))
		self.play(self.files[r])


def initDB(db):

	db.create_table()
	# db.insert("lairifangchang","http://mr3.doubanio.com/2a15a1609f7fee2ca82d7374c66e9755/0/fm/song/p2675108_128k.mp3")
	# db.insert("bunan","http://mr3.doubanio.com/1a5e40fee0b4c308f8be6704f16bd69a/0/fm/song/p2238367_128k.mp3")
	# db.insert("lilian","http://mr1.doubanio.com/23bdfdbb55e16554de9873cd42fdf8a3/1/fm/song/p1629393_64k.mp3")
	# db.insert("banmabanma","http://mr1.doubanio.com/8c7a7235a3a79ffca9988b6a44fe90f1/1/fm/song/p1832370_64k.mp3")
	# db.insert("jigeni","http://mr3.doubanio.com/43dde534f99882896d433bb40582efb7/1/fm/song/p1821846_64k.mp3")
	# db.insert("shenshenaishangni","http://mr3.doubanio.com/b8c5326259059b9622175deb533d7dda/0/fm/song/p1393888_64k.mp3")
	# db.insert("sugar","http://mp3.shmidt.net/files_play/f1586fcfc0b0f8b91d6cf23bb283289b/mp3/M/Maroon5/Maroon_5_-_Sugar_mp3.shmidt.net.mp3")
	# db.insert("Maps","http://poponandon.com/wp-content/uploads/2014/06/01-Maps.mp3")
	# db.insert("Memory","http://mr1.doubanio.com/8f804fa037a2f823e8ed6500382c6ab1/0/fm/song/p971481_64k.mp3")

def main():

	db = DB()
	initDB(db) # run once
	player = MusicPlay(db)
	player.playAll()


if __name__ == '__main__':
	main()



