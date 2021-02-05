# currency.py

import aiohttp
import asyncio

import collections, time, json

async def retrieve_currencies(api_key):
	async with aiohttp.ClientSession() as session:
		async with session.get(f'https://free.currconv.com/api/v7/currencies?apiKey={api_key}') as response:

			print(f'https://free.currconv.com/api/v7/currencies?apiKey={"*"*len(api_key)}:', response.status, response.headers['content-type'])

			if response.status != 200 or 'application/json' not in response.headers['content-type']:
				return None

			with open('./res/currencies.json', 'w') as f:
				json.dump((await response.json())['results'], f)
			
			print('Saved currency data to ./res/currencies.json')

async def get_exchange_rate(api_key, original, desired, /, __history=collections.defaultdict(lambda: (0, 0))):
	current_time = time.time()
	refresh_period = 6 * 60 * 60 # refresh exchange rates every 3 hours
	
	keys_sorted = sorted([original, desired])
	history_key = ':'.join(keys_sorted) # get a consistent key
	
	if __history[history_key][0] + refresh_period < current_time:
		# download exchange rate
		async with aiohttp.ClientSession() as session:
			async with session.get(f'https://free.currconv.com/api/v7/convert?q={keys_sorted[0]}_{keys_sorted[1]}&compact=ultra&apiKey={api_key}') as response:
				print('Retrieving exchange rate', history_key, '...')
				__history[history_key] = (time.time(), (await response.json())[f'{keys_sorted[0]}_{keys_sorted[1]}'])
	
	return __history[history_key][1] if history_key.startswith(original) else 1.0 / __history[history_key][1]

async def currency_convert(api_key, amount, original, desired):
	'__history stores the time a conversion rating was retrieved.'
	
	exchange_rate = await get_exchange_rate(api_key, original, desired)
	
	return amount * exchange_rate

if __name__ == '__main__':
	import sys, os
	
	def print_usage_and_exit():
		print('Usage:', sys.argv[0], '--get-currencies [api key]')
		print('Usage:', sys.argv[0], '--convert [api key] [amount] [origin] [desired]')
		print('Example:', sys.argv[0], '--convert 20 NZD PHP')
		sys.exit(1)
	
	if len(sys.argv) < 3:
		print_usage_and_exit()
	
	api_key = sys.argv[2]
	
	if sys.argv[1] == '--get-currencies':
		if not os.path.exists('./res'): os.mkdir('./res')
		asyncio.run(retrieve_currencies(api_key))
		
	elif sys.argv[1] == '--convert' and len(sys.argv) == 6:
		amount = float(sys.argv[3])
		original = sys.argv[4].upper()
		desired = sys.argv[5].upper()
		print(f'Converting {amount} {original} to {desired}...')
		
		exchanged = asyncio.run(currency_convert(api_key, amount, original, desired))
		print(exchanged, desired, 'at a rate of', asyncio.run(get_exchange_rate(api_key, original, desired)))
		
	else:
		print_usage_and_exit()