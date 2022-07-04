#  this is start message

from zero_two_bot.bot import bot
from zero_two_bot.vars import Var
from pyrogram import filters, emoji
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@bot.on_message(filters.command(['start', 'help']))
async def start(b, m):
	await m.reply('Official Bot',
				  reply_markup=InlineKeyboardMarkup(
					  [
						  [
							  InlineKeyboardButton(
								  f'{emoji.STAR} Source {emoji.STAR}',
								  url='https://t.me/RS_10Drives_bot'
							  )
						  ]
					  ]
				  ))
