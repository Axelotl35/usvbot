import discord

client = discord.Client()

# IGNORE UNTIL HERE

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# IGNORE FROM HERE

# ALWAYS COPY THE LAST LINE
# ALWAYS SHARE TOKEN WITH OTHERS
client.run()