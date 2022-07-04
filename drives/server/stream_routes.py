import math # import maths for calculation
import re # import logging to display logs
import secrets # import secrets
import mimetypes # import mimetypes for checking file mimetypes
from aiohttp.web_exceptions import HTTPNotFound # import string for converting text
import aiohttp_jinja2 # import for nothing
import aiohttp # import for nothing
import os # import for os
import asyncio

from aiohttp.web_response import json_response
from ..vars import Var # import all the variables preset in the var.py file
from aiohttp import web # import aiohttp for streaming files 
from ..bot import bot # import bot and bot2 (bot2 for database) 
from ..mod import crypto # import crypto which helps to decrypt, encrypt and create a new key
from drives.bot import multi_clients, work_loads #MultiClient
from ..utils.custom_dl import TGCustomYield, chunk_size, offset_fix # import telegrams data which helps to download file
import requests # import the requests

requested_links_id = {}

routes = web.RouteTableDef() # create a route for streaming file

async def get_file_extention(input_name: str): # get file extention
    try:
        if not '.' in input_name:
            return None
        input_name = input_name.split('.')
        input_name = input_name[len(input_name) - 1]
        return input_name
    except Exception as e:
        return None

async def media_streamer(request, message_id: int, cus_name=None): # start downloading from telegram 
    range_header = request.headers.get('Range', 0)
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if Var.MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.remote}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = utils.ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(message_id)
    logging.debug("after calling get_file_properties")
    media_msg = await bot.get_messages(Var.BIN_CHANNEL, message_id)
    file_properties = await TGCustomYield().generate_file_properties(media_msg)
    file_size = file_properties.file_size
    if range_header:
        from_bytes, until_bytes = range_header.replace('bytes=', '').split('-')
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = request.http_range.stop or file_size - 1
    req_length = until_bytes - from_bytes
    new_chunk_size = await chunk_size(req_length)
    offset = await offset_fix(from_bytes, new_chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = (until_bytes % new_chunk_size) + 1
    part_count = math.ceil(req_length / new_chunk_size)
    body = TGCustomYield().yield_file(media_msg, offset, first_part_cut, last_part_cut, part_count,
                                      new_chunk_size)
    file_name = file_properties.file_name if file_properties.file_name \
        else f"{secrets.token_hex(2)}.jpeg"
    mime_type = file_properties.mime_type if file_properties.mime_type \
        else f"{mimetypes.guess_type(file_name)}"
    if cus_name:
        extention = await get_file_extention(file_name)
        if extention:
            file_name = f'{cus_name}.{extention}'
    return_resp = web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": mime_type,
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Disposition": f'attachment; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        }
    )
    if return_resp.status == 200:
        return_resp.headers.add("Content-Length", str(file_size))
    return return_resp

def change_size(B):
	B = float(B)
	KB = float(1024)
	MB = float(KB ** 2) # 1,048,576
	GB = float(KB ** 3) # 1,073,741,824
	TB = float(KB ** 4) # 1,099,511,627,776
	if B < KB:
		return '{0} {1}'.format(B,'Bytes' if 0 == B > 1 else 'Byte')
	elif KB <= B < MB:
		return '{0:.2f} KB'.format(B/KB)
	elif MB <= B < GB:
		return '{0:.2f} MB'.format(B/MB)
	elif GB <= B < TB:
		return '{0:.2f} GB'.format(B/GB)
	elif TB <= B:
		return '{0:.2f} TB'.format(B/TB)

@routes.get("/")
async def home(request):
    return web.json_response({'status' : True})

@routes.get("/details/{mid}")
async def getDetails(request):
    try:
        mesid = request.match_info['mid']
        message = await bot.get_messages(Var.BIN_CHANNEL, int(mesid))
        if message.document:
            filename = message.document.file_name
            size = message.document.file_size
            mimetype = message.document.mime_type
        elif message.video:
            filename = message.video.file_name
            size = message.video.file_size
            mimetype = message.video.mime_type
        elif message.audio:
            filename = message.audio.file_name
            size = message.audio.file_size
            mimetype = message.audio.mime_type
        elif message.photo:
            filename = message.photo.file_name
            size = message.photo.file_size
            mimetype = message.photo.mime_type
        elif message.voice:
            filename = message.voice.file_name
            size = message.voice.file_size
            mimetype = message.voice.mime_type
        else:
            raise web.HTTPUnauthorized
        return json_response({
            "status" : True,
            "size" : change_size(size),
            "bytes" : size,
            "name" : filename,
            "contenttype" : mimetype
            })
    except Exception as e:
        print(f"Error in details : {e}")
        raise web.HTTPUnauthorized

@routes.get("/{link}")
async def start_download(request):
    global requested_links_id
    try:
        link = request.match_info['link']
        message_id = crypto.decrypt(Var.root_key, link)
        if not message_id:
            message_id = link
        if "," in message_id:
            mes_id = message_id.split(',')[0]
            name = message_id.split(',')[1]
        else:
            mes_id = message_id
            name = None
        return await media_streamer(request, int(mes_id), cus_name=name)
    except Exception as e:
        print(f"Error : {e}")
        raise web.HTTPUnauthorized

