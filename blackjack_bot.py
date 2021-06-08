import discord
from discord import embeds
from discord.ext import commands
from collections import defaultdict
import random

bot = commands.Bot(command_prefix='!')
# individual player scores that reset once players get to 21 or over
user_scores = defaultdict(int)
# the total scores that represent how many times a player has won blackjack, to be displayed on the leaderboard
total_scores = defaultdict(int)

@bot.command(name = "play", help = "Play blackjack and try to get to 21!")
async def blackjack(ctx, game : str):
    if game == "blackjack":
        await ctx.send("Dealing your card...")

        user_id = ctx.author 
        cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        random_card = random.choice(cards)

        if random_card == '2':
            user_scores[user_id] += 2
        elif random_card == '3':
            user_scores[user_id] += 3
        elif random_card == '4':
            user_scores[user_id] += 4
        elif random_card == '5':
            user_scores[user_id] += 5
        elif random_card == '6':
            user_scores[user_id] += 6
        elif random_card == '7':
            user_scores[user_id] += 7
        elif random_card == '8':
            user_scores[user_id] += 8
        elif random_card == '9':
            user_scores[user_id] += 9
        elif random_card == '10':
            user_scores[user_id] += 10
        elif random_card == 'Jack':
            user_scores[user_id] += 10
        elif random_card == 'Queen':
            user_scores[user_id] += 10
        elif random_card == 'King':
            user_scores[user_id] += 10
        elif random_card == 'Ace':
            # If we are at a score above 10, an Ace value of 11 will bring us over 21, so give Ace a value of 1
            # else Ace value = 11
            if user_scores[user_id] > 10:
                user_scores[user_id] += 1
            elif user_scores[user_id] <= 10:
                user_scores[user_id] += 11    

        if user_scores[user_id] == 21:
            user_scores[user_id] = 0
            await ctx.send("You win!")
        elif user_scores[user_id] > 21:
            loss_message = f'Unfortunate. You got: ' + str(user_scores[user_id]) + ', which is over 21.'
            await ctx.send(loss_message)
            total_scores[user_id] += 1
            user_scores[user_id] = 0                                        
        else:    
            card_message = f'You got a ' + random_card + '! :upside_down_face:'
            await ctx.send(card_message)
            score_message = f'Your score is now: ' + str(user_scores[user_id]) + ', ' + str(user_id)
            await ctx.send(score_message)
            await ctx.send("Type !hit me to play on.")
    else:
        await ctx.send("Invalid game!")   

@bot.command(name = "hit", help = "Continue playing blackjack.")
async def hit(ctx, player : str):
    if player == "me":
        await blackjack(ctx, "blackjack")
    else:
        await ctx.send("Invalid command.")    

@bot.command(name = "leaderboard", help = "Displays the players who win the most at blackjack.")
async def leaderboard(ctx,x = 5):
    to_embed = discord.Embed(title = f"Top {x} Best Blackjack Players", description = "These are the players who have won blackjack the most!", color = discord.Color(0x22ff00))

    index = 1
    for user_id, score in sorted(total_scores.items(), key=lambda item: item[1], reverse=True):
        to_embed.add_field(name = f"{index}. {user_id}", value = str(score), inline = False)
        if index == x:
            break
        else:
            index += 1
    
    await ctx.send(embed = to_embed)

with open("BOT_TOKEN.txt", "r") as token_file:
    TOKEN = token_file.read()
    print("Token file read")
    bot.run(TOKEN)