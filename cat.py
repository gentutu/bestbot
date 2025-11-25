########################################################################################################################
# INCLUDES
########################################################################################################################
import aiohttp

########################################################################################################################
# API
########################################################################################################################
async def get(animal, apiKey, mimeType):
    headers = {
        'x-api-key'   : apiKey,
        'Content-Type': 'application/json'
    }
    params = {
        'mime_types': mimeType
    }

    if(animal == 'cat'):
        API = 'https://api.thecatapi.com/v1/images/search'
    elif(animal == 'dog'):
        API = 'https://api.thedogapi.com/v1/images/search'
    else:
        return "Unknown API"

    async with aiohttp.ClientSession() as session:
        async with session.get(API, headers = headers, params = params) as response:
            if response.status != 200 or 'application/json' not in response.headers['content-type']:
                return "Cannot reach API"
            else:
                url = await response.json()
                return url[0]['url']

########################################################################################################################
# END OF FILE
########################################################################################################################