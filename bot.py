import discord, config, role
from module import opendb, refresh_token, add_user, get_user_profile
from discord import Option, default_permissions
intents=discord.Intents.all()
client = discord.Bot(intents=intents,debug_guilds=[config.guildid])


@client.slash_command(name="pull", description="Restore members")
@default_permissions(manage_messages=True)
async def restore(ctx,key:Option(str,description="The recovery key")):
    if not key == config.recover_key:
        return await ctx.respond("Wrong key")
    await ctx.respond("Started Pulling Users")
    con,cur = opendb()
    cur.execute("SELECT * FROM users;")
    users = cur.fetchall()

    for user in list(set(users)):
        try:
            new_token = await refresh_token(user[1])
            if new_token != False:
                cur.execute("UPDATE users SET refresh_token = ? WHERE  id == ?;", (new_token["refresh_token"], user[0]))
                con.commit()
                await add_user(new_token["access_token"], ctx.guild.id, user[0])
                profile = await get_user_profile(new_token["access_token"])
                role.add_role(config.guildid, profile["id"], config.roleid)
        except Exception as e:
            print(f"{config.RED}ERROR{config.RESET}:      Exception: {e}")
    con.close()
    await ctx.channel.send("Finished Pulling Users")
    
@client.slash_command(name="setup", description="Send verify panel")
@default_permissions(manage_messages=True)
async def verifypanel(ctx):
    await ctx.channel.send(embed=discord.Embed(color=0x32cd32, title="Verify yourself", description=f"To [verify]({config.oauth2_url}) your account please click on the link and you will recieve your role."))
    await ctx.respond("Done",ephemeral=True)

@client.slash_command(name="database-delete", description="Erase the database. Cannot be undone!")
@default_permissions(manage_messages=True)
async def erasedb(ctx):
    con,cur = opendb()
    cur.execute("DELETE FROM users;")
    con.commit()
    con.close()
    await ctx.respond(f"Erased {cur.rowcount} users from the database",ephemeral=True)

@client.slash_command(name="database-size", description="See how many users are in the db")
@default_permissions(manage_messages=True)
async def dbsize(ctx):
    con,cur = opendb()
    cur.execute("SELECT * FROM users;")
    await ctx.respond(f"There are {len(cur.fetchall())} users in database",ephemeral=True)
    con.close()
    
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name='made by Koma4k'))
    print(f'{config.GREEN}INFO{config.RESET}:     Logged in as {client.user} (ID: {client.user.id})')

if config.token == '':
    print(f'{config.RED}ERROR{config.RESET}:     Discord Bot Token is missing, please make sure the config.json has the bot token!')
else:
    client.run(config.token)