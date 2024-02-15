import planetterp
import discord
from discord.ext import commands
from functions.rankCourses import rankDep
from functions.rankProfGpa import *

TOKEN = "MTExNjkyMTY5Mzk4Njg4NTY5Nw.Gz_vZB.8cYYqq3160vbDaxuiNrv8ywy4INqi0U7p1mbFI"

intents = discord.Intents.all()
client = commands.Bot(command_prefix='$', intents=intents)


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
        return
    
    prof_score = []
    for x in prof_list:
        prof = planetterp.professor(name=x)
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
            ranked_str+=str(f"{counter}) {key}: None")
        else:
            ranked_str+=str(f"{counter}) {key}: {ranked[key]}")
        ranked_str+=("\n")
        counter+=1
    await ctx.channel.send(f"{ranked_str}")


@client.command()
async def getGPA(ctx, courseName, *, prof):
    average_gpa = calcGPA(courseName, prof)
    if(average_gpa == -1):
        await ctx.channel.send(f"No Data")
        return
    await ctx.channel.send(f"Average GPA: {average_gpa:.2f}")


@client.command()
async def rankGPA(ctx, courseVal):
    list = rankByGPA(courseVal)
    await ctx.channel.send(list)
    

@client.command()
async def rankCourses(ctx, department, level):
    list = rankDep(department, level)
    if list != "" and list != None: 
        await ctx.channel.send(f"{list}")
    else:
        await ctx.channel.send(f"There was an error")

client.run(TOKEN)