import telebot
from telebot import types
from internet_speedtest import internet_test
import threading
import schedule
from settings.config import type_and_size
from time import sleep

import sql_database as db
from functions import timer, weather
from image_crawler import google_images
from keyboards import keyboard as kb
from settings.config import TOKEN, IMAGE, GIF, INST_USER

bot = telebot.TeleBot(TOKEN, parse_mode='html')

"""START MESSAGE"""


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message) -> None:
    """SET COMMANDS"""
    bot.set_my_commands(
        commands=[
            types.BotCommand('start', 'bot launch'),
            types.BotCommand('help', 'bot info'),
            types.BotCommand('set', 'use /set <seconds> to set a timer'),
            types.BotCommand('unset', 'bot stops timer')
        ],
        scope=types.BotCommandScopeAllPrivateChats()
    )
    """Hello message"""
    bot.send_video(message.chat.id, GIF['gif_jujutsu'],
                   caption="Hello, {0.first_name}!\nThis is <b>{1.first_name}</b>, your new Telegram Bot!\n"
                           "I'm going to help you with lots of things :)"
                   .format(message.from_user, bot.get_me()),
                   reply_markup=kb.markup_buttons)
    send_options(message, gif=True, time_sleep=2)
    db.db_table_values(
        message.from_user.id,
        message.from_user.first_name,
        message.from_user.last_name,
        message.from_user.username
    )


"""HELP MESSAGE"""


@bot.message_handler(commands=['help'])
def send_help(message: types.Message) -> None:
    bot.send_message(message.chat.id, text="I can start Speedtest and Timer, give Instagram and GitHub portfolio, "
                                           "get current Weather data and coming soon :) \n\n"
                                           "You can control me by sending these commands:\n\n"
                                           "<strong>Default options</strong>\n"
                                           "/start - bot launch\n"
                                           "/help - bot info\n\n"
                                           "<strong>Timer</strong>\n"
                                           "/set - use <u>/set <b>seconds</b></u> to set a timer\n"
                                           "/unset - bot stops timer\n\n"
                                           "COMING SOON :D")
    send_options(message, gif=True, time_sleep=1.5)


"""TIMER"""


def beep(chat_id: types.Union) -> None:
    """Send the beep message."""
    message = bot.send_message(chat_id, 'Beep!')
    timer.delete_beeps.append((message.chat.id, message.id))


@bot.message_handler(commands=['set'])
def set_timer(message: types.Message) -> None:
    try:
        split_msg = message.text.split()
        timer.set_timer(message)
        sec = int(split_msg[1])
        bot.send_message(message.chat.id, f'{sec}-seconds timer have been started!')
    except ValueError as e:
        print(e)
        bot.reply_to(message, 'Usage: /set <b>seconds</b>')
        send_options(message)


@bot.message_handler(commands=['unset'])
def unset_timer(message: types.Message) -> None:
    timer.unset_timer(message)

    first_chat_id, first_message_id = timer.delete_beeps[0][0], timer.delete_beeps[0][1]
    bot.edit_message_text('Removing...', first_chat_id, first_message_id)
    for chat_id, message_id in tuple(reversed(timer.delete_beeps)):
        bot.delete_message(chat_id, message_id)
    timer.delete_beeps.clear()

    bot.send_message(message.chat.id, 'Timer is off')
    send_options(message)


"""OPTIONS INLINE"""


def send_options(message: types.Message, gif=False, time_sleep=0.5) -> None:
    """Send options of bot possibilities

    :param message: user message
    :param gif: False=no gif, True=with gif
    :param time_sleep: time before sending options
    :return: None
    """
    sleep(time_sleep)
    if gif:
        bot.send_video(message.chat.id, GIF['gif_naruto'],
                       caption="Choose an option from the list below:",
                       reply_markup=kb.markup_inline)
    else:
        bot.send_message(message.chat.id, "Choose an option from the list below:",
                         reply_markup=kb.markup_inline)


"""WEATHER"""


def get_weather(message: types.Message) -> None:
    try:
        forecast, icon = weather.get_weather(message)
        bot.send_photo(message.chat.id, f'http://openweathermap.org/img/wn/{icon}@2x.png',
                       caption=f'{forecast}')
        send_options(message, time_sleep=1)

    except Exception as e:
        print(repr(e))
        bot.reply_to(message, '💥 Sorry, i can`t find your city\n'
                              'Try again ^_^')
        send_options(message)


"""DOWNLOAD IMAGES"""


def get_image(message: types.Message) -> None:
    try:
        bot.send_message(message.chat.id, 'Downloading...')
        name, amount = google_images.get_image(message)

        files = google_images.get_images_from_dir()
        images = [types.InputMediaPhoto(open(f, 'rb')) for f in files]

        bot.send_media_group(message.chat.id, images)
        bot.send_message(message.chat.id, f'{amount} pictures of {name} were sent!')
        send_options(message)

    except (Exception, KeyError, ValueError) as e:
        print(e)
        bot.reply_to(message, "You need to write: <b>name amount</b>")
        send_options(message)


"""KEYBOARD BUTTONS CALLBACK"""


@bot.message_handler(content_types=['text'])
def keyboard_buttons(message: types.Message) -> None:
    """Button requests"""
    if message.chat.type == 'private':
        if message.text == "❤ Support us":
            bot.send_message(message.chat.id, "https://github.com/CoolmixZero")
            send_options(message)


"""INLINE BUTTONS CALLBACK"""


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: types.CallbackQuery) -> None:
    try:
        if call.message:
            # Speedtest
            if call.data == 'speedtest':
                bot.send_video(call.message.chat.id, GIF['gif_rocket'],
                               caption="⚠ Speedtest started!\n"
                                       "🕑 Wait 15 seconds")
                download, upload = internet_test.get_internet_speed()
                bot.send_video(call.message.chat.id, GIF['gif_elon_musk'],
                               caption=f"✅ » Download speed is {download}mb/s\n"
                                       f"✅ » Upload speed is {upload}mb/s")
                send_options(call.message, time_sleep=1)

            # Instagram
            elif call.data == 'instagram':
                bot.send_photo(call.message.chat.id, IMAGE['logo_instagram'],
                               caption=f"<b><span class='tg-spoiler'>https://www.instagram.com/{INST_USER}/</span></b>")
                send_options(call.message)

            # Weather
            elif call.data == 'weather':
                msg = bot.send_message(call.message.chat.id, "What is your city?")
                bot.register_next_step_handler(msg, get_weather)

            # Download
            elif call.data == 'download':
                bot.send_message(call.message.chat.id,
                                 "Choose <b>Type, Size and Amount</b> of the images",
                                 reply_markup=kb.download_markup)
                # Type
            elif call.data == 'type':
                bot.edit_message_text('Select image <b>Type</b>',
                                      call.message.chat.id, call.message.message_id,
                                      reply_markup=kb.image_types_markup)
                # Size
            elif call.data == 'size':
                bot.edit_message_text('Select image <b>Size</b>',
                                      call.message.chat.id, call.message.message_id,
                                      reply_markup=kb.image_sizes_markup)
                # Amount
            elif call.data == 'amount':
                bot.edit_message_text('Select images <b>Amount</b>',
                                      call.message.chat.id, call.message.message_id,
                                      reply_markup=kb.image_amount_markup)
                # Back
            elif call.data == 'back':
                bot.edit_message_text("Choose <b>Type, Size and Amount</b> of the images",
                                      call.message.chat.id, call.message.message_id,
                                      reply_markup=kb.download_markup)
                # Select type
            elif call.data in ('photo', 'face', 'clipart', 'linedrawing', 'animated'):
                type_and_size['type'] = call.data
                bot.edit_message_text("Choose <b>Type, Size and Amount</b> of the images",
                                      call.message.chat.id, call.message.message_id,
                                      reply_markup=kb.download_markup)
                # Select size
            elif call.data in ('large', 'medium', 'icon'):
                type_and_size['size'] = call.data
                bot.edit_message_text("Choose <b>Type, Size and Amount</b> of the images",
                                      call.message.chat.id, call.message.message_id,
                                      reply_markup=kb.download_markup)
                # Select amount
            elif call.data in ('3', '5', '10'):
                type_and_size['amount'] = call.data
                bot.edit_message_text("Choose <b>Type, Size and Amount</b> of the images",
                                      call.message.chat.id, call.message.message_id,
                                      reply_markup=kb.download_markup)
            # Continue
            elif call.data == 'continue':
                msg = bot.edit_message_text("<b>Name(<u>Any</u>)</b> of image that you wish to download\n"
                                            f"{type_and_size}",
                                            call.message.chat.id, call.message.message_id)
                bot.register_next_step_handler(msg, get_image)
                print(type_and_size)

    except Exception as ex:
        print(repr(ex))


"""INLINE MODE"""


@bot.inline_handler(lambda query: query.query == 'text')
def query_text(inline_query: types.InlineQueryResultArticle) -> None:
    try:
        r = types.InlineQueryResultArticle('1', 'Result1', types.InputTextMessageContent('hi'))
        r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
        bot.answer_inline_query(inline_query.id, [r, r2])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        sleep(1)
