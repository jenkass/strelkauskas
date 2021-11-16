import random

import telebot
from telebot import types

import config

bot = telebot.TeleBot(config.TOKEN)
compliments = ('Всегда считал, что совершенства не существует, пока не увидел тебя)',
               'В чай добавляют сахар для сладости, а в мою жизнь нужна сладкая ты)',
               'Мне нужна карта и компас, чтобы не заблудиться в твоих глазах)',
               'Ты невероятно привлекательна)',
               'Ты, действительно, милая)',
               'Ты такая обаятельная)',
               'Ты очаровательна)',
               'Ты такая соблазнительная)',
               'Не грусти, ведь ты причина, по которой кто-то улыбается)',
               'Я утонул в твоих глазах)',
               'Этот мир нуждается в таких людях, как ты',
               'Ты совершенна такой, какая есть. Помни, что в этом мире нет такой же, как ты)',
               'Ты забавная)',
               'У тебя золотое сердце)',
               'Мне повезло, что судьба нас столкнула вместе',
               'Я бы сравнил тебя с цветком, но такого красивого не существует',
               'Во времена Трои, война была бы из-за тебя',
               'Ты из тех роковых красоток, в которых влюбляются без памяти.',
               )
i = 0


@bot.message_handler(commands=['start'])
def start_message(message):
    sti = open('AnimatedSticker.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Почувствовать тепло ☺")
    item2 = types.KeyboardButton("Увидеть красоту 😛")
    markup.add(item1, item2)
    bot.send_message(message.chat.id,
                     f"Хеееей, {message.from_user.first_name}!\n<b>Я хочу поднять тебе настроение</b>😇\n"
                     f"Для начала улыбнись и выбирай пункт в меню ⬇\n"
                     f"Ты увидишь самую красивую девочку на этом свете😃", parse_mode='html',
                     reply_markup=markup)


@bot.message_handler(content_types=['text'])
def repeat(message):
    if message.chat.type == 'private':
        if message.text == 'Почувствовать тепло ☺':
            bot.send_message(message.chat.id, random.choice(compliments))
        elif message.text == 'Увидеть красоту 😛':
            markup = types.InlineKeyboardMarkup(row_width=1)
            item1 = types.InlineKeyboardButton('Увидеть один кусочек пазла 💛', callback_data='photo')
            item2 = types.InlineKeyboardButton('Почувствовать химию внутри 💚', callback_data='video')

            markup.add(item1, item2)
            bot.send_message(message.chat.id,
                             '<b>💫 Это мозайка 💫\nСобирай пазлы по одному и выясни, что же невероятное '
                             'там. \nПосле того, как закончишь, сравни свой результат с '
                             'ожидаемым🙈</b>', parse_mode='html', reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Эй, ты чего, лучше выбери пункт меню :)")


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'photo':
                global i
                bot.send_photo(call.message.chat.id, photo=open(config.IMG[i], 'rb'), caption=config.MUSIC[i])

                markup = types.InlineKeyboardMarkup(row_width=1)
                item1 = types.InlineKeyboardButton('Увидеть один кусочек пазла 💛', callback_data='photo')
                item2 = types.InlineKeyboardButton('Почувствовать химию внутри 💚', callback_data='video')
                markup.add(item1, item2)

                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=None)
                response = f'Итак, ты собрала {i + 1} пазл(а)(ов) из 11🧩'
                if i == 10:
                    response = f'Ты сорбала все пазлы, теперь почувстуй химию🔥'
                bot.send_message(call.message.chat.id, text=response,
                                 reply_markup=markup)
                if i == 10:
                    i = 0
                else:
                    i += 1

            elif call.data == 'video':
                bot.send_video(call.message.chat.id, data=open(config.VIDEO, 'rb'))
                bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                              reply_markup=None)



    except Exception as e:
        print(repr(e))


bot.polling(none_stop=True)
