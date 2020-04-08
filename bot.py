import telebot
import random
import time
import sqlite3 as sql

con = sql.connect('Matanove.db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS `identify` (`name` STRING, `surname` STRING, `user_id` INTEGER)")
cur.execute("CREATE TABLE IF NOT EXISTS `stat` (`qty` INTEGER, `user_id` INTEGER)")
con.commit()
cur.close()

TOKEN = 'token'
bot = telebot.TeleBot(TOKEN)
path = ""
isSolving = False
rightAnswer= 0
level = 0
tm = 0
isAdd = False
add_level = 0
add_ans = 0
add_lvls_list = [0,0,0,0]
PrevHelloMessageId = 51437 # рандомні цифри, номер повідомлення
NewHelloMessageId = 51438 # message_id
helloText = """Вітаю в @matan_help ✋
Головні правила чату:
➡️Не ображати інших учасників
➡️Допомагати іншим учасникам, якщо маєте змогу
➡️Якщо вам потрібна допомога, то просто попросіть
➡️За рекламу інших сторінок - бан🚫
/help - доступні команди
Бажаємо вам 200 балів на ЗНО!"""
helpText = """ /report - повідомити про порушення
/question - якщо виникло питання
/task - розв'язуйте задачі, стань першим в рейтингу
/stat - статистика чату"""

def pts():
	tm1=int(time.time())-int(tm)
	return round(pow(2,(level-1)/2.0)*pow(3,float(level)-float(tm1/(120.0*pow(10,float(level+2)/3.0)))))

@bot.message_handler(commands=['start'])
def start_message(message):
	bot.send_message(message.chat.id, 'Привіт! Я допомагаю в групі  @matan_help')

#команди
@bot.message_handler(commands=['help'])
def help_message(message):
	bot.send_message(message.chat.id, helpText);
	
@bot.message_handler(commands=['report'])
def report_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(-1001418192939, 'Розбійник в @matan_help');

@bot.message_handler(commands=['question'])
def question_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeR @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(-1001418192939, 'Є питання в @matan_help');

@bot.message_handler(commands=['task'])
def task_text(message):
	global isSolving
	global rightAnswer
	global path
	global level
	global tm
	tm1 = time.time()
	if int(tm1) - int(tm) > 1200:
		isSolving = False
	try:
		tester=message.text[6]
	except:
		bot.reply_to(message, 'Вказані невірні аргументи. Аргументом може слугувати лише число від 1 до 4 включно, де число позначає складність завдання')
		return 0
	if not isSolving and (message.text[6]=='1' or message.text[6]=='2' or message.text[6]=='3' or message.text[6]=='4'):
		listQ=open("Data/Tasks/q.txt",'r')
		quantity=0
		counter=0
		for line in listQ:
			counter+=1
			if counter==int(message.text[6]):
				level=int(message.text[6])
				quantity=int(line)
		a=random.randint(1,quantity)
		path = r"Data/Tasks/Questions/"+message.text[6]+"/"+str(a)+".png"
		file = open(path, 'rb')
		bot.send_photo(message.chat.id, file,caption='Відповіддю є число в десятковому записі. Гарантується, що нескінченних десяткових періодичних дробів немає.\nРівень складності: ' +str(level)+ '\nПриклад: 16; -38,8; 0; 44.268. \nТермін виконання - ' + str(level*10) +' хвилин')
		isSolving = True
		path2="Data/Tasks/Solutions/"+str(level)+"/sol.txt"
		counter=0
		sol=open(path2,'r')
		for line in sol:
			counter+=1
			if counter==a:
				rightAnswer=line
		file.close()
		sol.close()
		listQ.close()
		tm=time.time()
	elif isSolving:
		file = open(path, 'rb')
		bot.send_photo(message.chat.id, file,caption=r"Спочатку розв'яжіть запропоновану задачу!")
	else:
		bot.reply_to(message, 'Вказані невірні аргументи. Аргументом може слугувати лише число від 1 до 4 включно, де число позначає складність завдання')
		return 0

@bot.message_handler(commands=['add'])
def add_command(message):
	global add_level
	global add_ans
	global isAdd
	if int(message.chat.id)!=-1001382702607:
		bot.reply_to(message, 'На жаль, Ви не маєте прав додавати завдання до боту')
		return 0
	try:
		add_level=int(message.text[5])
		add_ans=message.text[7]
		add_ans=float(message.text[7:].replace(',','.'))
		isAdd=True
	except:
		bot.reply_to(message, 'Невірні аргументи')
		return 0
	f=open('Data/Tasks/q.txt','r')
	counter=0
	for line in f:
		add_lvls_list[counter]=int(line)
		counter+=1
	add_lvls_list[add_level-1]+=1
	f.close()
	bot.reply_to(message, 'Ожидаю фото...')

# Новий учасник групи зайшов в чат
@bot.message_handler(content_types=['new_chat_members'])
def hello_message(message): 
	bot.reply_to(message, helloText)
	global PrevHelloMessageId 
	global NewHelloMessageId 
	PrevHelloMessageId = int(NewHelloMessageId)
	NewHelloMessageId = int(message.message_id) + 1 
	bot.delete_message(message.chat.id, PrevHelloMessageId) 

@bot.message_handler(content_types=['text'])
def send_text(message):
	global isSolving
	tm1=time.time()
	txt=message.text
	txt=txt.replace(',','.')
	if int(tm1)-int(tm)>1200:
		isSolving=False
	try:
		float(txt)
		isVal=True
	except ValueError:
		isVal=False
	# print(message.text)
	if isVal:
		if isSolving and float(txt) == float(rightAnswer):
			bot.reply_to(message, '*Вітаємо!* _Ви першим розв\'язали задачу рівня ' + str(level) +' за ' + str(int(tm1)-int(tm)) + ' с, і отримуєте _*+' + str(pts()) + '*_ до Вашого інтелектуального рейтингу_',parse_mode="Markdown")
			isSolving = False
			
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
	global isAdd
	if isAdd and message.chat.id==-1001382702607:
		try:
			file_info = bot.get_file(message.photo[len(message.photo)-1].file_id)
			downloaded_file = bot.download_file(file_info.file_path)
			src="Data/Tasks/Questions/" + str(add_level) + "/" + str(add_lvls_list[add_level-1]) + ".png";
			with open(src, 'wb') as new_file:
				new_file.write(downloaded_file)
				bot.reply_to(message,"Ok!")
			f=open("Data/Tasks/q.txt",'w')
			for i in add_lvls_list:
				f.write(str(i)+'\n')
			f.close()
			f=open("Data/Tasks/Solutions/"+str(add_level)+"/sol.txt", 'a')
			f.write('\n' + str(add_ans))
		except Exception as e:
			bot.reply_to(message,e)

@bot.message_handler(content_types=[""'video_note', 'voice', 'text', 'sticker', 'photo', 'audio', 'document',
                                    'video', 'location', 'contact', 'new_chat_members', 'left_chat_member'""])
def count_msg(message):
    con_sql = sql.connect('Matanove.db')
    cur_sql = con_sql.cursor()
    name = (message.from_user.first_name, "")[str(message.from_user.first_name) == "None"]
    surname = (message.from_user.last_name, "")[str(message.from_user.last_name) == "None"]
    user_id = message.from_user.id
    # print(f"{message.from_user.username} posted '{message.content_type}' content")
    cur_sql.execute(f"SELECT `user_id` FROM `identify` WHERE `user_id` = '{user_id}'")
    user_id_list = cur_sql.fetchall()
    # print(user_id)
    if len(user_id_list) > 0:
        cur_sql.execute(f"UPDATE `stat` SET `qty` = `qty` + 1 WHERE `user_id` = '{user_id}'")
    else:
        cur_sql.execute(f"INSERT INTO `identify` VALUES ('{name}', '{surname}', '{user_id}')")
        cur_sql.execute(f"INSERT INTO `stat` VALUES (1, '{user_id}')")
    con_sql.commit()
    cur_sql.close()
	
bot.polling()

