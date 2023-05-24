from dotenv import load_dotenv
import discord
from discord.ext import commands
import os
import re


load_dotenv()
token = os.getenv('DISCORD_TOKEN')
commMark = os.getenv('COMMAND_MARKER')



description = 'Discord administration bot'


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=commMark, description=description, intents=intents)

#posts log in message on log in
@bot.event
async def on_ready():
    print('Logged on as {bot.user} (ID {bot.user.id})')
    print('-----------')
#------------------------------------------------Functions---------------------------------------------------#

def get_rid(ctx, role_input):
    print("get_rid starting") #debugging - prints once function is called
    
    #cleans input and assigns to role_name
    role_name = role_input.strip()
    print(role_name) 
    
    #first trying regext to get the id from the message itself
    role_id = re.search(r'\d{18}', role_name)
    roles_list = [] #initializing return list
    if role_id != None: #checking if re found something
        role_id = role.id.group(0) # getting readable id
        roles_list.append(int(role_id)) #getting and appending role-id to list
    else:
        #iterating through roles, searching for name match
        for g_role in ctx.guild.roles:
            if role_name in str(g_role.name):
                roles_list.append(int(g_role.id)) #appending to list
    

    print(roles_list) #debugging - prints roles_list
    roleLen = len(roles_list)
    print('length: ' + str(roleLen)) #debugging - prints length of roles_list
    print('get_rid finishing')
    return roles_list, len(roles_list)


#similar function to get_rid, but for retrieving user ID
def getuid(ctx, user_input): 
    print("get_uid starting") #debugging - prints once function is called
    #cleans input and assigns to role_name
    users_list = []
    user_name = user_input.strip()
    print("uid start " + user_name) 
    for g_user in ctx.guild.members:
        print( "uid for " + str(g_user))
        if user_name in str(g_user):
            users_list.append(int(g_user.id))
            print("username match")
            print("appended " + str(g_user.id)) #appending to list
            print("get_uid users list " + str(users_list))
        else:
            print("Not a match")
    print("get_uid list" + str(users_list)) #debugging - prints roles_list
    userLen = len(users_list)
    print(userLen)
    print('get_uid finishing')
    return users_list, len(users_list)

#----------------------------------------- Commands below, functions above-----------------------------------------------------------#


#------------------------------------------testing/troubleshooting commands----------------------------------------------------------#

#@bot.command()
#async def hello(ctx):
#    await ctx.send(f'Hello {ctx.author.display_name}.')


#test command, just echoes the argument
#@bot.command()
#async def test(ctx, content):
#    await ctx.send(content)


#-----------------------------------------------administrative commands---------------------------------------------------------------#
#command to get role ID
@bot.command()
async def roleid(ctx, role_name: str):
    try:
        role, le = get_rid(ctx, role_name)
        print(role)
        print(le)
        if le == 1:
            roleAdd = role[0]
            await ctx.send(roleAdd)
    except:
        emby = discord.Embed(title="", color=discord.Color.red())
        emby.add_field(name="Something went wrong", value="Please check your given argument")
        await ctx.send(embed=emby)

#command to add role to user
@bot.command()
async def addrole(ctx, role_name: str, user):
    try:
        role, le = get_rid(ctx, role_name)
        print(role)
        print(le)
        if le == 1:
            roleAdd = role[0]
            print(roleAdd)
            getuid(user)
            await ctx.send('Adding role %s to user %s' % (role_name, user))

    except:
        print("except")


#command to feth user id's
@bot.command()
async def userid(ctx, user):
    print('User ID command called by %s Requesting UserID for %s' % (ctx.author, user ))
    try:
        #calls function to get user ID by username, then prints variables for debugging/logging
        userN, leU = getuid(ctx, user)
        #outputs all user IDs to chat
        if leU == 0:
            await ctx.send("No user found with that name")
        else:
            for i in userN:
                await ctx.send(i)
    except:
        emby = discord.Embed(title="", color=discord.Color.red())
        emby.add_field(name="Something went wrong", value="Please check your given argument")
        await ctx.send(embed=emby)

#starts the bot
bot.run(token)
