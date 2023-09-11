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




bot = commands.Bot("$", intents=discord.Intents.all())


allowed_user_ids = [761769388335431690, 984481582826020905, 964374501343236096, 707782594418442270, 1097879047213686875] # This is for users to access the echo command.

word_list = ["king", "minecraft", "wumbee", "orange", "imagine", "ban", "alternate", "hakurei", "ng", "king of fighters", "nintendo", "fight", "python", "aleph", "tekken", "cod", "combat master", "cemu", "poop", "jabascript", "kong", "snek", "snek", "bro", "net", "oboro", "discord", "keyboard", "why", "sega", "rat", "fuck", "mark", "what", "bite", "dog", "slayer", "dragon", "gay", "shit", "ceaser", "me", "stress", "bird", "corn", "snake", "cat"]
attempts = 6
current_word = ""
current_progress = []


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


if os.path.exists('user_data.json'):
    with open('user_data.json', 'r') as file:
        user_data = json.load(file)
else:
    user_data = {}



@bot.event
async def on_ready():
    print(f"logged as {bot.user}")
    change_status.start()


@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return

    game = bot.get_cog('SnakeGame')
    if game and game.message and after.id == game.message.id:
        await after.delete()


@tasks.loop(seconds=5)
async def change_status():
  await bot.change_presence(activity=discord.Game(random.choice(["hehehe", "haaaaaaaaaaaaa"])))



@bot.event
async def on_message(message):

    if message.content == "uh oh":
        await message.channel.send("https://cdn.discordapp.com/attachments/1122408339570180147/1137485909453971506/mc.jpg", reference=message)

    if message.content == "mario":
        await message.channel.send("https://media.discordapp.net/attachments/1122408339570180147/1140644983037239336/world-1-1.gif", reference=message)

    if message.content == "whar":
        await message.channel.send("https://tenor.com/view/kiby-funkdela-funkdela-catalog-licorice-cookie-gif-26247566", reference=message)

    if message.content == "mad":
        await message.channel.send("https://cdn.discordapp.com/attachments/1119245853203386378/1131887991091101766/C750CA33-927B-441F-B702-F0F2F4334568.gif", reference=message)
    else:
        await bot.process_commands(message)


@bot.command(name='wordle')
async def wordle(ctx):
    global current_word, current_progress
    current_word = random.choice(word_list)
    current_progress = ['▫️' for _ in current_word]
    
    message = await ctx.send(f"Wordle has started! You have {attempts} attempts. Current progress: {' '.join(current_progress)}")
    await message.add_reaction('🟩')  # Green color square emoji for correct letter
    await message.add_reaction('🟨')  # Yellow color square emoji for misplaced letter

@bot.command(name='word')
async def word(ctx, *, guessed_word: str):
    global attempts, current_word, current_progress
    
    if len(guessed_word) != len(current_word):
        await ctx.send("Your guessed word has the wrong length. Please enter a word with the correct length.")
        return
    
    if guessed_word == current_word:
        await ctx.send(f"Congratulations! You've guessed the word: {current_word}")
        attempts = 6
        current_word = ""
        current_progress = []
        return
    
    if attempts > 1:
        attempts -= 1
        feedback_message = await ctx.send(f"Incorrect guess. You have {attempts} attempts left. Current progress: {' '.join(current_progress)}")
        
        for i in range(len(current_word)):
            if guessed_word[i] == current_word[i]:
                current_progress[i] = '🟩'  # Green color square emoji for correct letter
            elif guessed_word[i] in current_word:
                current_progress[i] = '🟨'  # Yellow color square emoji for misplaced letter
        await feedback_message.edit(content=f"Incorrect guess. You have {attempts} attempts left. Current progress: {' '.join(current_progress)}")
    else:
        await ctx.send(f"You've run out of attempts! The word was {current_word}.")
        attempts = 6
        current_word = ""
        current_progress = []

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
async def ascii(ctx):
    art = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣶⣿⣿⣷⣶⣄⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣾⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⡟⠁⣰⣿⣿⣿⡿⠿⠻⠿⣿⣿⣿⣿⣧⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⠏⠀⣴⣿⣿⣿⠉⠀⠀⠀⠀⠀⠈⢻⣿⣿⣇⠀⠀⠀
⠀⠀⠀⠀⢀⣠⣼⣿⣿⡏⠀⢠⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠈⣿⣿⣿⡀⠀⠀
⠀⠀⠀⣰⣿⣿⣿⣿⣿⡇⠀⢸⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⡇⠀⠀
⠀⠀⢰⣿⣿⡿⣿⣿⣿⡇⠀⠘⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⢀⣸⣿⣿⣿⠁⠀⠀
⠀⠀⣿⣿⣿⠁⣿⣿⣿⡇⠀⠀⠻⣿⣿⣿⣷⣶⣶⣶⣶⣶⣿⣿⣿⣿⠃⠀⠀⠀
⠀⢰⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀
⠀⢸⣿⣿⡇⠀⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠉⠛⠛⠛⠉⢉⣿⣿⠀⠀⠀⠀⠀⠀
⠀⢸⣿⣿⣇⠀⣿⣿⣿⠀⠀⠀⠀⠀⢀⣤⣤⣤⡀⠀⠀⢸⣿⣿⣿⣷⣦⠀⠀⠀
⠀⠀⢻⣿⣿⣶⣿⣿⣿⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣦⡀⠀⠉⠉⠻⣿⣿⡇⠀⠀
⠀⠀⠀⠛⠿⣿⣿⣿⣿⣷⣤⡀⠀⠀⠀⠀⠈⠹⣿⣿⣇⣀⠀⣠⣾⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣦⣤⣤⣤⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢿⣿⣿⣿⣿⣿⣿⠿⠋⠉⠛⠋⠉⠉⠁⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠁
    """
    await ctx.send(f"Here amongsus for you:\n```\n{art}\n```")


@bot.command()
async def number(ctx):
    await ctx.send("Welcome to the guessing game! I'm thinking of a number between 1 and 100. Start guessing!")

    # Generate a random number between 1 and 100
    secret_number = random.randint(1, 100)
    
    while True:
        def check(message):
            return message.author == ctx.author and message.content.isdigit()

        try:
            user_guess = await bot.wait_for('message', check=check, timeout=30)
            guess = int(user_guess.content)
            
            if guess < secret_number:
                await ctx.send("Too low! Guess higher.")
            elif guess > secret_number:
                await ctx.send("Too high! Guess lower.")
            else:
                await ctx.send(f"Congratulations! You guessed the correct number: {secret_number}")
                break  # Exit the loop when the user guesses correctly

        except asyncio.TimeoutError:
            await ctx.send("Time's up! The secret number was: {secret_number}")
            break


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
    for i in range(amount): # Do the next thing amount times
        await ctx.send(message) # Sends message where command was called


@bot.command()
async def react(ctx):
    def check(reaction, user):  # Our check for the reaction
        return user == ctx.message.author  # We check that only the authors reaction counts

    await ctx.send("React to this for a test")  # Message to react to

    reaction = await bot.wait_for("reaction_add", check=check)  # Wait for a reaction
    await ctx.send(f"You reacted with: {reaction[0]}")  # With [0] we only display the emoji


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
async def activity(ctx, user: discord.Member):
    try:
        for activity in user.activities:
            if activity.type == discord.ActivityType.playing:
                await ctx.send(f"{user.name} is playing {activity.name}")
                return
        await ctx.send(f"{user.name} is not playing anything.")
    except discord.NotFound:
        await ctx.send("User not found.")

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

@bot.command()
async def gnight(ctx):
    try:
        os.remove("condition")
        sys.exit(0)
    except:
        await ctx.reply("faild to kill")


@bot.command()
async def reboot(ctx):
    try:
        sys.exit(0)
    except:
        await ctx.reply("faild to reboot")



@bot.command()
async def timer(ctx):
    await ctx.send("Setting a timer for 3 days")

    majoras_mask_gif_url = "https://tenor.com/view/majoras-mask-zelda-moon-crash-gif-20298361"
    await ctx.send(majoras_mask_gif_url)

    duration_seconds = 3 * 24 * 60 * 60
    
    await asyncio.sleep(duration_seconds)

    await ctx.send("You met with a terrible fate haven't you")

 # spamming in dms

@bot.command()
async def dm_spam(ctx, user: discord.User, times: int, *, message: str):
    for _ in range(times):
        await user.send(message)
        await ctx.message.delete()


bot.run(os.environ['TOKEN'])
