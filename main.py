""" -- Hey I don't know how to optimize code please don't judge -- """
import discord
from discord.ext import commands

token = open("token.txt", "r").read()
intents = discord.Intents.all()

client = commands.Bot(command_prefix='.', intents=intents)

""" --- ####################################### --- """


@client.event
async def on_ready():
    print('whee')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('among us'):
        await message.channel.send("kindly shut up")
    await client.process_commands(message)


""" -- hey look some commands where you actually don't lose brain cells ! -- """

""" - purges channel """
@client.command()
@commands.has_guild_permissions(manage_messages=True)
@commands.bot_has_guild_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

""" - send message when member joins """
@client.event
async def on_member_join(member):
    embed = discord.Embed(title=f"Welcome {member}!",
                          description=f"Welcome to {member.guild.name}!",
                          color=0xb8dbc1)
    embed.set_thumbnail(url=member.guild.icon_url)
    embed.set_footer(icon_url=member.avatar_url, text='nyooming . . .')
    await member.guild.system_channel.send(embed=embed)

""" - send message when member leaves """
@client.event
async def on_member_remove(member):
    embed = discord.Embed(title=f"{member} has left the server!",
                          description=f"What a loser smh",
                          color=0xffe6d4)
    embed.set_thumbnail(url=member.guild.icon_url)
    embed.set_footer(icon_url=member.avatar_url, text='nyooming . . .')
    await member.guild.system_channel.send(embed=embed)

""" - update status """
@client.command()
async def playing(ctx, *, status):
    await client.change_presence(activity=discord.Game(name=status))
    await ctx.message.add_reaction("\U0001F34B")

""" - updates a user's roles """
@client.command()
@commands.has_guild_permissions(manage_roles=True)
# @commands.bot_has_guild_permissions(manage_roles=True)
async def giverole(ctx, users: commands.Greedy[discord.Member] = client.user, *, role: discord.Role = ' '):
    for user in users:
        if role in user.roles:
            await ctx.send(f"Unable to give role: {user.mention} already has the role `{role}`")
        else:
            await user.add_roles(role)
            await ctx.message.add_reaction("\U0001F34B")
            await ctx.send(f"Successfully added {role} to {user.mention}!")

""" - error check for .giverole command """
@giverole.error
async def giverole_error(ctx, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please mention a valid user/role!")
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.send("Syntax: giverole [@user] [role]")
    elif isinstance(error, discord.Forbidden):
        await ctx.send(f"I need `Manage roles` in order to do that!\
                        Please check my permissions and try again.")
    elif isinstance(error, discord.HTTPException):
        await ctx.send("There was an error. Sorry about that \U0001F626")

""" - Will probably never be used, but I don't particularly make the best use of my time
      Also probably really inefficient
      But it works so that's pretty cool """
@client.command()
@commands.has_guild_permissions(manage_roles=True)
async def createrole(ctx, *, name):

    embed = discord.Embed(title="Creating role...!",
                          color=0xb8dbc1)
    def ctxsend(msg):
        embed.description = msg
        embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQlpPSOx-x3FPhVw0vIe1eMKrDNrp65fo-F3A&usqp=CAU')
        embed.set_footer(icon_url=ctx.message.author.avatar_url,
                         text="Press 'q' to quit | 'y/n/yes/no' for Y/N questions")
        return embed

    def quit():
        ctxsend("Yeetus a feetus")
        embed.clear_fields()
        embed.title="Aborting Creation..."
        return embed

    def check(message):
        try:
            return ctx.message.author == message.author
        except commands.CommandInvokeError:
            return False

    await ctx.send(embed=ctxsend(f"Welcome to your custom role customizer. Your role will be created as {name}\
                    \nContinue? Y/N"))
    resume = await client.wait_for('message', check=check, timeout=20)
    if not(resume.content.lower() == "y" or resume.content.lower() == "yes"):
        return await ctx.send(embed=quit())

    embed.insert_field_at(index=0, name="Administrator Permissions:",
                          value="""administrator\nban_members\
                          \nkick_members\nmanage_channels\nmanage_emojis\
                          \nmanage_guild\nmanage_messages\nmanage_nicknames\
                          \nmanage_permissions\nmanage_roles\nmanage_webhooks\
                          \nmention_everyone\nview_audit_log\nview_guild_insights""",
                          inline=True)
    embed.insert_field_at(index=1, name="Member Permissions",
                          value="""change_nickname\nadd_reactions\nattach_files\
                          \ncreate_instant_invite\nembed_links\
                          \nexternal_emojis\nread_message_history\nread_messages\
                          \nsend_messages\nsend_tts_messages\
                          \nuse_external_emojis\nuse_slash_commands\nview_channel""",
                          inline=True)
    embed.insert_field_at(index=2, name="Voice Channel Permissions",
                          value="""connect\nspeak\nstream\
                          \nuse_voice_activation\nvalue\nrequest_to_speak\
                          \n\n\n---\nmove_members\nmute_members\ndeafen_members\npriority_speaker""",
                          inline=True)
    await ctx.send(embed=ctxsend("Add permissions to your role OR press s to skip.\
                                 \nSeperate permissions by commas. Enter permissions exactly as they appear.\
                                 \nAvaliable permissions are:"))
    permissions_msg = await client.wait_for('message', check=check, timeout=500)
    if (permissions_msg.content.lower() == "q" or permissions_msg.content.lower() == "quit"):
        return await ctx.send(embed=quit())
    elif not (permissions_msg.content.lower() == "skip" or permissions_msg.content.lower() == "s"):
        permissions_list = permissions_msg.content.split(",")
        temp_list = {}
        for permission in permissions_list:
            temp_list[permission.strip()] = True
        permissions = discord.Permissions(**temp_list)
    else:
        permissions = discord.Permissions.membership()

    embed.clear_fields()

    await ctx.send(embed=ctxsend("Enter a RBG seperated by commas OR press s to skip"))
    colour_msg = await client.wait_for('message', check=check, timeout=300)
    if colour_msg.content.lower() == "q" or colour_msg.content.lower() == "quit":
        return await ctx.send(embed=quit())
    elif colour_msg.content.lower() == "skip" or colour_msg.content.lower() == "s":
        colour = discord.Colour.default()
    else:
        rgb = colour_msg.content.split(",")
        colour = discord.Colour.from_rgb(r=int(rgb[0]), g=int(rgb[1]), b=int(rgb[2]))

    await ctx.send(embed=ctxsend("Should the role be shown separately in the member list? Y/N"))
    hoist_msg = await client.wait_for('message', check=check, timeout=100)
    if hoist_msg.content.lower() == "q" or hoist_msg.content.lower() == "quit":
        return await ctx.send(embed=quit())
    elif (hoist_msg.content.lower == "y" or hoist_msg.content.lower() == "yes"):
        hoist = True
    else:
        hoist = False
    print(hoist)

    await ctx.send(embed=ctxsend("Should the role be mentionable? Y/N"))
    mentionable_msg = await client.wait_for('message', check=check, timeout=100)
    if (mentionable_msg.content.lower() == "q" or mentionable_msg.content.lower() == "quit"):
        return await ctx.send(embed=quit())
    elif (mentionable_msg.content.lower == "y" or mentionable_msg.content.lower() == "yes"):
        mentionable = True
    else:
        mentionable = False
    print(mentionable)

    await ctx.send(embed=ctxsend(f"Creating role with the name: {name}\npermissions: {permissions},\
                                    \ncolour: {colour}\nhoist: {hoist}\nmentionable: {mentionable}\
                                    \nContinue? Y/N"))
    resume = await client.wait_for('message', check=check, timeout=20)
    if not (resume.content.lower() == "y" or resume.content.lower() == "yes"):
        return await ctx.send(embed=quit())
    else:
        await ctx.guild.create_role(name=name,
                                    permissions=permissions,
                                    colour=colour,
                                    hoist=hoist,
                                    mentionable=mentionable)
    await ctx.send(embed=ctxsend(f"Role `{name}` created!"))

""" - error check for .createrole command """
@createrole.error
async def createrole_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Syntax: .createrole [role name]")
    elif isinstance(error, discord.Forbidden):
        await ctx.send(f"I need `Manage roles` in order to do that!\
                        Please check my permissions and try again.")

""" - repeats back what user says """
@client.command()
async def say(ctx, *, message):
    await ctx.message.delete()
    await ctx.send(message)

""" - logs a deleted message """
@client.event
async def on_message_delete(message):
    embed = discord.Embed(title=f"Message by {message.author} deleted in {client.get_channel(message.channel.id)}",
                          description=message.content,
                          inline=True)
    embed.set_footer(icon_url=message.author.avatar_url, text=f"Today at HOW DO I ADD TIME")
    await message.guild.system_channel.send(embed=embed)

@client.event
async def on_bulk_message_delete(messages):
    embed = discord.Embed(title=f"Bulk messages deleted in {client.get_channel(messages[0].channel.id)}",
                          description=f"{len(messages)} messages deleted")
    embed.set_footer(icon_url=messages[0].author.avatar_url, text=f"Today at HOW DO I ADD TIME")
    await messages[0].guild.system_channel.send(embed=embed)

extensions = ['cogs.amongus']

if __name__ == '__main__':
  for ext in extensions:
    client.load_extension(ext)
client.run(token)
