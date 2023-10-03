import planetterp
import json
import discord
from discord.ext import commands


intents = discord.Intents.default()

client = commands.Bot(command_prefix='$', intents=intents)
TOKEN = "TOKEN"

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

@client.command()
async def getGPA(ctx, courseName, *, prof):
    grades = planetterp.grades(course = str(courseName), professor=str(prof))
    counter = 0
    total = 0

    grade_weights = {
        "A+": 4,
        "A": 4,
        "A-": 3.7,
        "B+": 3.3,
        "B": 3,
        "B-": 2.7,
        "C+": 2.3,
        "C": 2,
        "C-": 1.7,
        "D+": 1.3,
        "D": 1,
        "D-": .7
    }

    for x in grades:
        for grade, weight in grade_weights.items():
            total += x[grade] * weight
            counter += x[grade]

# Calculate the average GPA if counter is not zero
    if counter != 0:
        average_gpa = total / counter
    await ctx.channel.send(f"Average GPA: {average_gpa:.2f}")
client.run(TOKEN)
