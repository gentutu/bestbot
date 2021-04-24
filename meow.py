########################################################################################################################
# INCLUDES
########################################################################################################################
import aiohttp

########################################################################################################################
# API
########################################################################################################################
async def get(apiKey, mimeType):
    headers = {
        'x-api-key'   : apiKey,
        'Content-Type': 'application/json'
        }
    params = {
        'mime_types': mimeType
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
