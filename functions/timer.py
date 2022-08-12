import schedule
from telebot import types
from bot import beep

delete_beeps = []


def set_timer(message: types.Message) -> None:
    args = message.text.split()
    if len(args) <= 1 or not args[1].isdigit():
        raise ValueError('None or wrong value for ->/set')
    else:
        sec = int(args[1])
        schedule.every(sec).seconds.do(beep, message.chat.id).tag(message.chat.id)


def unset_timer(message: types.Message) -> None:
    schedule.clear(message.chat.id)
