########################################################################################################################
# INCLUDES
########################################################################################################################
import aiohttp

########################################################################################################################
# API
########################################################################################################################
async def send(api_key, mime_type):
    headers = {
        'x-api-key' : api_key,
        'Content-Type' : 'application/json'
}
    params = {
        'mime_types' : mime_type
}

    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.thecatapi.com/v1/images/search', headers=headers, params=params) as response:

            if response.status != 200 or 'application/json' not in response.headers['content-type']:
                return "Cannot reach api.thecatapi.com"

            else:
                url = await response.json()
                return url[0]['url']

########################################################################################################################
# END OF FILE
########################################################################################################################
