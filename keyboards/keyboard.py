from telebot import types

"""Keyboard"""
markup_buttons = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
support = types.KeyboardButton("❤ Support us")

markup_buttons.add(support)

"""Inline text"""
markup_inline = types.InlineKeyboardMarkup(row_width=2)

speed_test = types.InlineKeyboardButton("🚀 Speedtest", callback_data='speedtest')
instagram = types.InlineKeyboardButton("🔥 Instagram", callback_data='instagram')
weather = types.InlineKeyboardButton("⛈ Weather", callback_data='weather')
download = types.InlineKeyboardButton("⬇ Download", callback_data='download')

markup_inline.add(speed_test, instagram, weather, download)

"""Download inline text"""
download_markup = types.InlineKeyboardMarkup(row_width=3)

img_type = types.InlineKeyboardButton("Type", callback_data='type')
img_size = types.InlineKeyboardButton("Size", callback_data='size')
img_amount = types.InlineKeyboardButton("Amount", callback_data='amount')
continue_img = types.InlineKeyboardButton("Continue", callback_data='continue')

download_markup.add(img_type, img_size, img_amount, continue_img)
back_button = types.InlineKeyboardButton("Back", callback_data='back')

"""Image types inline text"""
image_types_markup = types.InlineKeyboardMarkup(row_width=2)

photo = types.InlineKeyboardButton("Photo", callback_data='photo')
face = types.InlineKeyboardButton("Face", callback_data='face')
clipart = types.InlineKeyboardButton("Clipart", callback_data='clipart')
linedrawing = types.InlineKeyboardButton("Linedrawing", callback_data='linedrawing')
animated = types.InlineKeyboardButton("Animated", callback_data='animated')

image_types_markup.add(photo, face, clipart, linedrawing, back_button)

"""Image size inline text"""
image_sizes_markup = types.InlineKeyboardMarkup(row_width=3)

large = types.InlineKeyboardButton("Large", callback_data='large')
medium = types.InlineKeyboardButton("Medium", callback_data='medium')
icon = types.InlineKeyboardButton("Icon", callback_data='icon')

image_sizes_markup.add(large, medium, icon, back_button)

"""Image amount inline text"""
image_amount_markup = types.InlineKeyboardMarkup(row_width=3)
three = types.InlineKeyboardButton("3", callback_data='3')
five = types.InlineKeyboardButton("5", callback_data='5')
ten = types.InlineKeyboardButton("10", callback_data='10')

image_amount_markup.add(three, five, ten, back_button)
