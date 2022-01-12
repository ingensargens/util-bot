import discord
#from discord import file
#from discord import errors
#from discord import user
from discord.ext import commands
#pillow
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import os
import time
import requests
import numpy as np
from io import BytesIO

file = open('token.txt', 'r')
TOKEN = file.read()

client = commands.Bot(command_prefix = "u!", intents = discord.Intents.all())

#custom color function defined
def color_select(c):
    #new match case from python 3.10+
    match c:
        case 'red':
            return 'red'
        case 'orange':
            return 'orange'
        case 'yellow':
            return 'yellow'
        case 'green':
            return 'green'
        case 'blue':
            return 'blue'
        case 'purple':
            return 'purple'
        case 'pink':
            return 'pink'
        case 'black':
            return 'black'
        case 'white':
            return 'white'             
        case _:
            return '**Color unrecognized. Please try again**.'

#function converting bytes to its equivalant counterpart 
def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

@client.event
async def on_ready():
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    #startup time logging
    print(f'logged in as {client.user} - {current_time}')

#banner command removed due to discord update

#avatar
@client.command(aliases = ["av"])
async def avatar(ctx, userID=""):
    #starting process timer
    start = time.time()
    #if no user id, user id is authors id
    if(userID == ""):
        userID = ctx.author.id
    #fetching the user using user id    
    user = await client.fetch_user(userID)
    #sending the url in either a gif or png format as size 1024
    await ctx.send(user.avatar_url_as(format='png', size=1024))
    #ending process timer
    end = time.time()
    #sending process total time
    await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')

#emote to png
@client.command(aliases = ['emoji'])
async def emote(ctx, emote):
    #starting process timer
    start = time.time()
    #if there is no emote arg
    if(emote == ""):
        #or emote != discord.Emoji
        return await ctx.send("Emote not found. Please provide an emote to transform.")
    else:
        #split the emote string into an array
        emoteArr = emote.split(':')
        emoteID = emoteArr[2]
        #get the png, size 80, using emotes id
        var = f'https://cdn.discordapp.com/emojis/{emoteID}.png?size=1024'
        arr2 = var.split('>')
        newUrl = (str(arr2[0] + arr2[1]))
        #send the png as a url
        await ctx.send(newUrl)
        #ending process timer
        end = time.time()
        #sending process total time
        return await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')
        
#returns a pixelated image of an input attached image
@client.command()
async def pixelate(ctx,scale=16):
    #starting process timer
    start = time.time()
    #get the png by requesting the url
    response = requests.get(ctx.message.attachments[0])
    #open the image
    img = Image.open(BytesIO(response.content))         
    #resize image
    imgSmall = img.resize((scale,scale),resample=Image.BILINEAR)
    #new image back to main size
    result = imgSmall.resize(img.size,Image.NEAREST)
    #save image
    result.save('result.png')
    #send
    await ctx.send(file = discord.File('result.png'))
    #remove image
    os.remove('result.png')
    #ending process timer
    end = time.time()
    #sending process total time
    return await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')

#image to bl + wh
@client.command(aliases = ['gray', 'grey', 'greyscale'])
async def grayscale(ctx):
    #starting process timer
    start = time.time()
    #get the png by requesting the url
    response = requests.get(ctx.message.attachments[0])
    #open the image
    img = Image.open(BytesIO(response.content))  
    result = ImageOps.grayscale(img)
    #save image
    result.save('result.png')
    #send
    await ctx.send(file = discord.File('result.png'))
    #remove image
    os.remove('result.png')
    #ending process timer
    end = time.time()
    #sending process total time
    return await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')

#blending 2 images
@client.command()
async def blend(ctx):
    #starting process timer
    start = time.time()
    #alpha (combination amount) variable
    alpha = 0.5
    #get the png by requesting the url
    image1 = requests.get(ctx.message.attachments[0])
    img1 = Image.open(BytesIO(image1.content))
    image2 = requests.get(ctx.message.attachments[1])
    img2 = Image.open(BytesIO(image2.content))
    #setting a tuple to the width and height of size
    img1w, img1h = img1.size
    img2w, img2h = img2.size
    #if the heights and width of the images are the same, blend
    if((img1w * img1h) == (img2w * img2h)):
        out = Image.blend(img1, img2, alpha)
        #save the image, send it, and delete it
        out.save('result.png')
        await ctx.send(file = discord.File('result.png'))
        os.remove('result.png')
        #ending process timer
        end = time.time()
        #sending process total time
        return await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')
    #else, return a message preventing an error if not same size    
    else:
        return await ctx.send("**Images are not the same size.** Please provide images with same pixel size.")

#color overlay
@client.command(aliases = ['overlay', 'colorize'])
async def tint(ctx, color = 'black'):
    #starting process timer
    start = time.time()
    #requesting the url of the image
    image1 = requests.get(ctx.message.attachments[0])
    img1 = Image.open(BytesIO(image1.content)).convert("L")
    #colorizing the image using a custom function
    result = ImageOps.colorize(img1, black = color_select(color), white ="white")
    #save the image, send it, and delete it
    result.save('result.png')
    await ctx.send(file = discord.File('result.png'))
    os.remove('result.png')
    #ending process timer
    end = time.time()
    #sending process total time
    return await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')
    
#contour
@client.command(aliases = ['outline'])
async def contour(ctx):
    #starting process timer
    start = time.time()
    #get the png by requesting the url
    image1 = requests.get(ctx.message.attachments[0])
    img1 = Image.open(BytesIO(image1.content))
    #result created with contour
    result = img1.filter(ImageFilter.CONTOUR)
    #save the image, send it, and delete it
    result.save('result.png')
    await ctx.send(file = discord.File('result.png'))
    os.remove('result.png')
    #ending process timer
    end = time.time()
    #sending process total time
    return await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')

#information about an image
@client.command()
async def stats(ctx):
    #starting process timer
    start = time.time()
    #get the png by requesting the url
    image1 = requests.get(ctx.message.attachments[0])
    img1 = Image.open(BytesIO(image1.content))
    #creating a discord embed containing information about the attached image
    embed=discord.Embed(title="Image information: ", color=0xad1457)
    embed.add_field(name = "Image name", value=ctx.message.attachments[0].filename, inline=False)
    embed.add_field(name="Format: ", value=img1.format, inline=False)
    #embed.add_field(name="Pixel size: ", value=f'{img1.size}', inline=False)
    embed.add_field(name="Width: ", value=img1.width, inline=False)
    embed.add_field(name="Height: ", value=img1.height, inline=False)
    embed.add_field(name="Mode: ", value=img1.mode, inline=False)
    embed.add_field(name="File size: ", value=convert_bytes(ctx.message.attachments[0].size), inline=False)
    #sending the discord embed
    await ctx.send(embed=embed)
    #ending process timer
    end = time.time()
    #sending process total time
    return await ctx.send(f'`Process finished in: {round(end - start, 4)} seconds.`')
     
#error handler - sends errors through the bot
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")

client.run(str(TOKEN))
file.close()