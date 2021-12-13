import discord
#from discord import errors
#from discord import user
from discord.ext import commands
from PIL import Image, ImageOps
import os
import requests
from io import BytesIO

TOKEN="ODk5MTAzMTQxMjAxNTc1OTg2.YWt5DQ.qBMjqbW8r85MzxUSdA7Bu2BhSO0"
client = commands.Bot(command_prefix = "u!", intents = discord.Intents.all())

@client.event
async def on_ready():
    print(f'logged in as {client.user}')


#banner
@client.command()
async def banner(ctx, userID=""):
    #user defined
    if(userID == ""):
        userID = ctx.author.id
    user = await client.fetch_user(userID)

    #if color
    if(user.accent_color):
        embed = discord.Embed(title = user, color = user.accent_color)
        await ctx.send(embed=embed)
    #if banner gif/image
    elif(user.banner):
        embed = discord.Embed(title = user, color = discord.Color.dark_blue())
        embed.set_image(url = user.banner.url)
        await ctx.send(embed = embed) 
    #neither    
    else:
        await ctx.send("No banner or color to return.")
    
#avatar
@client.command(aliases = "av")
async def avatar(ctx, userID=""):
    if(userID == ""):
        userID = ctx.author.id
    user = await client.fetch_user(userID)
    embed = discord.Embed(title = user, color = discord.Color.dark_blue())
    embed.set_image(url = user.avatar.url)
    await ctx.send(embed = embed)

#returns a pixelated image of an input attached image
@client.command()
async def pixelate(ctx,scale=16):
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

#image to bl + wh
@client.command(aliases = ['gray', 'grey', 'greyscale'])
async def grayscale(ctx):
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

#blending 2 images
@client.command()
async def blend(ctx):
    alpha = 0.5
    #get the png by requesting the url
    image1 = requests.get(ctx.message.attachments[0])
    img1 = Image.open(BytesIO(image1.content))
    image2 = requests.get(ctx.message.attachments[1])
    img2 = Image.open(BytesIO(image2.content))
    img1w, img1h = img1.size
    img2w, img2h = img2.size
    if((img1w * img1h) == (img2w * img2h)):
        out = Image.blend(img1, img2, alpha)
        out.save('result.png')
        await ctx.send(file = discord.File('result.png'))
        os.remove('result.png')
    else:
        return await ctx.send("**Images are not the same size.** Please provide images with same pixel size.")
#error handler
@client.event
async def on_command_error(ctx, error):
    await ctx.send(f"An error occured: {str(error)}")    
client.run(TOKEN)