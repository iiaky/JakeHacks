""" -- Hey I don't know how to optimize code please don't judge -- """

import discord
import numpy as np
import numpy.random
from discord.ext import commands
import asyncio

token = open("token.txt", "r").read()

colors = ("Red", "Green", "Blue", "Yellow", "Black", "White", "Cyan", "Lime")
colors_choice = np.random.choice(colors)
tasks = {"commontasks" : ["Swipe card", "Fix wiring"],
            "shorttasks" : ["Clean filter", "Prime shields"],
            "longtasks" : ["Upload data", "Submit scan"]}

task_list = {"Swipe card" : ["Fill in the blank", "Card swipe task"]}

commontasks_bank = {"Fill in the blank": {"Never drink _ _ _ _ _   _ _ potions at 3 AM!" : "among us",
                     "I saw you _ _ _ _ !" : "vent",
                     "Lolz a _ _ _ _ _ baka xd" : "sussy",
                     "Shut the _ _ _ _ up about among us" : "FUCK",
                     "This is so fucking _ _ _ _ _ _ _ _ _" : "cancerous"},
                    "Card swipe task" : "boop!"}

killmessage_crew = [f"You have been killed by {colors_choice}",
                    f"Get absolutely fucked by {colors_choice}",
                    f"{colors_choice} did ya mahm and you perished from inferiority complex.",
                    f"A wild {colors_choice} appeared! Brain exploded! Life gone!!"]

killmessage_imp = [f"You killed {colors_choice}!",
                   f"You destoryed {colors_choice}'s mom",
                   f"You asserted your dominance on {colors_choice},"
                   f"A bullet went through {colors_choice}'s head. Huh, who did that?"
                   f"STABBY STAB HEHE KNIFE GO STABERS RIP {colors_choice} LLLLL"]

killmessage_choice =[]

client = commands.Bot(command_prefix = '.')

class Crewmate():
    def __init__(self):
        self.role = "Crewmate"
        self.killmessage = []
        self.commontask = self.choose_tasks("commontasks")
        self.shorttask =self.choose_tasks("shorttasks")
        self.longtask = self.choose_tasks("longtasks")
        self.susmeter = 0

    def choose_tasks(self, task_type):
        global killmessage_crew
        return numpy.random.choice(tasks[task_type])

    def kill(self):
        encounterchance = 0.2
        encounterchoice = numpy.random.choice([True, False], p = [encounterchance, 1-encounterchance])
        global killmessage_crew

        if encounterchoice:
            encounterchance = 0.2
            killmessage_choice.append(numpy.random.choice(killmessage_crew))
            return True
        else:
            encounterchance += 0.15
            return False

class Imposter():
    def __init__(self):
        self.role = "Imposter"
        self.commontask = self.choose_tasks("commontasks")
        self.shorttask = self.choose_tasks("shorttasks")
        self.longtask = self.choose_tasks("longtasks")
        self.susmeter = 0

    def choose_tasks(self, task_type):
        return numpy.random.choice(tasks[task_type])

    def kill(self):
        encounterchance = 0.2
        killing = np.random.choice([True, False], p = [encounterchance, 1-encounterchance])
        if killing:
            encounterchance = 0.2
            killmessage_choice.append(numpy.random.choice(killmessage_imp))
            return True
        else:
            encounterchance += 0.1
            return False

async def do_task(role, task, ctx):
    if task == "Card swipe task":
        card_msg = await ctx.send(f"React with :green_circle: when the bar reaches full!")
        await card_msg.add_reaction('\U0001F7E2')
        boop = "beep"
        await asyncio.sleep(1)
        await card_msg.edit(content = "'''▱▱▱▱▱▱▱▱▱▱```")
        await asyncio.sleep(1)
        await card_msg.edit(content="'''▰▱▱▱▱▱▱▱▱▱```")
        await asyncio.sleep(1)
        await card_msg.edit(content="'''▰▰▱▱▱▱▱▱▱▱```")
        await asyncio.sleep(0.5)
        await card_msg.edit(content="'''▰▰▰▰▱▱▱▱▱▱```")
        await asyncio.sleep(0.8)
        await card_msg.edit(content="'''▰▰▰▰▰▰▱▱▱▱```")
        await asyncio.sleep(1)
        await card_msg.edit(content="'''▰▰▰▰▰▰▰▰▰▱```")
        await asyncio.sleep(0.8)
        await card_msg.edit(content="'''▰▰▰▰▰▰▰▰▰▰```")
        await asyncio.sleep(1.2)
        boop = "boop"
        return "boop!"

    elif task == "Fill in the blank":
        key, answer = zip(*commontasks_bank.items())
        question = numpy.random.choice(key)
        return question

""" --- ####################################### ---"""

def check(author):
    def inner_check(message):
        return message.author == author
    return inner_check

@client.event
async def on_ready():
    print('whee')

@client.event
async def on_message(message):
    if message.content.startswith('among us'):
        await message.channel.send("fuck off you annoying cunekmasfd")
    await client.process_commands(message)

@client.command()
async def play(ctx):
    rolelist = {"Imposter": 0.2, "Crewmate": 0.8}
    name, weight = zip(*rolelist.items())
    role_choice = np.random.choice(name, p = weight)
    if role_choice == "Imposter":
        role = Imposter()
    if role_choice == "Crewmate":
        role = Crewmate()
    print(type(role))
    await ctx.send(f"```Generating virtual world...You are {role.role}```") # setting role
    starting = await ctx.send("```Awaiting landing...\n\
                        □□□□□□□□□□```")
    await asyncio.sleep(0.5)
    await starting.edit(content = "```Landed safely!\n\
                        ■□□□□□□□□□```")
    await asyncio.sleep(1)
    await starting.edit(content="```Loading air tank, checking pressure...\n\
                            ■■■□□□□□□□```")
    await asyncio.sleep(1)
    await starting.edit(content="```The possibilty of suffocation is great\n\
                                ■■■■■□□□□□```")
    await asyncio.sleep(1)
    await starting.edit(content="```Doing ya mum\n\
                                    ■■■■■■□□□□```")
    await asyncio.sleep(0.25)
    await starting.edit(content="```Finishing your hent*i...\n\
                                    ■■■■■■■■□□```")
    await asyncio.sleep(1)
    await starting.edit(content="```Ready to go!\n\
                                     ■■■■■■■■■■```")


    if role.commontask == "Swipe card": # card swipe task
        msg_display = {"Crewmate": ["Nyooming to admin...", "Go to admin you nutsack"],
                       "Imposter": ["You are faking card swipe...", "Ultimate stealth mode in admin gogogo"]}

        task = numpy.random.choice(["Fill in the blank", "Card swipe task"]) # setting "game"
        task_result = do_task(role, task, ctx)
        await ctx.send(f'{numpy.random.choice(msg_display[role_choice])}\n\n\
                        Your task is: Swipe card\n\
                        Task: {task}\n\n\
                        `{task_result}`')
        task_msg = await client.wait_for('message', check = check, timeout = 10)
        if task_msg.content.lower() == commontasks_bank[task][task_result].lower():
            await ctx.send(f"Correct! The answer is {commontasks_bank[task][task_result]}")
        else:
            await ctx.send(f"You fucking idiot. The answer is {commontasks_bank[task][task_result]}")
            caught = np.random.choice([True, False], p = (0.35, 0.65))
            if caught:
                await ctx.send(f"{colors_choice} killed you for being such a dumbass fuck")
            await ctx.send("Wrong answer? That's real sus... My susometer is really sussing you out right now")
            role.susmeter += 1

    elif role.commontask == "Fix wiring":
        await ctx.send(f'Your task is: Fix wiring\n\
                       {np.random.choice(["Nyooming to electrical", "Fix the wires bitch"])}')
        if type(role) == Crewmate:
            await ctx.send(f"TASK TBA (im uncreative")
        elif type(role) == Imposter:
            await ctx.send(f"You are faking wires.")

    role.kill()
    if role.kill():
        await ctx.send(killmessage_choice[-1])
        return

    if role.shorttask == "Clean filter" :
        await ctx.send(np.random.choice(["Go do your job you garbageboy",
                                         "Scurry through the trash, bitch"]))
        if type(role) == Crewmate:
            await ctx.send(f"Fulfilling your future of being a garbageman")
        elif type(role) == Imposter:
            await ctx.send(f"You are faking being a garbageman. What are you, a loser?")

    elif role.shorttask == "Prime shields" :
        await ctx.send(np.random.choice(["Going to prime shields...",
                                         "**BAZINGA**"]))

    if role.longtask == "Upload data" :
        await ctx.send(np.random.choice(["Going to data to upload fornication content, probably",
                                         "Go to admin you nutsack"]))
    elif role.longtask == "Submit scan" :
        await ctx.send(np.random.choice(["Scanning ... your mom",
                                         "Nyooming to medical!"]))
@client.command()
async def amongusmode(ctx):
    async def amongusloop(loop):
        await ctx.send("amongus")
        await asyncio.sleep(1.5)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.ensure_future(amongusloop(loop))
    if client.on_message("stop"):
        loop.stop()

client.run(token)