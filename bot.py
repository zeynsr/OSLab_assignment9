import telebot
import random
import qrcode
from khayyam import JalaliDatetime
from gtts import gTTS

bot=telebot.TeleBot("2121470448:AAGrgK1EpHad3dHawzn_EJji0AE3c5eo6rA")

num=0

@bot.message_handler(commands=['start'])
def hello(message):
    bot.reply_to(message, "wellcome "+message.from_user.first_name)

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,"""
        /start
    Wellcome
    /game 
    guessing number
    /age
    calculate your age
    /voice
    send a sentence.....get the voice
    /max
    calculate the maximum of an array
    /argmax
    Calculate the maximum index of an array
    /qrcode
    Get QRcode for a text
    /help
    Instructions guide
        """)

@bot.message_handler(commands=['game'])
def guess(message):
    global num
    num=random.randint(0,21)
    user_g=bot.send_message(message.chat.id,'guess the number[0-20] :')
    bot.register_next_step_handler(user_g, game)
def game(user_g):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1)
    Button = telebot.types.KeyboardButton('New Game')
    markup.add(Button)
    global num

    if user_g.text == "New Game":
        user_g = bot.send_message(user_g.chat.id, 'game has started again...\nguess another number[0-20] :',reply_markup=markup)
        num = random.randint(0,21)
        bot.register_next_step_handler(user_g, game)
    else:  
        try:  
            if int(user_g.text) > num :
                user_g = bot.send_message(user_g.chat.id, 'go down🔻',reply_markup=markup)
                bot.register_next_step_handler(user_g, game)
            elif int(user_g.text) < num :
                user_g=bot.send_message(user_g.chat.id,'go up🔺',reply_markup=markup)
                bot.register_next_step_handler(user_g, game)
            else :
                markup = telebot.types.ReplyKeyboardRemove(selective=True)
                user_g=bot.send_message(user_g.chat.id,'you Win✨',reply_markup=markup)  

        except:
            user_g=bot.send_message(user_g.chat.id,'Enter the correct number in the range',reply_markup=markup)
            bot.register_next_step_handler(user_g, game)

@bot.message_handler(commands=['age'])
def age(message):
    BDay=bot.send_message(message.chat.id,'Enter your date of birth [Y/M/D]:')
    bot.register_next_step_handler(BDay,ExactAge)
def ExactAge(BDay):
    try:
        t=BDay.text.split('/')
        td=str(JalaliDatetime.now()-JalaliDatetime(t[0],t[1],t[2]))
        Te=int(td.split(' ')[0])//365
        bot.send_message(BDay.chat.id,'you are '+str(Te)+'years old.\nDays : '+str(td.split(' ')[0]))
    except:
        BDay=bot.send_message(BDay.chat.id,'Enter your date of birth correctly!! :')
        bot.register_next_step_handler(BDay,ExactAge)    

@bot.message_handler(commands=['voice'])
def Voice(message):
    v_txt=bot.send_message(message.chat.id,'Enter your text(in english) to turn it to vice :')
    bot.register_next_step_handler(v_txt,vc2txt)
def vc2txt(v_txt):
    try:
        txt=v_txt.text
        language='en'
        vc=gTTS(text=txt,lang=language,slow=False)
        vc.save('vc.mp3')
        voice=open('vc.mp3','rb')
        bot.send_voice(v_txt.chat.id,voice)
    except:  
        v_txt=bot.send_message(v_txt.chat.id,'Enter your text correctly!! :')
        bot.register_next_step_handler(v_txt,vc2txt)       

@bot.message_handler(commands=['max'])
def maximum(message):
    arr=bot.send_message(message.chat.id,'Enter your array [1,2,3,4] :')
    bot.register_next_step_handler(arr,max_arr)
def max_arr(arr):    
    try:
        numbers=list(map(int,arr.text.split(',')))
        bot.send_message(arr.chat.id,'Maximum : '+str(max(numbers)))
    except:    
        arr=bot.send_message(arr.chat.id,'Enter your array correctly!! :')
        bot.register_next_step_handler(arr,max_arr)

@bot.message_handler(commands=['argmax'])
def argmax(message):
    arr=bot.send_message(message.chat.id,'Enter your array [1,2,3,4] :')
    bot.register_next_step_handler(arr,max_arr_indx)
def max_arr_indx(arr):
    try:
        numbers=list(map(int,arr.text.split(',')))
        bot.send_message(arr.chat.id,'Maximum number index  : '+str(numbers.index(max(numbers))+1))
    except:    
        arr=bot.send_message(arr.chat.id,'Enter your array correctly!! :')
        bot.register_next_step_handler(arr,max_arr_indx)
      
@bot.message_handler(commands=['qrcode'])
def Qrcode(message):
    string=bot.send_message(message.chat.id,'Enter a text to turn it to QRcode :')        
    bot.register_next_step_handler(string,tx2QR)
def tx2QR(string):
    try:
        QR_img=qrcode.make(string.text)
        QR_img.save('QRcode.png')
        Qr=open('QRcode.png','rb')
        bot.send_photo(string.chat.id,Qr)
    except:   
        string=bot.send_message(string.chat.id,'Enter text correctly!! :')
        bot.register_next_step_handler(string,tx2QR)  

bot.infinity_polling()    
