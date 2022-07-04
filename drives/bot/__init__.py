from pyrogram import Client
from ..vars import Var

bot = Client(
	'zero_two_private_session',
	api_id=Var.API_ID,
	api_hash=Var.API_HASH,
	sleep_threshold=Var.SLEEP_THRESHOLD,
	workers=Var.WORKERS
)

multi_clients = {}
work_loads = {}
