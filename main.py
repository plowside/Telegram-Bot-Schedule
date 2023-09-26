# -*- coding: utf-8 -*-
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters import BoundFilter

from config import *

import pytz, datetime, json, asyncio, sqlite3, logging, random, os, httpx
#################################################################################################################################
con = sqlite3.connect('db.db')
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	uid INT,
	username TEXT,
	course TEXT,
	is_banned BOOL DEFAULT(False)
	)''')
cur.execute('''CREATE TABLE IF NOT EXISTS cache(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	query TEXT,
	json TEXT,
	temp TEXT,
	temp_ INT
	)''')
#################################################################################################################################
storage = MemoryStorage()
bot = Bot(token=bot_token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s', level=logging.INFO,)
logging.getLogger("httpx").setLevel(logging.WARNING)
#################################################################################################################################
async def get_teacher(id = None):
	async with httpx.AsyncClient() as client:
		try:
			req = (await client.get('https://api.collegeschedule.ru:8443/users/', params={'offset': '0','limit': '500','type': 'TEACHER'}, headers={'authority': 'api.collegeschedule.ru:8443','accept': 'application/json, text/plain, */*','accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7','authorization': 'Bearer nke','if-none-match': 'W/"5ff6-y/moxr/LYNcuxHdmJUEQnglaRu0"','origin': 'http://www.nke.ru','referer': 'http://www.nke.ru/','sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})).json()
			if len(cur.execute('SELECT * FROM cache WHERE query = "teacher"').fetchall()) != len(req):
				cur.execute('DELETE FROM cache WHERE query = "teacher"');con.commit()
				for x in req: cur.execute('INSERT INTO cache(query, json) VALUES("teacher", ?)',[json.dumps(x)])
				con.commit()
		except:
			req = [json.loads(x[0]) for x in cur.execute('SELECT json FROM cache WHERE query = "teacher"').fetchall()]
			if len(req) == 0: q
		if id: return [x for x in req if x['id'] == id or id in x['full'].lower()]
		return req

async def get_groups(id = None, is_q=False):
	async with httpx.AsyncClient() as client:
		try:
			req = (await client.get('https://api.collegeschedule.ru:8443/groups/', params={'offset': '0','limit': '500'}, headers={'authority': 'api.collegeschedule.ru:8443','accept': 'application/json, text/plain, */*','accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7','authorization': 'Bearer nke','if-none-match': 'W/"5ff6-y/moxr/LYNcuxHdmJUEQnglaRu0"','origin': 'http://www.nke.ru','referer': 'http://www.nke.ru/','sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})).json()
			if len(cur.execute('SELECT * FROM cache WHERE query = "groups"').fetchall()) != len(req):
				cur.execute('DELETE FROM cache WHERE query = "groups"');con.commit()
				for x in req: cur.execute('INSERT INTO cache(query, json) VALUES("groups", ?)',[json.dumps(x)])
				con.commit()
		except:
			req = [json.loads(x[0]) for x in cur.execute('SELECT json FROM cache WHERE query = "groups"').fetchall()]
			if len(req) == 0: q
	
		if id:
			if is_q: [x for x in req if str(x['id']) == str(id)]
			return [x for x in req if str(x['id']) == id or id in ','.join([x['title'],x['pretty']]).lower()]
		return req

async def get_buildings(id: int = None):
	async with httpx.AsyncClient() as client:
		try:
			req = (await client.get('https://api.collegeschedule.ru:8443/buildings/0/classrooms/', params={'offset': '0','limit': '500'}, headers={'authority': 'api.collegeschedule.ru:8443','accept': 'application/json, text/plain, */*','accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7','authorization': 'Bearer nke','if-none-match': 'W/"5ff6-y/moxr/LYNcuxHdmJUEQnglaRu0"','origin': 'http://www.nke.ru','referer': 'http://www.nke.ru/','sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})).json()
			if len(cur.execute('SELECT * FROM cache WHERE query = "buildings"').fetchall()) != len(req):
				cur.execute('DELETE FROM cache WHERE query = "buildings"');con.commit()
				for x in req: cur.execute('INSERT INTO cache(query, json) VALUES("buildings", ?)',[json.dumps(x)])
				con.commit()
		except:
			req = [json.loads(x[0]) for x in cur.execute('SELECT json FROM cache WHERE query = "buildings"').fetchall()]
			if len(req) == 0: q

		return req

async def get_group(id,is_=False):
	async with httpx.AsyncClient() as client:
		id = int(id)
		utc = pytz.utc
		today = datetime.datetime.today()
		need_ts = int(utc.normalize(utc.localize(today - datetime.timedelta(days=today.weekday()+1), is_dst=None).astimezone(utc).replace(hour=0, minute=0, second=0)).timestamp())
		try:
			if is_:
				req = (await client.get('https://api.collegeschedule.ru:8443/schedule/', params={'start': need_ts,'end': need_ts+900000,'groupId': id}, headers={'authority': 'api.collegeschedule.ru:8443','accept': 'application/json, text/plain, */*','accept-language': 'ru,ru-RU;q=0.9,en-US;q=0.8,en;q=0.7','authorization': 'Bearer nke','origin': 'http://www.nke.ru','referer': 'http://www.nke.ru/','sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})).json()

				if len(cur.execute('SELECT * FROM cache WHERE (query,temp_) = ("group",?)',[id]).fetchall()) != len(req):
					cur.execute('DELETE FROM cache WHERE (query,temp_) = ("group",?)',[id]);con.commit()
					cur.execute('INSERT INTO cache(query, json, temp_) VALUES("group", ?, ?)',[json.dumps(req), id])
					con.commit()
			else:
				req = [json.loads(x[0]) for x in cur.execute('SELECT json FROM cache WHERE (query,temp_) = ("group",?)',[id]).fetchall()][0]
				if len(req) == 0: q
		except:
			print('eerro')
			req = [json.loads(x[0]) for x in cur.execute('SELECT json FROM cache WHERE (query,temp_) = ("group",?)',[id]).fetchall()][0]
			if len(req) == 0: q

		return req

def format_date(d=0,m=0,y=0,m_=None,ts=None,is_today=False):
	if ts:
		_=datetime.datetime.fromtimestamp(ts)+datetime.timedelta(hours=7)
		d, m, y = _.day, _.month, _.year

	if len(str(d)) > 9 and str(d)[0] == '0': d = str(d)[1]
	if len(str(m)) > 9 and str(m)[0] == '0': m = str(m)[1]
	m_ = {1:'Января',2:'Февраля',3:'Марта',4:'Апреля',5:'Мая',6:'Июня',7:'Июля',8:'Августа',9:'Сентября',10:'Октября',11:'Ноября',12:'Декабря'}[m]

	return (d, m, y, m_, f'{d} {m_}', is_today)

def kb_construct(keyboard,query):
	if type(query) is dict:
		for x in query:
			_ = query[x].split('^')
			if _[0] == 'url': keyboard.insert(InlineKeyboardButton(x,url=_[1]))
			elif _[0] == 'cd': keyboard.insert(InlineKeyboardButton(x,callback_data=_[1]))
	else:
		for x in query: keyboard.insert(x)
	return keyboard

async def kb_get_courses():
	s = {x:f'cd^utils:get_course:{x}' for x in set([x['course'] for x in (await get_groups()) if 'course' in x])}
	keyboard = kb_construct(InlineKeyboardMarkup(row_width=2), s)
	return keyboard

async def kb_get_course(id):
	s = {x[1]:f'cd^utils:get_group:{x[0]}:{id}' for x in sorted(set([(x['id'], x['pretty']) for x in (await get_groups()) if 'course' in x and str(x['course']) == id]))}
	keyboard = kb_construct(InlineKeyboardMarkup(row_width=3), s)
	
	keyboard.add(InlineKeyboardButton('↪ Назад',callback_data='utils:get_courses'))
	return keyboard

async def kb_get_group(id,course):
	s = {}
	today = datetime.datetime.today().day
	for x in sorted([x['date'] for x in (await get_group(id))['items']]):
		d=format_date(ts=x)
		s[f"🔆 {d[4]}" if d[0] == today else f"🌑 {d[4]}" if  d[0] == today+1 else d[4]] = f'cd^utils:get_day:{x}:{id}:{course}' 
	keyboard = kb_construct(InlineKeyboardMarkup(row_width=2), s)

	keyboard.add(InlineKeyboardButton('↪ Назад',callback_data=f'utils:get_course:{course}'))
	return keyboard

async def kb_get_day(day,group,course,temp):
	s={}
	if temp[0][0]: s['❮❮']=f'cd^utils:get_day:{day-86400}:{group}:{course}'
	elif temp[0][1]: s['❮❮']=f'cd^utils:get_day:{day-172800}:{group}:{course}'
	if temp[1][0]: s['❯❯']=f'cd^utils:get_day:{day+86400}:{group}:{course}'
	elif temp[1][1]: s['❯❯']=f'cd^utils:get_day:{day+172800}:{group}:{course}'

	keyboard = kb_construct(InlineKeyboardMarkup(row_width=2), s)

	keyboard.add(InlineKeyboardButton('↪ Назад',callback_data=f'utils:get_group:{group}:{course}'))
	return keyboard
#################################################################################################################################
class is_reg(BoundFilter):
	async def check(self, message: types.Message):
		uid = message.from_user.id
		uum = message.from_user.username if message.from_user.username else None
		user_db = cur.execute('SELECT * FROM users WHERE uid = ?',[uid]).fetchone()


		if user_db is not None and bool(user_db[4]) is False: return True

		cur.execute('INSERT INTO users(uid, username, course) VALUES (?, ?, "1")',[uid,uum]);con.commit()

		for x in admin_id:
			url = f'<a href="t.me/{uum}">{message.from_user.first_name}</a>' if uum else f'<a href="tg://user?id={uid}">{message.from_user.first_name}</a>'
			try: await bot.send_message(x, f'<b>🔔 Новый пользователь!\n\n👤 Username: {url}\n🆔 Telegram ID: <code>{uid}</code></b>', disable_web_page_preview=True, reply_markup=kb_construct(InlineKeyboardMarkup(row_width=1),{'❌ Закрыть':'cd^utils:delete'}))
			except: pass

		return True


@dp.message_handler(is_reg(), CommandStart())
async def CommandStart_(message: types.Message):
	uid=message.from_user.id
	uum=message.from_user.username
	try: await message.answer('<i>Выберите свой курс</i>', reply_markup=await kb_get_courses())
	except: await message.answer('<b>🖥 Сервер расписания не отвечает</b>',reply_markup=kb_construct(InlineKeyboardMarkup(row_width=1), {'Проверить вручную':'url^http://www.nke.ru/students/raspisanie','❌ Закрыть':'cd^utils:delete'}));return


@dp.callback_query_handler(is_reg(), text_startswith='utils')
async def utils_(call: types.CallbackQuery, state: FSMContext):
	await state.finish()
	uid=call.from_user.id
	uum=call.from_user.username
	cd = call.data.split(':')

	if cd[1] == 'get_courses':
		try: await call.message.edit_text('<i>Выберите свой курс</i>', reply_markup=await kb_get_courses())
		except: await call.answer('🖥 Сервер расписания не отвечает',show_alert=True);return

	if cd[1] == 'get_course':
		course = cd[2]
		cur.execute('UPDATE users SET course = ? WHERE uid = ?',[course, uid]);con.commit()

		try: await call.message.edit_text(f'<i>Выберите группу</i>', reply_markup=await kb_get_course(course))
		except: await call.answer('🖥 Сервер расписания не отвечает',show_alert=True);return
	
	elif cd[1] == 'get_group':
		group = cd[2]
		course = cd[3]

		cur.execute('UPDATE users SET course = ? WHERE uid = ?',[f'{course},{group}', uid]);con.commit()
	
		try: await call.message.edit_text(f'<i>Выберите день</i>', reply_markup=await kb_get_group(group,course))
		except: await call.answer('🖥 Сервер расписания не отвечает',show_alert=True);return

	elif cd[1] == 'get_day':
		day = int(cd[2])
		group = cd[3]
		course = cd[4]

		try: group_data = (await get_group(group))#['items']
		except: await call.answer('🖥 Сервер расписания не отвечает',show_alert=True);return
		day_data = sorted([x for x in group_data['items'] if x['date'] == day], key=lambda x: x['sort'])
		_ = [x['date'] for x in group_data['items']]
		
		json_days = {
			0:"Понедельник",
			1:"Вторник",
			2:"Среда",
			3:"Четверг",
			4:"Пятница",
			5:"Суббота",
			6:"Воскресенье"
		}

		today = datetime.datetime.today().day
		today_ = (datetime.datetime.fromtimestamp(day)+datetime.timedelta(hours=7)).weekday()
		ddd = format_date(ts=day)

		try:text = f'<code>{ddd[4]}</code> | {"🔆" if today == ddd[0] else "🌑" if  today+1 == ddd[0] else ""} {json_days[today_]}\n\n<b>{group_data["meta"]["group"]["pretty"]}</b> - <i>{group_data["meta"]["group"]["specialty"]["boss"]["pretty"]}</i>\n'
		except: return await call.answer('🖥 Сервер расписания не отвечает',show_alert=True)

		time_ = {
			True: {
				1: ['8:30','10:05'],
				2: ['10:20','11:55'],
				3: ['12:25','14:00'],
				4: ['14:10','15:45'],
				5: ['15:55','17:00'],
				6: ['17:10','18:45']
			},
			False: {
				1: ['8:30','10:05'],
				2: ['10:15','11:50'],
				3: ['12:10','13:45'],
				4: ['13:55','15:30'],
				5: ['15:45','17:20'],
				6: ['17:30','19:05']
			}
		}


		try:
			for x in day_data:
				sub_title=x['plan']['subject']['short']
				sub_teacher=x['teacher']['pretty']
				sub_subgroup=f"├ Подгруппа: <b>{x['subgroup']}</b>\n" if x['subgroup'] is not None else None
				sub_room= f"<code>{x['classroom']['title']}</code>"
				sub_index=x['sort']+1
				time = time_[today_ != 6][sub_index]
				text_=f'\n👁‍🗨Пара: <code>{sub_index}</code>\n├ Предмет: <b><i>{sub_title}</i></b>\n├ Кабинет:  <code>{sub_room}</code>\n{sub_subgroup if sub_subgroup else ""}├ Время:  <code>{time[0]} </code><b>/</b><code> {time[1]}</code>\n└ Преподаватель: <b>{sub_teacher}</b>\n'
				text+=text_
		except: return await call.answer('🖥 Сервер расписания не отвечает',show_alert=True)

		try:await call.message.edit_text(text, reply_markup=await kb_get_day(day,group,course,[(day-86400 in _,day-172800 in _),(day+86400 in _,day+172800 in _)]))
		except: await call.answer('.')

	elif cd[1] == 'delete':
		await call.message.delete()




async def db_update():
	while True:
		groups = await get_groups()
		for x in groups:
			d=await get_group(x['id'],True)
		await asyncio.sleep(3600)


#################################################################################################################################
async def on_startup(dp):
	global bot_info
	bot_info=await bot.get_me()
	async def set_default_commands(dp):
		await dp.bot.set_my_commands([types.BotCommand("start", "Запустить бота")])
	await set_default_commands(dp)
	asyncio.get_event_loop().create_task(db_update())

if __name__ == '__main__':
	executor.start_polling(dp, on_startup=on_startup)