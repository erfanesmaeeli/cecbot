# Developed by Erfan Esmaeeli Shirazi
# erffan.com

import telebot
import logging
from telebot import types
import re
from persiantools.jdatetime import JalaliDate
import time

TOKEN = 'put your token here'  # T.me/BotFather

bot = telebot.TeleBot(TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

ADMINS = [admin_telegram_unique_id]
user_dict = {}
class User:
	def __init__(self, fname):
		self.fname = fname
		self.lname = None
		self.phone = None
		self.gender = None
		self.gender_emoji = None
		self.sn = None
		self.join = None
		self.user_fname = None
		self.user_lname = None
		self.user_username = None
		self.user_id = None

def id_is_exist(user_id):
	with open("signup.txt" ,"r" , encoding="utf-8") as openfile:
		for line in openfile:
			for part in line.split():
				if "id=" in part:
					if part[3:] == str(user_id) and int(part[3:]) not in ADMINS:
						return True
	return False

def return_line_id(user_id):
	with open("signup.txt" ,"r" , encoding="utf-8") as openfile:
		for line in openfile:
			for part in line.split():
				if "id=" in part:
					if part[3:] == str(user_id):
						return line

def return_line_join(user_join):
	c = 0
	with open("signup.txt" ,"r" , encoding="utf-8") as openfile:
		list = []
		for line in openfile:
			for part in line.split():
				if "join_uni=" in part:
					if part[9:] == str(user_join):
						list.append(line)
						c += 1
		if c != 0:				
			return 0	
		else:
			return -1			

def user_line_by_join(user_join):
	list = []
	list = return_line_join(user_join)
	my_list = []
	fname = None
	lname = None
	join_uni = None
	phone = None
	gender = None
	sn = None
	my_list_string = None
	

	for line in list:
		for x in line.split():
			if "gender" in x:
				gender = "📍 جنسیت: " + x[7:]

			if "fname" in x:
				if gender == 'آقا':
					gender_emoji = "👨🏻‍💼"
				else:
					gender_emoji = "👩🏻‍💼"	
				fname = gender_emoji + "نام: " + x[6:]

			if "lname" in x:
				lname = gender_emoji + "نام خانوادگی: " + x[6:]
				
			if "join_uni" in x:
				join_uni = "👥 ورودی: " + x[9:]

			if "phone" in x:
				phone = "📞 تلفن همراه: " + x[6:]

			if "sn" in x:
				sn = "🔗 شماره دانشجویی: " + x[3:]
				
		my_list_string = f"{fname}\n\n{lname}\n\n{join_uni}\n\n{phone}\n\n{gender}\n\n{sn}"
		my_list.append(my_list_string)

	return my_list

	
def user_line(user_id):						
	line = return_line_id(user_id)
	list = []
	for x in line.split():
		gender = ""
		if "gender" in x:
			gender = x[7:]	
		if "fname" in x:	
			fname = "😶" + "نام: " + x[6:]
			list.append(fname)

	for x in line.split():
		if "lname" in x:
			lname = "😶" + "نام خانوادگی: " + x[6:]
			list.append(lname)

	for x in line.split():
		if "hbd" in x:
			hbd = "🎉 تاریخ تولد: " + x[4:]
			list.append(join_uni)
	
	return list											


# @bot.message_handler(commands=['end'])
# def end(message):
# 	send_welcome(message)

@bot.message_handler(commands=['start'])
def send_welcome(message):
	user_id = message.from_user.id
	if message.chat.type == 'private':
		if user_id in ADMINS:
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton('🔸 ثبت نام در انجمن 🔸')
			item2 = types.KeyboardButton('🔍 مشاهده لیست ثبت نام ها')


			keyboard.row(item1)
			keyboard.row(item2)

			user_fname = message.from_user.first_name
			welcome_text = f"💫 سلام عرفان عزیز\n\n🔰 شما با موفقیت وارد بخش مدیریت شده اید"
			msg = bot.send_message(message.chat.id,welcome_text, reply_markup=keyboard)
			bot.register_next_step_handler(msg, start_check)
		else:
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton('🔸 ثبت نام در انجمن 🔸')
			item2 = types.KeyboardButton('🔹کانال تلگرام')
			item3 = types.KeyboardButton('🔹اینستاگرام')
			item4 = types.KeyboardButton('🎥 آپارات')
			item5 = types.KeyboardButton('👨‍💻 پشتیبانی')
			item6 = types.KeyboardButton('وب سایت 🖥')


			keyboard.row(item1)
			keyboard.row(item2 , item3 , item4)
			keyboard.row(item6, item5)

			user_fname = message.from_user.first_name
			welcome_text = f"⭐ سلام {user_fname} عزیز\n\nبه ربات انجمن علمی مهندسی کامپیوتر دانشگاه آزاد کرج خوش اومدی 🌷"
			msg = bot.send_message(message.chat.id,welcome_text, reply_markup=keyboard)
			bot.register_next_step_handler(msg, start_check)


def start_check(message):
	check = message.text
	user_id = message.from_user.id
	if user_id in ADMINS and check == '🔍 مشاهده لیست ثبت نام ها':
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

			item1 = types.KeyboardButton('جدیدترین ها')
			item2 = types.KeyboardButton('شماره دانشجویی')
			item3 = types.KeyboardButton('سال ورودی')
			item4 = types.KeyboardButton('آیدی تلگرام')
			item5 = types.KeyboardButton('نام خانوادگی')
			item6 = types.KeyboardButton('نام')
			item7 = types.KeyboardButton('جنسیت')

			keyboard.row(item1)
			keyboard.row(item2 , item3)
			keyboard.row(item4 , item5 , item6)
			keyboard.row(item7)

			msg = bot.send_message(message.chat.id , "جست و جو بر اساس ..." , reply_markup = keyboard)
			bot.register_next_step_handler(msg, start_search)

	elif user_id in ADMINS or check == '🔸 ثبت نام در انجمن 🔸':
		user_id = message.from_user.id
		if id_is_exist(user_id):
			my_string = ""
			list = user_line(user_id)
			for i in list:
				my_string += f"{i}\n\n"
			msg2 = bot.send_message(message.chat.id, "🎁شما قبلا در انجمن ثبت نام کرده اید"+"\n\n📑 اطلاعات شما:\n\n" + my_string)
			bot.register_next_step_handler(msg2, start_check)
		else:	
			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton('↪️ مرحله قبل')
			item2 = types.KeyboardButton('🔺 خروج')

			keyboard.row(item2 , item1)

			msg = bot.send_message(message.chat.id, "شما با موفقیت وارد صفحه ی ثبت نام شده اید ✅ \n\nنام خود را بصورت فارسی وارد نمایید 📝",reply_markup=keyboard)
			bot.register_next_step_handler(msg, signup_fname)

	elif check == '🔹کانال تلگرام':
		msg = bot.send_message(message.chat.id, "telegram.me/CECkiau")
		bot.register_next_step_handler(msg, start_check)

	elif check == '🔹اینستاگرام':
		msg = bot.send_message(message.chat.id, "instagram.com/CECkiau")
		bot.register_next_step_handler(msg, start_check)

	elif check == '🎥 آپارات':
		msg = bot.send_message(message.chat.id, "aparat.ir/CECkiau")
		bot.register_next_step_handler(msg, start_check)

	elif check == '👨‍💻 پشتیبانی 24 ساعته':
		msg = bot.send_message(message.chat.id, "telegram.me/CEC_Online")
		bot.register_next_step_handler(msg, start_check)

	elif check == 'وب سایت 🖥':
		msg = bot.send_message(message.chat.id, "https://ceckiau.ir")
		bot.register_next_step_handler(msg, start_check)
		
	elif check =="/start":
		send_welcome(message)

	elif check =="/end":
		send_welcome(message)
	else:
		msg = bot.reply_to(message, "📛 دستور وارد شده صحیح نمی باشد")
		bot.register_next_step_handler(msg, start_check)


def start_search(message):
	input = message.text
	if input == 'سال ورودی':
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

		item1 = types.KeyboardButton('98')
		item2 = types.KeyboardButton('97')
		item3 = types.KeyboardButton('96')
		item4 = types.KeyboardButton('95')
		item4 = types.KeyboardButton('94')
		item5 = types.KeyboardButton('93')
		item6 = types.KeyboardButton('92')
		item7 = types.KeyboardButton('91')
		item8 = types.KeyboardButton('90')

		keyboard.row(item1 , item2)
		keyboard.row(item3 , item4)
		keyboard.row(item5 , item6)
		keyboard.row(item7 , item8)

		msg = bot.send_message(message.chat.id , "سال ورودی را انتخاب نمایید", reply_markup = keyboard)
		bot.register_next_step_handler(msg, start_search_by_join )



def start_search_by_join(message):
	try:
		# join_uni = message.text
		# if join_uni == "97":
		# 	msg = bot.send_message(message.chat.id , "ok")
		# 	bot.register_next_step_handler(msg, start_search_by_join )
		# else:
		# 	raise Exception()	
			# start_search_by_join(message)
		user_join = message.chat
		if return_line_join(user_join) == -1:
			msg = bot.send_message(message.chat.id , "NOT FOUND !!")
			bot.register_next_step_handler(msg, start_search_by_join)
		elif return_line_join(user_join) == 0:	
			msg = bot.send_message(message.chat.id , "NOT FOUND 22222222!!")
			bot.register_next_step_handler(msg, start_search_by_join)
		else:
			list = user_line_by_join(user_join)
			for i in list:
				bot.send_message(message.chat.id , list[i])
				if i != -1:
					bot.send_message(message.chat.id , "بعدی")
	except Exception:
		msg = bot.send_message(message.chat.id , "something wrong !")
		bot.register_next_step_handler(msg, start_search_by_join)
	

def signup_fname(message):
	if message.text =="/end" or message.text =="🔺 خروج":
		bot.reply_to(message, "❌ فرایند لغو گردید ❌ ")
		send_welcome(message)
	elif message.text == "↪️ مرحله قبل":
		bot.reply_to(message, "↪️ وارد مرحله قبلی شدید ")
		send_welcome(message)
	else:
		try:
			chat_id = message.chat.id
			fname = message.text
			if fname.isdigit():	
				msg = bot.reply_to(message, '📛 نام عدد نمیتواند باشد . مجدد تلاش کنید')
				bot.register_next_step_handler(msg, signup_fname)
				return
			elif re.compile(r'[a-z]').match(fname) or re.compile(r'[A-Z]').match(fname) or re.search("^['/start'.*]", fname):
				raise Exception()
			else:
				user = User(fname)
				user_dict[chat_id] = user

				# config user info
				user_fname = message.from_user.first_name
				user_lname = message.from_user.last_name
				user_username = message.from_user.username
				user_id = message.from_user.id
				user.user_fname, user.user_lname, user.user_username, user.user_id = user_fname, user_lname, user_username, user_id

				msg = bot.send_message(message.chat.id, "نام خانوادگی خود را بصورت فارسی وارد نمایید 📝")	
				bot.register_next_step_handler(msg, signup_lname)
		except Exception :
			msg = bot.send_message(message.chat.id, " 📛 نام انگلیسی نمیتواند باشد . مجدد تلاش کنید")
			bot.register_next_step_handler(msg, signup_fname)



def signup_lname(message):
	if message.text =="/end" or message.text =="🔺 خروج":
		bot.reply_to(message, "❌ فرایند لغو گردید ❌ ")
		send_welcome(message)
	elif message.text == "↪️ مرحله قبل":
		msg = bot.reply_to(message, "↪️ وارد مرحله قبل شدید \n\nنام خود را بصورت فارسی وارد نمایید 📝")
		bot.register_next_step_handler(msg, signup_fname)
	else:
		try:
			chat_id = message.chat.id
			user = user_dict[chat_id]
			lname = message.text
			user.lname = lname
			if lname.isdigit():	
				msg = bot.reply_to(message, '📛 نام خانوادگی عدد نمیتواند باشد . مجدد تلاش کنید')
				bot.register_next_step_handler(msg, signup_lname)
				return
			if re.compile(r'[a-z]').match(lname) or re.compile(r'[A-Z]').match(lname) or re.search("^['/start'.*]", lname):
				raise Exception()
			msg = bot.send_message(message.chat.id, "تلفن همراه خود وارد نمایید 📞 \n\n⚠️ همراه با صفر\n\n⚠️ بصورت لاتین")
			bot.register_next_step_handler(msg, signup_phone)
		except Exception :
			msg = bot.send_message(message.chat.id, "📛 نام خانوادگی انگلیسی نمیتواند باشد . مجدد تلاش کنید")
			bot.register_next_step_handler(msg, signup_lname)


def signup_phone(message):
	if message.text =="/end" or message.text =="🔺 خروج":
		bot.reply_to(message, "❌ فرایند لغو گردید ❌ ")
		send_welcome(message)
	elif message.text == "↪️ مرحله قبل":
		msg = bot.reply_to(message, "↪️ وارد مرحله قبل شدید \n\nنام خانوادگی خود را بصورت فارسی وارد نمایید 📝")
		bot.register_next_step_handler(msg, signup_lname)	
	else:
		try:
			chat_id = message.chat.id
			phone = message.text
			if not phone.isdigit():	
				msg = bot.reply_to(message, '📛 تلفن همراه فقط شامل عدد می باشد . مجدد تلاش کنید')
				bot.register_next_step_handler(msg, signup_phone)
				return
			if not re.search("^[0][9][0-9]{9,9}$", phone):
				raise Exception()
			user = user_dict[chat_id]
			user.phone = phone     
			markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton('👨🏻‍💼 آقا')
			item2 = types.KeyboardButton('👩🏻‍💼 خانم')
			item3 = types.KeyboardButton('🔺 خروج')
			item4 = types.KeyboardButton('↪️ مرحله قبل')

			markup.row(item1 , item2)
			markup.row(item3 , item4)


			msg = bot.send_message(message.chat.id, "جنسیت خود را انتخاب نمایید 📍", reply_markup=markup)
			bot.register_next_step_handler(msg, signup_gender)
		except Exception :
			msg = bot.reply_to(message, ' 📛 تلفن همراه معتبر نمی باشد . مجدد تلاش کنید')
			bot.register_next_step_handler(msg, signup_phone)

def signup_gender(message):
	if message.text =="/end" or message.text =="🔺 خروج":
		bot.reply_to(message, "❌ فرایند لغو گردید ❌ ")
		send_welcome(message)
	elif message.text == "↪️ مرحله قبل":
		keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton('↪️ مرحله قبل')
		item2 = types.KeyboardButton('🔺 خروج')

		keyboard.row(item2 , item1)

		msg = bot.reply_to(message, "↪️ وارد مرحله قبل شدید \n\nتلفن همراه خود وارد نمایید 📞 \n\n⚠️ همراه با صفر\n\n⚠️ بصورت لاتین" , reply_markup = keyboard)
		bot.register_next_step_handler(msg, signup_phone)
	else:
		try:
			chat_id = message.chat.id
			gender = message.text
			user = user_dict[chat_id]
			if (gender == '👨🏻‍💼 آقا') or (gender == '👩🏻‍💼 خانم'):
				gender = gender.split()
				user.gender = gender[1]
				if user.gender == 'آقا':
					user.gender_emoji = '👨🏻‍💼'
				elif user.gender == 'خانم':
					user.gender_emoji = '👩🏻‍💼'	
			else:
				raise Exception()

			keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
			item1 = types.KeyboardButton('↪️ مرحله قبل')
			item2 = types.KeyboardButton('🔺 خروج')

			keyboard.row(item2 , item1)	

			msg = bot.send_message(message.chat.id , "شماره دانشجویی خود را وارد نمایید 📝\n\n⚠️ بصورت لاتین" , reply_markup=keyboard)	
			bot.register_next_step_handler(msg, signup_sn)
		except Exception :
			msg = bot.send_message(message.chat.id, "📛 جنسیت وارد شده معتبر نمی باشد . مجدد تلاش کنید")
			bot.register_next_step_handler(msg, signup_gender)


def signup_sn(message):
	if message.text =="/end" or message.text =="🔺 خروج":
		bot.reply_to(message, "❌ فرایند لغو گردید ❌ ")
		send_welcome(message)
	elif message.text == "↪️ مرحله قبل":
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		item1 = types.KeyboardButton('👨🏻‍💼 آقا')
		item2 = types.KeyboardButton('👩🏻‍💼 خانم')
		item3 = types.KeyboardButton('🔺 خروج')
		item4 = types.KeyboardButton('↪️ مرحله قبل')

		markup.row(item1 , item2)
		markup.row(item3 , item4)

		msg = bot.reply_to(message, "↪️ وارد مرحله قبل شدید \n\nجنسیت خود را انتخاب نمایید 📍", reply_markup = markup)
		bot.register_next_step_handler(msg, signup_gender)	
	else:
		try:
			chat_id = message.chat.id
			sn = message.text
			if not sn.isdigit():	
				msg = bot.reply_to(message, '📛 شماره دانشجویی فقط شامل عدد می باشد . مجدد تلاش کنید')
				bot.register_next_step_handler(msg, signup_sn)
				return
			if not re.search("^[9][0-8][0-9]{7,7}$", sn):
				raise Exception()
			user = user_dict[chat_id]
			user.sn = sn        
			user.join = sn[0:2]
			user_info = f"\n\n{user.gender_emoji} نام: {user.fname}\n\n{user.gender_emoji} نام خانوادگی: {user.lname}\n\n👥 ورودی:  {user.join}\n\n📍 جنسیت: {user.gender}\n\n📞 تلفن همراه: {user.phone}\n\n🔗 شماره دانشجویی: {user.sn}"
			cec_info = "\n\n🔰کارگروه برنامه نویسی انجمن علمی مهندسی کامپیوتر 💡\n\n🏫 دانشگاه آزاد اسلامی واحد کرج\n\n🔄 /start شروع مجدد"
			msg = bot.send_message(message.chat.id, f"ثبت نام شما با موفقیت انجام شد ✅"+user_info+cec_info)
			myFile = open('signup.txt' , 'a+' , encoding="utf-8")
			mytime = time.strftime("%H:%M:%S")
			myFile.write(f"| Date: {JalaliDate.today()} time: {mytime}        | id={user.user_id}      | join_uni={user.join}      | fname={user.fname}  lname={user.lname}      | phone={user.phone}       | gender={user.gender}      | sn={user.sn} \n\n")
			myFile.close()
			bot.register_next_step_handler(msg, send_welcome)
		except Exception :
			msg = bot.reply_to(message, ' 📛 شماره دانشجویی معتبر نمی باشد . مجدد تلاش کنید')
			bot.register_next_step_handler(msg, signup_sn)








# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
# bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
# bot.load_next_step_handlers()



bot.polling()
f"🙀Hello dear {name}\n\n🆔Your id is =  {id} \n\n👤Your username is = @{username}\n\n🗓 امروز {day}  {month}  {year} \n🕖 ساعت {time_now} \n\n🤖Py Bot\n👨‍💻Developer: Erfan Esmaeeli"  
