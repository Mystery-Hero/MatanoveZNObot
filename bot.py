import telebot;

TOKEN = '123'
bot = telebot.TeleBot(TOKEN);

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привіт! Я допомагаю в групі  @matan_help. Поки що у мене зовсім малий функціонал. Прошу не спамити команди в групу без поважної причини)')
    bot.send_message(message.chat.id, 'Бажаю усім 200 балів на ЗНО)')
@bot.message_handler(commands=['help'])
def send_help_message(message):
	bot.send_message(message.chat.id, 'Командою "/questiоn" ви можете попросити допомоги з якоюсь задачею');
	bot.send_message(message.chat.id, 'Командою "/repоrt" ви можете повідомити про порушення, один з адмінів прийде на допомогу');

@bot.message_handler(commands=['report'])
def report_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeP @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(message.chat.id, 'Розбійник в @matan_help');

@bot.message_handler(commands=['question'])
def question_message(message):
	bot.reply_to(message, '@mataner @andead422 @dimaborak @Gazelka @nporMaTeP @melkii_pumba');
	if (message.chat.type == 'supergroup'):
		bot.send_message(message.chat.id, 'Є питання в @matan_help');

#@bot.message_handler(content_types=['text'])
#def send_text(message):
 #   if message.text == '!report':
 #       bot.send_message(message.chat.id, '@mataner @andead422 @dimaborak @Gazelka')
 #       bot.send_message(-1001418192939, 'Зайдіть в Матанове')
#
 #   elif message.text == '!helper':Є питання
 #       bot.send_message(message.chat.id, 'Нова задача в Матановому')

bot.polling()










