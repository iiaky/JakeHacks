""" -- Hey I don't know how to optimize code please don't judge --
    -- Admin commands and stuff at the end -- """

import discord
import numpy as np
import numpy.random
from discord.ext import commands
import asyncio

token = open("token.txt", "r").read()
intents = discord.Intents.default()
intents.members = True

colors = ("Red", "Green", "Blue", "Yellow", "Black", "White", "Cyan", "Lime")
colors_choice = np.random.choice(colors)
tasks = {"commontasks": ["Swipe card", "Fix wiring"],
         "shorttasks": ["Clean filter", "Prime shields"],
         "longtasks": ["Upload data", "Submit scan"]}

task_list = {"Swipe card": ["Fill in the blank", "Card swipe task"]}

commontasks_bank = {"Never drink _ _ _ _ _   _ _ potions at 3 AM!": "among us",
                    "I saw you _ _ _ _ !": "vent",
                    "Lolz a _ _ _ _ _ baka xd": "sussy",
                    "Shut the _ _ _ _ up about among us": "FUCK",
                    "Unspeak,  _ _ _ _ _ lord": "cringe"}

killmessage = {"Crewmate" : [f"You have been killed by {colors_choice}",
                             f"Get absolutely destroyed by {colors_choice}",
                             f"You perished from inferiority complex thanks to {colors_choice}",
                             f"A wild {colors_choice} appeared! Brain exploded! Life gone!!"],

               "Imposter" : [f"You killed {colors_choice}!",
                             f"You destoryed {colors_choice}",
                             f"You asserted your dominance on {colors_choice},"
                             f"A bullet went through {colors_choice}'s head."
                             f"STABBY STAB HEHE KNIFE GO STABERS RIP {colors_choice} LL"]}

killmessage_choice = []

client = commands.Bot(command_prefix='.', intents=intents)

class Roles:
    def __init__(self):
        self.commontask = self.choose_tasks("commontasks")
        self.shorttask = self.choose_tasks("shorttasks")
        self.longtask = self.choose_tasks("longtasks")
        self.susmeter = 0

    def choose_tasks(self, task_type):
        return numpy.random.choice(tasks[task_type])

    def kill(self):
        encounterchance = 0.2
        encounterchoice = numpy.random.choice([True, False], p=[encounterchance, 1-encounterchance])
        global killmessage_crew

        if encounterchoice:
            encounterchance = 0.2
            killmessage_choice.append(numpy.random.choice(killmessage[self.role]))
            return True
        else:
            encounterchance += 0.15
            return False


class Crewmate(Roles):
    def __init__(self):
        super().__init__()
        self.role = "Crewmate"
        self.killmessage = []



class Imposter(Roles):
    def __init__(self):
        super().__init__()
        self.role = "Imposter"


async def card_swipe_task(ctx):
    def check(reaction):
        print(ctx.message.author, reaction.author, reaction.id)
        try:
            return ctx.message.author == reaction.author and reaction.id == '\U0001F7E2'
        except commands.CommandInvokeError:
            return False

    card_msg = await ctx.send(f"React with :green_circle: when the bar reaches full!")
    card_swipe = ("```▱▱▱▱▱▱▱▱▱▱```", "```▰▱▱▱▱▱▱▱▱▱```", "```▰▰▱▱▱▱▱▱▱▱```", "```▰▰▰▰▱▱▱▱▱▱```",
                  "```▰▰▰▰▰▰▱▱▱▱```", "```▰▰▰▰▰▰▰▰▰▱```", "```▰▰▰▰▰▰▰▰▰▰```")

    await card_msg.add_reaction('\U0001F7E2')
    i=0
    while i<len(card_swipe):
        try:
            await client.wait_for('reaction_add', check=check, timeout=0.7)
        except asyncio.TimeoutError:
            await card_msg.edit(content=card_swipe[i])
            if i == (len(card_swipe)-1):
                await asyncio.sleep(1.5)
        else:
            if card_msg.content == '"```▰▰▰▰▰▰▰▰▰▰```"':
                ctx.send("You successfully swiped the card!")
                return
            else:
                ctx.send("You failed to swipe the card! (Dude how hard is it to react properly)")
                return
        i+=1

def fill_in_the_blank():
    key, answer = zip(*commontasks_bank["Fill in the blank"].items())
    question = numpy.random.choice(key)
    return question

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

@client.command()
async def play(ctx):

    def check(message):
        try:
            return message.author == ctx.message.author
        except commands.CommandInvokeError:
            return False

    rolelist = {"Imposter": 0.2, "Crewmate": 0.8}
    name, weight = zip(*rolelist.items())
    role_choice = np.random.choice(name, p=weight)
    if role_choice == "Imposter":
        role = Imposter()
    if role_choice == "Crewmate":
        role = Crewmate()
    await ctx.send(f"```Generating virtual world...You are {role.role}```")  # setting role
    """starting = await ctx.send("```Vibing in space\
                            \n\t□□□□□□□□□□```")
    await asyncio.sleep(0.5)
    await starting.edit(content="```Awaiting landing...\
                            \n\t■□□□□□□□□□```")
    await asyncio.sleep(1)
    await starting.edit(content="```Landed safely!\
                            \n\t■■■□□□□□□□```")
    await asyncio.sleep(1)
    await starting.edit(content="```Loading air tank, checking pressure...\
                            \n\t■■■■■□□□□□```")
    await asyncio.sleep(1)
    await starting.edit(content="```Watering plants\
                            \n\t■■■■■■□□□□```")
    await asyncio.sleep(0.5)
    await starting.edit(content="```Unloading trash chute\
                            \n\t■■■■■■■■□□```")
    await asyncio.sleep(0.5)
    await starting.edit(content="```Ready to go!\
                            \n\t■■■■■■■■■■```")"""

    if role.commontask == "Swipe card":  # card swipe task
        msg_display = {"Crewmate": ["Nyooming to admin...", "Go to admin you nerd"],
                       "Imposter": ["You are faking card swipe...", "Ultimate stealth mode in admin"]}

        task = numpy.random.choice(["Fill in the blank", "Card swipe task"])  # setting "game"
        await asyncio.sleep(1)
        await ctx.send(f'```{numpy.random.choice(msg_display[role_choice])}\
                        \n\tYour task is: Swipe card\
                        \n\tTask: {task}```')

        if task == "Card swipe task":
            await ctx.send(await card_swipe_task(ctx))
        if task == "Fill in the blank":
            task_result = fill_in_the_blank()
            fitb_Embed = discord.Embed(title="Fill in the blank",
                                       description=f"Fill in the missing word! You have 10 seconds\
                                       \n`{task_result}`",
                                       color=0xd6ffe8)
            fitb_Embed.set_thumbnail(url='https://i.pinimg.com/originals/6c/fd/65/6cfd65d719d5f01b815a24c6f47e5ca9.jpg')
            fitb_Embed.set_footer(text=f'This bot was made by {client.get_user(215897727983288320)}')
            await ctx.send(embed=fitb_Embed)
            try:
                task_msg = await client.wait_for('message', check=check, timeout=10)
            except asyncio.TimeoutError:
                await ctx.send(f'Too slow! The answer is {commontasks_bank[task_result]}')
                caught = np.random.choice([True, False], p=(0.35, 0.65))
                if caught:
                    await ctx.send(f"{colors_choice} killed you for being an idiot")
                else:
                    await ctx.send("Kinda sus!!!")
                    role.susmeter += 1
            if task_msg.content.lower() == commontasks_bank[task_result].lower():
                await ctx.send(f"Correct! The answer is {commontasks_bank[task_result]}")
            else:
                await ctx.send(f"You fucking idiot. The answer is {commontasks_bank[task_result]}")
                caught = np.random.choice([True, False], p=(0.35, 0.65))
                if caught:
                    await ctx.send(f"{colors_choice} killed you for being such a dumbass")
                else:
                    await ctx.send("Wrong answer? That's real sus... My susometer is really sussing you out right now")
                    role.susmeter += 1

    elif role.commontask == "Fix wiring":
        await ctx.send(f'Your task is: Fix wiring\n\
                       {np.random.choice(["Nyooming to electrical", "Fix the wires sir"])}')
        if type(role) == Crewmate:
            await ctx.send(f"tasknotfound(yet) (im uncreative")
        elif type(role) == Imposter:
            await ctx.send(f"You are faking wires.")

    role.kill()
    if role.kill():
        await ctx.send(killmessage_choice[-1])
        return

""" -- beautiful command -- """
@client.command()
async def aum(ctx):
    sus = True

    def check(message):
        try:
            return message.content == "stop" and ctx.message.author == message.author
        except commands.CommandInvokeError:
            return False

    while sus:
        try:
            message = await client.wait_for('message', check=check, timeout=1)
        except asyncio.TimeoutError:
            await ctx.send("amongus")
        else:
            if message:
                sus = False
    await ctx.send("amongus stopped")


""" -- hey look some commands where you actually don't lose brain cells ! -- """

""" - purges channel, checks for perms """
@client.command()
@commands.has_guild_permissions(manage_messages=True)
@commands.bot_has_guild_permissions(manage_messages=True)
async def purge(ctx, amount=5):
    print(amount)
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

""" - update status (thanks jayjay ;-;) """
@client.command()
async def playing(ctx, *, status):
    await client.change_presence(activity=discord.Game(name=status))
    await ctx.message.add_reaction("\U0001F34B")

""" - updates a user's roles """
@client.command()
@commands.has_guild_permissions(manage_roles=True)
# @commands.bot_has_guild_permissions(manage_roles=True)
async def giverole(ctx, users:commands.Greedy[discord.Member] = client.user, *, role:discord.Role = ' '):
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

    embed.insert_field_at(index=0, name = "Administrator Permissions:",
                          value = """administrator\nban_members\
                          \nkick_members\nmanage_channels\nmanage_emojis\
                          \nmanage_guild\nmanage_messages\nmanage_nicknames\
                          \nmanage_permissions\nmanage_roles\nmanage_webhooks\
                          \nmention_everyone\nview_audit_log\nview_guild_insights""",
                          inline = True)
    embed.insert_field_at(index=1, name = "Member Permissions",
                          value = """change_nickname\nadd_reactions\nattach_files\
                          \ncreate_instant_invite\nembed_links\
                          \nexternal_emojis\nread_message_history\nread_messages\
                          \nsend_messages\nsend_tts_messages\
                          \nuse_external_emojis\nuse_slash_commands\nview_channel""",
                          inline = True)
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
        permissions_list=permissions_msg.content.split(",")
        temp_list={}
        for permission in permissions_list:
            temp_list[permission.strip()]=True
        permissions=discord.Permissions(**temp_list)
        print(permissions)
    else:
        permissions=discord.Permissions.membership()

    embed.clear_fields()

    await ctx.send(embed=ctxsend("Enter a RBG seperated by commas OR press s to skip"))
    colour_msg = await client.wait_for('message', check=check, timeout=300)
    if (colour_msg.content.lower() == "q" or colour_msg.content.lower() == "quit"):
        return await ctx.send(embed=quit())
    elif colour_msg.content.lower() == "skip" or colour_msg.content.lower() == "s":
        colour = discord.Colour.default()
    else:
        rgb=colour_msg.content.split(",")
        colour=discord.Colour.from_rgb(r=int(rgb[0]), g=int(rgb[1]), b=int(rgb[2]))

    await ctx.send(embed=ctxsend("Should the role be shown separately in the member list? Y/N"))
    hoist_msg = await client.wait_for('message', check=check, timeout=100)
    if (hoist_msg.content.lower() == "q" or hoist_msg.content.lower() == "quit"):
        return await ctx.send(embed=quit())
    elif (hoist_msg.content.lower == "y" or hoist_msg.content.lower() == "yes"):
        hoist=True
    else:
        hoist=False
    print(hoist)

    await ctx.send(embed=ctxsend("Should the role be mentionable? Y/N"))
    mentionable_msg = await client.wait_for('message', check=check, timeout=100)
    if (mentionable_msg.content.lower() == "q" or mentionable_msg.content.lower() == "quit"):
        return await ctx.send(embed=quit())
    elif (mentionable_msg.content.lower == "y" or mentionable_msg.content.lower() == "yes"):
        mentionable=True
    else:
        mentionable=False
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

client.run(token)
