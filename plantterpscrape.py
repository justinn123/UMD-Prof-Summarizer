import planetterp
import json
import discord
from discord.ext import commands


intents = discord.Intents.default()

client = commands.Bot(command_prefix='$', intents=intents)
TOKEN = "MTExNjkyMTY5Mzk4Njg4NTY5Nw.GVgtw9.8-C7xrQI_f7LelqxXeNL8FIL2EI0ZIatX8YNcw"


@client.event
async def on_ready():
    print(f"{client.user} is ready")

@client.command()
async def rankProf(ctx, courseValue):
    try:
        course = planetterp.course(name=courseValue)  
        prof_list = course["professors"]
    except:
        await ctx.channel.send(f"Could not find course")

    prof_score = []
    for x in prof_list:
        prof = json.dumps(planetterp.professor(name=x))
        prof = json.loads(prof)
        if(prof["average_rating"] != None):
            prof_score.append(float('{0:.2f}'.format(prof["average_rating"])))
        else:
            prof_score.append(-1)

    prof_dictionary = dict(zip(prof_list, prof_score))
    ranked = dict(sorted(prof_dictionary.items(), key = lambda item: item[1],reverse = True))
    ranked_str = ""
    counter = 1
    
    for key in ranked:
        if ranked[key] == -1:
            ranked_str+=str(f"{counter} {key}: None")
        else:
            ranked_str+=str(f"{counter}) {key}: {ranked[key]}")
        ranked_str+=("\n")
        counter+=1
    await ctx.channel.send(f"{ranked_str}")

client.run(TOKEN)
