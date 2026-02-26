import asyncio
import os
import re
import websockets
import threading
import time
import discord
from discord.ext import commands
import json
import requests
import subprocess
# Create handler for each connection
from discord.ext import commands
from discord.ui import Button, View
import datetime
from typing import Literal
#from datetime import datetime
import threading
import sys
import os

# Set UTF-8 encoding for stdout
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)


connections = []

onuse = {}
balance = {}

cash_app_cmessages_sent = {}
cash_app_submited = {}
import os
import json


r = None 
g = None
b = None
name = None
#tickets_channel = 1228833158640828416
tickets_channel = 1429971163135611082

replacement_category=None
#ticket_category_id = 1205992768506429462
ticket_category_id = 1472121828540420199

#1205992767852126311
mods_role_id = 1429842378877046835

#1230963547085996042
mod_logs = 1430043016621461504

#1230963547085996042
transcript_channel_id = 1472123299403403286

#1205992767814369304
buyer_role = 1430204969583251476

#1205992767784878110
server_id =1429677443731689585


def get_emoji_safe(name):
    """Get emoji string from config, return PartialEmoji or None if invalid."""
    raw = get_emoji(name)
    if raw is None:
        return None
    try:
        # Handle custom emoji format like <:name:id> or <a:name:id>
        match = re.match(r'<(a?):(\w+):(\d+)>', str(raw))
        if match:
            animated = match.group(1) == 'a'
            emoji_name = match.group(2)
            emoji_id = int(match.group(3))
            return discord.PartialEmoji(name=emoji_name, id=emoji_id, animated=animated)
        # Unicode emoji (single character or string)
        return str(raw)
    except Exception:
        return None




def set_autorespondjson(key, value, admin):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "auto_respond.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    print(data)
    data[str(key)] = [value,admin]
    print(data)

    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4)  



def remove_autorespondjson(key):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "auto_respond.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    if str(key) in data:
        del data[str(key)]
    else:
        return False

    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4)  
    return True


def get_autorespondjson():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "auto_respond.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    return data



def set_sticky(channel, value):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "sticky.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    data[channel] = value

    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4) 




def remove_sticky(channel):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "sticky.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    if channel in data:
        del data[channel]

    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4)  



 

def add_medal(userid):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "medals.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)
    a = False
    if userid in data:
        data.remove(userid)
    else:
        data.append(userid)
        a = True

    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4) 

    return a

def has_medal(userid):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "medals.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    if userid in data:
        return True
    else:
        return False




def get_sticky(channel):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "sticky.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    if channel in data:
        return data[channel]
    else:
        return None
    

def set_data(file,tid, value):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, f"{file}.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    data[str(tid)] = value

    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4)  


def get_data(file,tid):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    used_json_path = os.path.join(script_dir, f"{file}.json")
    print(used_json_path)
    #load
    with open(used_json_path, "r", encoding="utf-8") as f:

        data = json.load(f)

    if tid in data: 
        return data[tid]
    else:
        return None
    

def get_emoji(name):
    return get_data("emojis",name)

def get_color_roles(name):
    color =  get_data("colors",name)
    return int(color.lstrip('#'), 16)


def get_channel(name):
    return get_data("channels",name)

def get_category(name):
    return get_data("categories",name)

def get_roles(name):
    return get_data("roles",name)

def get_server_data(name):
    return get_data("server",name)



def get_server_id():
    return get_data("server","server_id")


def get_color():
    hex =  get_data("server","hex")
    return int(hex.lstrip('#'), 16)


def get_logo():
    return get_data("server","logo")


def get_ticket(tid):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    used_json_path = os.path.join(script_dir, "tickets.json")
    print(used_json_path)
    #load
    with open(used_json_path, "r") as f:
        data = json.load(f)

    print("data: "+str(data))
    print("tid: " + tid)


    if tid in data: 
        return data[tid]
    else:
        print("not found")
        return None




def set_ticket(tid, aid,service, amount,payment):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "tickets.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)

    data[str(tid)] = [aid,service,amount,payment]

    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4)  



def add_balance(id, value):
    if "$" in str(value):
        amount_float = float(value.strip("$"))
    else:
        amount_float = float(value)

    rounded_amount = round(amount_float, 2)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "balance.json")

    # Load existing data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    # Check if the ID exists in the data
    if str(id) in data:
        # If the ID exists, update its value
        data[str(id)] = round(data[str(id)] + rounded_amount, 2)
    else:
        # If the ID doesn't exist, add it to the data
        data[str(id)] = rounded_amount
    
    
    # Write the updated data back to the JSON file
    with open(used_json_path, "w") as f:
        json.dump(data, f)
    
def set_balancef(id, value):
    if "$" in str(value):
        amount_float = float(value.strip("$"))
    else:
        amount_float = float(value)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "balance.json")

    # Load existing data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    # Check if the ID exists in the data
    if str(id) in data:
        # If the ID exists, update its value
        data[str(id)] = amount_float
    else:
        # If the ID doesn't exist, add it to the data
        data[str(id)] = amount_float
    
    # Write the updated data back to the JSON file
    with open(used_json_path, "w") as f:
        json.dump(data, f)


def get_balance(id):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "balance.json")

    # Load data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    if str(id) in data:
        return round(data[str(id)], 2)
    else:
        return 0
    




def add_balance2(id, value):
    if "$" in str(value):
        amount_float = float(value.strip("$"))
    else:
        amount_float = float(value)

    rounded_amount = round(amount_float, 2)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "tbal.json")

    # Load existing data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    # Check if the ID exists in the data
    if str(id) in data:
        # If the ID exists, update its value
        data[str(id)] = round(data[str(id)] + rounded_amount, 2)
    else:
        # If the ID doesn't exist, add it to the data
        data[str(id)] = rounded_amount
    
    
    # Write the updated data back to the JSON file
    with open(used_json_path, "w") as f:
        json.dump(data, f)
    
def set_balancef2(id, value):
    if "$" in str(value):
        amount_float = float(value.strip("$"))
    else:
        amount_float = float(value)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "tbal.json")

    # Load existing data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    # Check if the ID exists in the data
    if str(id) in data:
        # If the ID exists, update its value
        data[str(id)] = amount_float
    else:
        # If the ID doesn't exist, add it to the data
        data[str(id)] = amount_float
    
    # Write the updated data back to the JSON file
    with open(used_json_path, "w") as f:
        json.dump(data, f)


def get_balance2(id):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "tbal.json")

    # Load data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    if str(id) in data:
        return round(data[str(id)], 2)
    else:
        return 0
    


intents = discord.Intents.all()

managers = {}

bot = commands.Bot(command_prefix='$', intents=intents)



        
class CloseTicketView(View):
    def __init__(self):
        super().__init__()
        
        self.add_item(Button(label="🔒 Close Ticket", custom_id="ticket_delete", style=discord.ButtonStyle.danger))
        


class ClaimTicketView(View):
    def __init__(self):
        super().__init__()
        





@bot.event
async def on_ready():
    print("bot is up and ready")

    try:
        for command in bot.tree.walk_commands():
            command.guild_only = True

        synced = await bot.tree.sync()
        print(f"Syntax {len(synced)} commands")

        update_vc_names.start() 
    except Exception as e:
        print(e)



async def autorespond(message):
        guild = message.guild
    

        words =get_autorespondjson()
        content = message.content.lower()

        print("message:",content)

        for i in words:
                if i == content:
                    if words[i][1] == True:
                        role_id = 813208940808634411
                        role = discord.utils.get(guild.roles, id=role_id)
                        
                        if role not in message.author.roles:
                            return

                    await message.channel.send(words[i][0])
                    await message.delete()

@bot.listen('on_message')
async def on_message(message):

    if message.author == bot.user and not message.embeds:
        return
    
    await autorespond(message)
    

    sticky = get_sticky(str(message.channel.id))

    if sticky != None:
        
        messages = [message async for message in message.channel.history(limit=10)]
        for i in messages:
                if i.author == bot.user and not i.embeds:
                    if i.content == sticky:
                        await i.delete()


        await message.channel.send(sticky)
        return

    

from discord.ext import tasks
deals_channel_id = 1331326580017856615
usd_channel_id = 1331326788550266892

@tasks.loop(minutes=10)  # Runs every 10 minutes
async def update_vc_names():
    try:

        script_dir = os.path.dirname(os.path.abspath(__file__))
        # Load the deals (tbal.json) data

        deals_json_path = os.path.join(script_dir, "tbal.json")
        usd_json_path = os.path.join(script_dir, "balance.json")
        with open(deals_json_path, "r") as f:
            deals_data = json.load(f)
        total_deals = sum(deals_data.values())  # Calculate total deals

        # Load the USD value (balance.json) data
        with open(usd_json_path, "r") as f:
            usd_data = json.load(f)
        total_usd_value = sum(usd_data.values())  # Calculate total USD value

        formatted_usd_value = f"{int(total_usd_value):,}$"

        # Get the channels
        guild = bot.get_guild(get_server_id())  # Replace with your guild ID
        deals_channel = guild.get_channel(deals_channel_id)
        usd_channel = guild.get_channel(usd_channel_id)

        # Edit the channel names
        if deals_channel is not None:
            await deals_channel.edit(name=f"Total Deals: {int(total_deals)}")
        if usd_channel is not None:
            await usd_channel.edit(name=f"USD-Value: {formatted_usd_value}")

        print(f"Updated VC names: deals = {total_deals}, usd-value = {total_usd_value}")

    except Exception as e:
        print(f"Error in updating VC names: {e}")






class ResponseModalNoAdmin(discord.ui.Modal, title="Yukkis Autorespond public"):
    word = discord.ui.TextInput(style = discord.TextStyle.short,label = "Word",required = True,placeholder = "Word here...")

    response = discord.ui.TextInput(style = discord.TextStyle.paragraph,label = "Response:",required = True,placeholder = "Response here...")

    async def on_submit(self, interaction: discord.Interaction):
        print(self.word)
        print(self.response)
        
        set_autorespondjson(str(self.word),str(self.response), False)

        embed = discord.Embed(
                    title="Auto respond message created! ✅",
                    description="",
            )
        
        embed.add_field(name="Word:", value="> "+str(self.word),inline=False)
        embed.add_field(name="Respond:", value="```\n"+str(self.response)+"```", inline=False)


        await interaction.response.send_message(embed=embed)
        
@bot.tree.command(name="add_autorespond", description="Add an auto responder")
@discord.app_commands.checks.has_permissions(administrator=True)

async def set_autorespond(interaction: discord.Interaction):


    if interaction.guild.id != get_server_id():
        return

    
    await interaction.response.send_modal(ResponseModalNoAdmin())



class Paginator(discord.ui.View):
    def __init__(self, embeds):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.current_page = 0

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.primary)
    async def previous_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page - 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.current_page = (self.current_page + 1) % len(self.embeds)
        await interaction.response.edit_message(embed=self.embeds[self.current_page], view=self)


@bot.tree.command(name="list_autorespond", description="List all autoresponders")
@discord.app_commands.checks.has_permissions(administrator=True)

async def list_autorespond(interaction: discord.Interaction):
    if interaction.guild.id != get_server_id():
        return
    words = get_autorespondjson()

    # Create paginated embeds
    embeds = []
    embed = discord.Embed(title="Auto-respond list 🤖", description="")
    
    count = 0
    for i in words:
        embed.add_field(name=" - " + i, value="", inline=False)
        if words[i][1] == True:
            embed.add_field(name="", value="Word only: ✅", inline=True)
        else:
            embed.add_field(name="", value="Word only: ❌", inline=True)

        embed.add_field(name="", value="Respond:\n```\n" + words[i][0] + "```", inline=False)
        count += 1

        # Create a new embed if it reaches the field limit of 25
        if count % 8 == 0:
            embeds.append(embed)
            embed = discord.Embed(title="Auto-respond list 🤖", description="")

    if count == 0:
        embed = discord.Embed(title="No autorersponders found", description="")
        await interaction.response.send_message(embed=embed)
        return 
    

    if embed.fields:
        embeds.append(embed)

    # Create the paginator view and send the first embed
    view = Paginator(embeds)
    await interaction.response.send_message(embed=embeds[0], view=view)



@bot.tree.command(name="remove_autorespond", description="Remove an autoresponder")
@discord.app_commands.checks.has_permissions(administrator=True)
async def remove_autorespond(interaction: discord.Interaction, word:str):
    if interaction.guild.id != get_server_id():
        return

    s = remove_autorespondjson(word)

    if s == True:

        embed = discord.Embed(
                    title="Auto respond word removed. ✅",
                    description="",
            )
        
        embed.add_field(name="Word:", value="> "+word,inline=False)

    else:
        embed = discord.Embed(
                    title="Failed to remove word from auto respond. ❌",
                    description="",
            )
        
        

      
    await interaction.response.send_message(embed=embed)


@bot.command()
async def remind(ctx,  member: discord.Member):
        role_id = get_roles("staff")
        role = discord.utils.get(ctx.guild.roles, id=role_id)
        
        if role not in ctx.author.roles and ctx.author.id != 954504985977188382:
            await ctx.send("You do not have permission to use this command.")
            return
        
        await ctx.message.delete()


        channel = ctx.channel

        tdata = get_ticket(str(channel.id))


        try:
            await member.send(f"**Hey, please check your ticket** <#{str(channel.id)}>.")  # Send the message as a DM to the user
            await ctx.send(f"**Reminder sent to {member.mention}**")
        except discord.Forbidden:
            await ctx.send("Failed to send message to the ticket owner. They may have DMs disabled.")







class stickyModal(discord.ui.Modal, title="Sticky"):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(title="Sticky")
        self.channel = channel

    response = discord.ui.TextInput(
        style=discord.TextStyle.paragraph,
        label="Response:",
        required=True,
        placeholder="Response here..."
    )

    async def on_submit(self, interaction: discord.Interaction):
        print(self.response.value)

        set_sticky(str(self.channel.id), self.response.value)

        await self.channel.send(self.response.value)

        await interaction.response.send_message(
            "Sticky message has been set", ephemeral=True
        )





@bot.tree.command(name="set_sticky", description="Set sticky message")
async def set_stickyc(interaction: discord.Interaction, channel: discord.TextChannel):
    channel_id = channel.id
    if interaction.guild.id != get_server_id():
         return
    
    modal = stickyModal(channel)
    await interaction.response.send_modal(modal)
    




@bot.tree.command(name="medal", description="add/remove medal to user")
async def remove_stickyc(interaction: discord.Interaction, user: discord.User):
    if interaction.guild.id != get_server_id():
         return

    uid = str(user.id)
    status = add_medal(uid)

    if status == True:
        await interaction.response.send_message(f"{interaction.user.mention} Has given {user.mention} a medal , **Congratulations 🎉**")
    else:
        await interaction.response.send_message(f"{user.mention}'s Medal 🎖️ has been taken away by {interaction.user} 👍",ephemeral=True)


@bot.tree.command(name="remove_sticky", description="Remove sticky message")
async def remove_stickyc(interaction: discord.Interaction, channel: discord.TextChannel):
    channel_id = channel.id
    if interaction.guild.id != get_server_id():
         return

    remove_sticky(str(channel_id))

    await interaction.response.send_message("Sticky message has been removed",ephemeral=True)


@bot.tree.command(name="rename", description="rename a channel")
async def rename_channel(interaction: discord.Interaction, new_name: str):
    channel = interaction.channel
    # Check if the user has permission to manage channels
    if not interaction.user.guild_permissions.manage_channels:
        await interaction.response.send_message("You don't have permission to rename channels.", ephemeral=True)
        return

    # Try renaming the channel
    try:
        await channel.edit(name=new_name)
        await interaction.response.send_message(f"Channel renamed to **{new_name}**")
    except Exception as e:
        await interaction.response.send_message(f"Failed to rename the channel: {e}", ephemeral=True)



@bot.command()
async def priority(ctx):
    roles = [
        get_roles("owner"),
        get_roles("staff")
    ]

    perms = False
    for i in roles:
        role = discord.utils.get(ctx.guild.roles, id=i)
    
        if role in ctx.author.roles :
            perms = True

    if perms == False:
        await ctx.channel.send("You're not authorized to use this command") 
        return
    
    try:
        await ctx.channel.edit(position=0)
        await ctx.channel.send("Channel has been moved to the top of its category.")
    except Exception as e:
        await ctx.channel.send(f"An error occurred while moving the channel: {e}")
    




@bot.command()
async def done(ctx,amount: float = 0.0):
    roles = [
        get_roles("owner"),
        get_roles("staff")
    ]

    perms = False
    for i in roles:
        role = discord.utils.get(ctx.guild.roles, id=i)
    
        if role in ctx.author.roles :
            perms = True

    if perms == False:
        await ctx.channel.send("You're not authorized to use this command") 
        return
    
    if (ctx.channel.category_id) not in categories :
        await ctx.send("This command can only be used in a ticket channel.")
        return

    
    
    await ctx.message.delete()


    

    channel = ctx.channel
    guild = ctx.channel.guild


    tdata = get_ticket(str(channel.id))

    if tdata != None:
        owner_id = tdata[0]
        add_balance2(str(owner_id),1)
        add_balance(str(owner_id),amount)

        bal = get_balance(str(owner_id))
        await ctx.channel.send("_balance given_ **Closing Channel**")

        member = await guild.fetch_member(int(owner_id))
            # Fetch the role
        if bal > 10000:
            role = guild.get_role(get_roles("goat"))
            await member.add_roles(role)
        elif bal > 5000:
            role = guild.get_role(get_roles("unreal_client"))
            await member.add_roles(role)
        elif bal > 2500:
            role = guild.get_role(get_roles("premium_client"))
            await member.add_roles(role)
        elif bal > 1000:
            role = guild.get_role(get_roles("godly_client"))
            await member.add_roles(role)
        elif bal > 500:
            role = guild.get_role(get_roles("super_client"))
            await member.add_roles(role)
        elif bal > 100:
            role = guild.get_role(get_roles("pro_client"))
            await member.add_roles(role)



        role = guild.get_role(get_roles("client"))
        if member:
            await member.add_roles(role)


            
        transcript = await chat_exporter.export(channel)


        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{channel.name}.html",
        )

        target_channel = guild.get_channel(get_channel("transcripts"))
        transcript_message = await target_channel.send(file=transcript_file)
        link = transcript_message.attachments[0].url

        transcript_embed = discord.Embed(
            title="Channel Transcript",
            description=f"Click [this link]({link}) to view the transcript online.",
            color=discord.Color.blue()
        )
        tdata = get_ticket(str(channel.id))
        
        transcript_embed.add_field(name="Ticket Owner", value=f"<@{str(tdata[0])}>", inline=True)
        transcript_embed.add_field(name="Payment", value=f"{str(tdata[1])}", inline=True)
        transcript_embed.add_field(name="Receive ", value=str(tdata[2]), inline=True)
        transcript_embed.add_field(name="Ticket Closer", value=ctx.author.mention, inline=True)

        await target_channel.send(content=f"**{ctx.author.name}** has logged a transaction valued at **`${amount}`** for <@{str(tdata[0])}> **`{str(tdata[0])}`**",embed=transcript_embed)


        await channel.delete()
    else:
        await ctx.send("No info found about this ticket")


from discord import app_commands


@bot.tree.command(name="forcestats", description="Edit someone's stats")
@app_commands.describe(action="Action to perform", stat_type="Type of stat", amount="Amount to change", member="Member to update")
@app_commands.choices(action=[
    app_commands.Choice(name="Add", value="Add"),
    app_commands.Choice(name="Remove", value="Remove")
])
@app_commands.choices(stat_type=[
    app_commands.Choice(name="Deals", value="deals"),
    app_commands.Choice(name="USD Value", value="USD_value"),
])
async def forcestats(interaction: discord.Interaction, action: str, stat_type: str, amount: int, member: discord.Member):

    if interaction.guild.id != get_server_id():
        return
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path1 = os.path.join(script_dir, "tbal.json")
    used_json_path2 = os.path.join(script_dir, "balance.json")

    if stat_type == "deals":
        used_json_path = used_json_path1
        with open(used_json_path1, "r") as f:
            data = json.load(f)
    else:
        used_json_path = used_json_path2
        with open(used_json_path2, "r") as f:
            data = json.load(f)




    if action == "Add":
        if str(member.id) not in data:
            data[str(member.id)] = amount
        else:
            data[str(member.id)] = data[str(member.id)]+amount
    else:
        if str(member.id) not in data:
            data[str(member.id)] = -amount
        else:
            data[str(member.id)] = data[str(member.id)]-amount





    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4)


    if action == "Add":
        await interaction.response.send_message(f"{action}ed {amount} {stat_type} for {member.mention}")
    else:
        await interaction.response.send_message(f"{action}d {amount} {stat_type} for {member.mention}")



@bot.tree.command(name="stock-edit",description="Edit stock")
@app_commands.describe(category="Category for stock edit",action="Action to perform",amount="Amount to change", skin="Which skin?",)
@app_commands.choices(category=[
    app_commands.Choice(name="Dahood", value="Dahood"),
    app_commands.Choice(name="Limiteds", value="Limiteds"),
    app_commands.Choice(name="Bladeball Skins", value="Bladeball Skins"),
    app_commands.Choice(name="Trade tokens", value="Trade tokens"),
    app_commands.Choice(name="Limiteds", value="Limiteds"),
    app_commands.Choice(name="Robux", value="Robux"),
])
@app_commands.choices(action=[
    app_commands.Choice(name="Add", value="Add"),
    app_commands.Choice(name="Remove", value="Remove")
])

async def stock_edit(interaction: discord.Interaction,category:str, skin:str, action: str,amount: int):

    if interaction.guild.id != get_server_id():
        return
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "stock.json")

    with open(used_json_path, "r") as f:
        data = json.load(f)




    if action == "Add":
        item = None
        for i in data[category]:
            print(i)
            if skin.lower() in i.lower():
                print("found")
                item = i

        if item != None:
            print("not none")
            data[category][str(item)] = data[category][str(item)] +amount
        else:
            data[category][str(skin)] = amount



    else:
        item = None
        for i in data[category]:
            print(i)
            if skin.lower() in i.lower():
                print("found")
                item = i

        if item != None:
            print("not none")
            data[category][str(item)] = data[category][str(item)] -amount
        else:
            data[category][str(skin)] = -amount





    with open(used_json_path, "w") as f:
        json.dump(data, f, indent=4)


    await interaction.response.send_message(f"**Stock has been successfully edited**\n> Action: `{action}`\n> Amount: `{amount}`\n> Skin/Item `{skin}`\n> Category: {category}",ephemeral=True)


@bot.tree.command(name="leaderboard",description="Check the leaderboard of users usd value")
async def balance_leadboard(interaction: discord.Interaction):
    await interaction.response.send_message(f"**Loading {get_emoji('loading')}**")
    msg = await interaction.original_response()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "balance.json")

    # Load existing data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    # Sort the data by balance in descending order
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    # Create the leaderboard embed
    embed = discord.Embed(
        title="Client Leaderboard 🏆",
        color=get_color()
    )

    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1331358834144313396/1332552940640272455/leaderboard.png?ex=6795ac22&is=67945aa2&hm=2b4c155480dbc000c0598b2b2616f4fd6ea731fce0345ca2c1a35ff9c59ae25d&")


    x = 0
    for idx, (user_id, balance) in enumerate(sorted_data[:9], start=1):
        member = await bot.fetch_user(int(user_id))
        deals = get_balance2(str(user_id))
        if member.name:
            if idx == 1:
                name = f"{str(idx)}. {member.name} 🥇"
            elif idx == 2:
                name = f"{str(idx)}. {member.name} 🥈"
            elif idx == 3:
                name = f"{str(idx)}. {member.name} 🥉"
            else:
                name = f"{str(idx)}. {member.name}"
            
            embed.add_field(
                name=name,
                value=f"USD Value: **`${int(balance)}`**\nDeals: **`{int(deals)}`**",
                inline=True
            )
        else:
            embed.add_field(
                name=f"{idx}. User Not Found",
                value=f"Balance: {int(balance)}$",
                inline=False
            )
        

    await msg.edit(embed=embed, content=None)




class StockPaginator(View):
    def __init__(self, embed_pages):
        super().__init__(timeout=None)
        self.embed_pages = embed_pages
        self.current_page = 0

    @discord.ui.button(label="Previous", style=discord.ButtonStyle.danger)
    async def previous_page(self, interaction: discord.Interaction, button: Button):
        self.current_page = (self.current_page - 1) % len(self.embed_pages)
        await interaction.response.edit_message(embed=self.embed_pages[self.current_page], view=self)

    @discord.ui.button(label="Next", style=discord.ButtonStyle.danger)
    async def next_page(self, interaction: discord.Interaction, button: Button):
        self.current_page = (self.current_page + 1) % len(self.embed_pages)
        await interaction.response.edit_message(embed=self.embed_pages[self.current_page], view=self)

import json
import os
import copy

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type == discord.InteractionType.component:
        if interaction.data['custom_id'] == "stock_select":
            selected_value = interaction.data['values'][0]

            script_dir = os.path.dirname(os.path.abspath(__file__))
            used_json_path = os.path.join(script_dir, "stock.json")
            
            with open(used_json_path, "r", encoding="utf-8") as f:

                data = json.load(f)
            
            stock = data.get(selected_value, [])

            # Determine base embed
            embed = discord.Embed(title="", description=f"### burrito's {selected_value} Stock", color=get_color())
            
            # Set stock-specific embed content
            if selected_value == "Dahood":
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1323843879992033301.webp?size=96")
                embed.set_footer(text="Also accepting trades!")
                embed.set_image(url="https://cdn.discordapp.com/attachments/1269717039640088668/1311098168095674408/ezgif.com-effects.gif")
            elif selected_value == "Limiteds":
                embed.set_image(url="https://cdn.discordapp.com/attachments/1269717039640088668/1311098168095674408/ezgif.com-effects.gif")
                embed.set_footer(text="I accept Limiteds + USD Aswell")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1269717039640088668/1277417780156829817/limiteds.png")
            elif selected_value == 'Bladeball':
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1269826795624988715.webp?size=96")
                embed.set_image(url="https://cdn.discordapp.com/attachments/1269717039640088668/1311098168095674408/ezgif.com-effects.gif")
            elif selected_value == 'Trade tokens':
                embed.set_image(url="https://cdn.discordapp.com/attachments/1269717039640088668/1311098168095674408/ezgif.com-effects.gif")
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1304927746715291730.webp?size=96")
            elif selected_value == 'Robux':
                embed.set_image(url="https://cdn.discordapp.com/attachments/1269717039640088668/1311098168095674408/ezgif.com-effects.gif")
                embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1269721622059810979.webp?size=96")
            
            # Create the pagination embeds
            embeds = []
            description = ""
            x = 0


            try:
                for i, v in stock.items():
                    if v != 0:
                        x += 1
                        description += f"**{i}:** {v}\n"

                        # Create a new embed every 10 items
                        if x % 10 == 0:
                            nembed = copy.deepcopy(embed)  # Copy the base embed
                            nembed.add_field(name=f"Stock Page {len(embeds) + 1}", value=description, inline=False)
                            description = ""  # Reset description for the next set of items
                            embeds.append(nembed)
            except:
                print('no stock')

            # If there are remaining items (less than 10)
            if description:
                nembed = copy.deepcopy(embed)
                nembed.add_field(name=f"Stock Page {len(embeds) + 1}", value=description, inline=False)
                embeds.append(nembed)

            # Create paginator view
            view = StockPaginator(embeds)

            # Add any additional fields or content if necessary
            if selected_value == 'Bladeball':
                print('bladeball selected')
                tokens = data['Trade tokens']['Tokens']
                embed.add_field(name="burrito's Trade token stock", value=f'{get_emoji("trade_token")} Stock: `{tokens:,}` | Rate: 3.5$/1000', inline=False)

                await interaction.response.send_message(embed=embed, ephemeral=True)
            elif selected_value == 'Robux':
                robuxs = data['Robux']['Robux']
                rate = data['Robux']['Prices']
                embed.add_field(name="Robuxs Stock", value=f'{get_emoji("robuxs")} Stock: `{robuxs:,} robuxs`', inline=False)
                embed.add_field(name="Robuxs rate", value=rate, inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:

            # Send the first embed with pagination
                await interaction.response.send_message(embed=embeds[0], ephemeral=True, view=view)

                


        elif interaction.data['custom_id'] == 'product_select':

                bt = False

                user = interaction.user
                user_id = user.id

                script_dir = os.path.dirname(os.path.abspath(__file__))

                used_json_path = os.path.join(script_dir, "tickets.json")
                print(used_json_path)
                #load
                with open(used_json_path, "r") as f:
                    data = json.load(f)

                    
                guild = interaction.guild

                for i in data:
                    owner = data[str(i)][0]
                    print(owner)
                    if str(owner) == str(user_id):
                        print("exists")
                        chan = guild.get_channel(int(i))
                        print("channel defined.")
                        if chan and not "closed" in chan.name:
                            print("ticket: ",i)
                            await interaction.response.send_message(content=f"You already own a ticket <#{i}> ❌",ephemeral=True)
                            return
                        
                selected_value = interaction.data['values'][0]
                crypto = False

                option1 = None
                option2 = None
                
                option1 = selected_value
                
                


                

                if selected_value == "Middleman":
                    await interaction.response.send_message(f'Creating ticket {get_emoji("loading")}',ephemeral=True)

                    category = guild.get_channel(get_category("middleman"))
                
                    ticket_access_role = guild.get_role(get_roles("staff"))

                    overwrites = {
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        guild.me: discord.PermissionOverwrite(read_messages=True),
                        ticket_access_role: discord.PermissionOverwrite(
                            read_messages=True, send_messages=True, attach_files=True, embed_links=True,read_message_history=True
                        ),
                    }
                    overwrites[interaction.user] = discord.PermissionOverwrite(
                        read_messages=True, send_messages=True, attach_files=True, embed_links=True,read_message_history=True
                    )

                    new_channel = await category.create_text_channel(
                            f"{interaction.user.name}", overwrites=overwrites
                        )
                    
                    #set_ticket_data(str(new_channel.id),data)

                    embed = discord.Embed(
                                    title="", 
                                    description=f"> Thank you for using our middleman services. \n- Explain your deal in detail.",
                                    color=get_color()
                    )

                    embed.set_footer(text="For any urgent matters, please contact an administrator.")



                    embed.set_author(
                                        name=f"Middleman Ticket", 
                                        icon_url='https://cdn.discordapp.com/emojis/1193849035807784990.webp?size=96'
                    )

                    avatar_url = user.avatar.url if user.avatar else "https://ia600305.us.archive.org/31/items/discordprofilepictures/discordred.png"

                    embed.set_thumbnail(url=avatar_url)
                
                    
                    print("💼┃Middleman Ticket Created ✅")
                                
                    await new_channel.send(content=f"Welcome <@{str(interaction.user.id)}> <@954504985977188382> <@&1328507128931160167>!",embed=embed, view=CloseTicketView())

                    
                    set_ticket(str(new_channel.id), str(interaction.user.id), None,None,None)

                    user = interaction.user
                    msg = await interaction.original_response()
                    

                    await msg.edit(content=f"Ticket created! <#{new_channel.id}> ✅")
                    return
                        
                    
                
                else:
                    if selected_value == 'Limiteds':
                        view = LimitedsView(get_emoji_safe('limiteds'), get_emoji_safe('selling'))
                        url = 'https://cdn.discordapp.com/emojis/1277333511539265557.webp?size=96'

                        embed = discord.Embed(title="",description='Would you like to **buy** or **sell** Limiteds?',color=get_color())
                        embed.set_thumbnail(url=url)

                        embed.set_author(
                                            name=f"Limiteds Ticket",
                                            icon_url="https://cdn.discordapp.com/emojis/1332761218875916299.webp?size=96"

                        )

                        await interaction.response.send_message(embed=embed,view=view, ephemeral=True)
                        msg = await interaction.original_response()

                        await view.wait()

                        option1 = view.product

                        if option1 == 'Buy limiteds':
                            cat = get_category("buy_limiteds")
                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)

                        elif option1 == 'Sell limiteds':
                            cat = get_category("sell_limiteds")
                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to receive?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)

                    elif selected_value == "Dahood Skins":
                        view = DHView(get_emoji_safe('dh_skins'), get_emoji_safe('selling'))
                        url = 'https://cdn.discordapp.com/emojis/1323843879992033301.webp?size=96'

                        embed = discord.Embed(title="",description='Would you like to **buy** or **sell** skins?',color=get_color())
                        embed.set_thumbnail(url=url)
                        embed.set_author(
                                            name=f"Dahood Skins Ticket",
                                            icon_url="https://cdn.discordapp.com/emojis/1332761218875916299.webp?size=96"

                        )

                        await interaction.response.send_message(embed=embed,view=view, ephemeral=True)
                        msg = await interaction.original_response()

                        await view.wait()

                        option1 = view.product

                        if option1 == "Purchase dahood skins":
                            cat = get_category("buy_dahood_skins")
                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)
                        elif option1 == "Sell dahood skins":
                            cat = get_category("sell_dahood_skins")

                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to receive?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)                      #  bt = True
                       

                    elif selected_value == "Bladeball":
                        view = BladeballView(get_emoji_safe('bladeball'), get_emoji_safe('selling'))
                        url = 'https://cdn.discordapp.com/emojis/1269826795624988715.webp?size=96'

                        embed = discord.Embed(title="",description='Would you like to **buy** or **sell** skins?',color=get_color())
                        embed.set_thumbnail(url=url)
                        embed.set_author(
                                            name=f"Bladeball Tickets",
                                            icon_url="https://cdn.discordapp.com/emojis/1332761218875916299.webp?size=96"

                        )

                        await interaction.response.send_message(embed=embed,view=view, ephemeral=True)
                        msg = await interaction.original_response()

                        await view.wait()

                        option1 = view.product

                        if option1 == "Purchase bladeball skins":
                            cat = get_category("buy_bladeball_skins")
                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)
                        elif option1 == "Sell bladeball skins":
                            cat = get_category("sell_bladeball_skins")

                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to receive?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)
                        elif option1 == 'Buy Bladeball Trade Tokens':
                            cat = get_category("buy_bladeball_trade_tokens")
                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)

                    
                    elif selected_value == "Buy Robuxs/Giftables":

                        view = RobloxView(get_emoji_safe('robuxs'), get_emoji_safe('whitegift'))
                        url = 'https://cdn.discordapp.com/emojis/1332188374433529938.webp?size=96'

                        embed = discord.Embed(title="",description='What would you like to purchase',color=get_color())
                        embed.set_thumbnail(url=url)
                        embed.set_author(
                                            name=f"R$ & Giftables Ticket",
                                            icon_url="https://cdn.discordapp.com/emojis/1332761218875916299.webp?size=96"

                        )

                        await interaction.response.send_message(embed=embed,view=view, ephemeral=True)
                        msg = await interaction.original_response()

                        await view.wait()

                        print(option1)

                        

                        option2 = view.product

                        if option2 == 'Robuxs':
                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)
                            cat = get_category("robuxs")
                            
                        elif option2 == 'Giftables':
                            embed = discord.Embed(title="Game", description="> Select the game",color=get_color() )
                            url = "https://cdn.discordapp.com/emojis/1269858025892614206.webp?size=96&quality=lossless"
                            embed.set_thumbnail(url=url)


                            view = GamesView()

                            await msg.edit(embed=embed, view=view)
                            await view.wait()

                            embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
                            url="https://cdn.discordapp.com/attachments/1211126894653739059/1332770173471428719/gifmaker_me.gif?ex=67967673&is=679524f3&hm=815ba9cbae113a38a310394f891041cdd02d78ff0684a993cb63478acef6a1b3&"
                            embed.set_thumbnail(url=url)
                            cat = get_category("giftables")



                             
                        else:
                            return



                      #  url = "https://cdn.discordapp.com/emojis/1269721622059810979.webp?size=96&quality=lossless"
                      #  embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
                      #  embed.set_thumbnail(url=url)
                    
                    else:
                        url = "https://cdn.discordapp.com/emojis/1269721622059810979.webp?size=96&quality=lossless"
                        embed = discord.Embed(title="Payment Method", description="> What payment method would you like to use?",color=get_color() )
     
                    view = ProductSelectView2()

                
                if crypto == True:
                    msg = await interaction.original_response()
                    await msg.edit(embed=embed,view=view)
                elif bt == True:
                    await interaction.response.send_message(embed=embed,view=view,ephemeral=True)
                    msg = await interaction.original_response()
                else:
                    msg = await interaction.original_response()
                    await msg.edit(embed=embed,view=view)
                    

                await view.wait()

                print(option1)

                

                option2 = view.product
                print("option2 :",option2)

                if option2 == "50,000+":
                    option2 = "more"
                elif option2 == "50,000-":
                    option2="less"
                
                print("waited")


                if option2 == None:
                    return

                #here ticket creation

                print(f"final options: \nSending: {option1}\nReceiving: {option2}")
                await msg.edit(content=f"Creating ticket {get_emoji('loading')}", embed=None, view=None)

                guild = interaction.guild
                if option1 == "Buy Robuxs":
                    cat = get_category("robuxs")
                elif option1 == "Ingame Giftables":
                    cat = get_category("giftables")
                elif option1 == 'Buy Dahood Skins':
                    cat = get_category("buy_dahood_skins")
                elif option1 == 'Sell Dahood Skins':
                    cat = get_category("sell_dahood_skins")
                elif option1 == 'Buy Limiteds':
                    cat = get_category("buy_limiteds")

                print("cat: ",cat)
                
                category = guild.get_channel(cat)
                
                ticket_access_role = guild.get_role(get_roles("staff"))

                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True),
                    ticket_access_role: discord.PermissionOverwrite(
                        read_messages=True, send_messages=True, attach_files=True, embed_links=True,read_message_history=True
                    ),
                }
                overwrites[interaction.user] = discord.PermissionOverwrite(
                    read_messages=True, send_messages=True, attach_files=True, embed_links=True,read_message_history=True
                )

                try:

                    new_channel = await category.create_text_channel(
                        f"{interaction.user.name}-{str(option2)}", overwrites=overwrites
                    )
                except:
                            cat = get_category("buy_dahood_skins2")
                            category = guild.get_channel(cat)
                            new_channel = await category.create_text_channel(
                            f"{interaction.user.name}-{str(option2)}", overwrites=overwrites
                            )
                #set_ticket_data(str(new_channel.id),data)
                if "sell" in option1.lower():
                    embed = discord.Embed(
                                    title="", 
                                    description=f"> Thank you for selling to us. \n- You will be assisted soon.",
                                    color=get_color()
                    )
                    url = "https://cdn.discordapp.com/emojis/1332792571495190650.webp?size=96"
                else:
                    print("option1: ",option1)
                    embed = discord.Embed(
                                    title="", 
                                    description=f"> Thank you for purchasing from us!. \n- You will be assisted soon.",
                                    #description=f"> Thank you for selling to us. \n- You will be assisted soon.",
                                    color=get_color()
                    )
                    url = "https://cdn.discordapp.com/emojis/1332761218875916299.webp?size=96"

                embed.set_footer(text="For any urgent matters, please contact an administrator.")

                modified_string = option1.replace("Buy", "Buying")


                embed.set_author(
                                    name=f"Purchase Ticket - {modified_string}", 
                                    icon_url=url
                )

                avatar_url = user.avatar.url if user.avatar else "https://ia600305.us.archive.org/31/items/discordprofilepictures/discordred.png"

                embed.set_thumbnail(url=avatar_url)
               
                
                print("[🛒]┃Ticket Crated ✅")
                            
                await new_channel.send(content=f"Welcome <@{str(interaction.user.id)}> <@954504985977188382>!",embed=embed, view=CloseTicketView())

                
                set_ticket(str(new_channel.id), str(interaction.user.id), option1, option2,None)

                user = interaction.user
                msg = await interaction.original_response()
                

                await msg.edit(content=f"Ticket created! <#{new_channel.id}> ✅")
        elif interaction.data['custom_id'] == "ticket_delete":
                await interaction.response.send_message(f"**Deleting ticket** {get_emoji('loading')} ")
                print("received ticket_delete!")
                await handle_transcript(interaction)

                await asyncio.sleep(3)
                await interaction.channel.delete()


                


import chat_exporter
import io


async def handle_transcript(interaction: discord.Interaction):
        channel = interaction.channel
        guild = interaction.guild   
    
        transcript = await chat_exporter.export(channel)


        transcript_file = discord.File(
            io.BytesIO(transcript.encode()),
            filename=f"transcript-{channel.name}.html",
        )

        target_channel = guild.get_channel(get_channel("close_transcripts"))
        transcript_message = await target_channel.send(file=transcript_file)
        link = transcript_message.attachments[0].url

        transcript_embed = discord.Embed(
            title="Channel Transcript",
            description=f"Click [this link]({link}) to view the transcript online.",
            color=discord.Color.blue()
        )
        tdata = get_ticket(str(channel.id))
        
        transcript_embed.add_field(name="Ticket Owner", value=f"<@{str(tdata[0])}>", inline=True)
        transcript_embed.add_field(name="Payment", value=f"{str(tdata[1])}", inline=True)
        transcript_embed.add_field(name="Receive ", value=str(tdata[2]), inline=True)
        transcript_embed.add_field(name="Ticket Closer", value=interaction.user.mention, inline=True)

        await target_channel.send(content=f"**{interaction.user.name}** Has closed ticket (not paid ticket) for <@{str(tdata[0])}> **`{str(tdata[0])}`**",embed=transcript_embed)


from discord.ui import Button, View, Select
from discord import SelectOption



class ProductSelectView(View):
    def __init__(self):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="Choose a product",
            options=[
                SelectOption(label="Dahood Skins",emoji=get_emoji_safe("dh_skins")),
                SelectOption(label="Limiteds",emoji=get_emoji_safe("limiteds")),

                SelectOption(label="Buy Robuxs/Giftables",emoji=get_emoji_safe("robuxs")),
                
                SelectOption(label="Bladeball",emoji=get_emoji_safe("bladeball")),
                SelectOption(label="Middleman", emoji='💼')
            ],
            custom_id="product_select"
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user

        print(self.product)

        return True
    
    

class StockView(View):
    def __init__(self):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="Choose a service",
            options=[
                SelectOption(label="Dahood",emoji=get_emoji_safe("dh_skins")),
                SelectOption(label="Limiteds",emoji=get_emoji_safe("limiteds")),
                SelectOption(label="Bladeball",emoji=get_emoji_safe("bladeball")),
                SelectOption(label="Robux",emoji=get_emoji_safe("robuxs")),
            ],
            custom_id="stock_select"
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user

        print(self.product)

        return True
    

class ProductSelectView2(View):
    def __init__(self):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="Payment Method",
            options=[
                SelectOption(label="Cashapp",emoji=get_emoji_safe("cashapp")),
                SelectOption(label="Apple Pay",emoji=get_emoji_safe("apple_pay")),
                SelectOption(label="Paypal",emoji=get_emoji_safe("paypal")),
                SelectOption(label="Venmo",emoji=get_emoji_safe("venmo")),
                SelectOption(label="Zelle",emoji=get_emoji_safe("zelle")),
                SelectOption(label="Crypto",emoji=get_emoji_safe("crypto")),
                
            ],
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user
        await interaction.response.defer()
        self.stop()


        return True
    


class RobuxsView(View):
    def __init__(self):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="Amount of Robuxs",
            options=[
                SelectOption(label="50,000+"),
                SelectOption(label="50,000-"),
            ],
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user
        await interaction.response.defer()
        self.stop()


        return True
    

class GamesView(View):
    def __init__(self):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="What Game",
            options=[
                SelectOption(label="Bladeball",emoji=get_emoji_safe("bladeball")),
                SelectOption(label="Dahood",emoji=get_emoji_safe("dh_skins")),
                SelectOption(label="Rivals",emoji=get_emoji_safe("rivals")),
                SelectOption(label="Other",emoji="🔎"),
            ],
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user
        await interaction.response.defer()
        self.stop()


        return True


class RobloxView(View):
    def __init__(self,emoji1,emoji2):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="What would you like to purchase",
            options=[
                SelectOption(label="Robuxs",emoji=emoji1),
                SelectOption(label="Giftables",emoji=emoji2),
            ],
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user
        await interaction.response.defer()
        self.stop()


        return True


class DHView(View):
    def __init__(self,emoji1,emoji2):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="Would you like to purchase or sell skins",
            options=[
                SelectOption(label="Purchase dahood skins",emoji=emoji1),
                SelectOption(label="Sell dahood skins",emoji=emoji2),
            ],
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user
        await interaction.response.defer()
        self.stop()


        return True
    


class LimitedsView(View):
    def __init__(self,emoji1,emoji2):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="Would you like to purchase or sell limiteds",
            options=[
                SelectOption(label="Buy limiteds",emoji=emoji1),
                SelectOption(label="Sell limiteds",emoji=emoji2),
            ],
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user
        await interaction.response.defer()
        self.stop()


        return True


class BladeballView(View):
    def __init__(self,emoji1,emoji2):
        super().__init__()
        self.product = None
        self.user = None




        self.add_item(Select(
            placeholder="Would you like to purchase or sell skins",
            options=[
                SelectOption(label="Purchase bladeball skins",emoji=emoji1),
                SelectOption(label="Sell bladeball skins",emoji=emoji2),
                SelectOption(label="Buy Bladeball Trade Tokens",emoji=get_emoji_safe("trade_token")),

            ],
        ))

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        print("selected used")
        self.product = interaction.data['values'][0]
        self.user = interaction.user
        await interaction.response.defer()
        self.stop()


        return True




    
class RobuxsModal(discord.ui.Modal, title=f"robuxs rates"):
    response = discord.ui.TextInput(style = discord.TextStyle.paragraph,label = "Rates:",required = True,placeholder = "**5$ | 1000 robuxs**\n**8$ | 2000 robuxs **")

    async def on_submit(self, interaction: discord.Interaction):
        print(self.response)


        script_dir = os.path.dirname(os.path.abspath(__file__))
        used_json_path = os.path.join(script_dir, "stock.json")

        with open(used_json_path, "r") as f:
            data = json.load(f)

        data['Robux']['Prices'] = self.response.value

        with open(used_json_path, "w") as f:
            json.dump(data, f, indent=4)  


        await interaction.response.send_message('robuxs rates have been set', ephemeral=True)

@bot.tree.command(name='set_robuxs_rates',description='set robuxs rate')
async def robuxs_rate(interaction: discord.Interaction):
    if interaction.guild.id == get_server_id():
        await interaction.response.send_modal(RobuxsModal())
    
@bot.tree.command(name="add", description='Add a user to ticket')
async def add(interaction: discord.Interaction, user: discord.Member):
    if interaction.channel is not None:
        await interaction.channel.set_permissions(user, read_messages=True, send_messages=True, attach_files=True,embed_links=True,read_message_history=True)
        await interaction.response.send_message(f'{user.mention} has been added to the channel with read, send, and attach permissions.', ephemeral=True)
    else:
        await interaction.response.send_message('This command must be used in a text channel.', ephemeral=True)



@bot.tree.command(name="remove", description='Remove a user from ticket')
async def add(interaction: discord.Interaction, user: discord.Member):
    if interaction.channel is not None:
        await interaction.channel.set_permissions(user, read_messages=False, send_messages=False, attach_files=False,embed_links=True,read_message_history=True)
        await interaction.response.send_message(f'{user.mention} has been removed from the channel.', ephemeral=True)
    else:
        await interaction.response.send_message('This command must be used in a text channel.', ephemeral=True)

@bot.tree.command(name="assistant", description = "Add assistant role to ticket")
async def add_role(interaction: discord.Interaction):
    role_id = get_roles("assistant")  # Replace with your role ID
    role = interaction.guild.get_role(role_id)
    
    embed = discord.Embed(title='', description=f"**The <@&1335300498986897499> role has been added to <#{str(interaction.channel.id)}>**", color=discord.Color.green())

    # Define the regular user permissions
    regular_permissions = discord.PermissionOverwrite(
        read_messages=True,
        send_messages=True,
        attach_files=True,
        read_message_history=True,
        embed_links=True
    )

    try:
        await interaction.channel.set_permissions(role, overwrite=regular_permissions)
        await interaction.response.send_message(
            embed=embed
        )
    except Exception as e:
        await interaction.response.send_message(
            f"An error occurred while adding the role: {str(e)}", ephemeral=True
        )

@bot.tree.command(name="update-all",description="Check a user's stats")
async def update_all(interaction: discord.Interaction):
        guild = interaction.guild
        channel = interaction.channel 
        channel_id = channel.id
        lenght = len(guild.members)
        await interaction.response.send_message(f"Loading {get_emoji('loading')} 0/{lenght}")
        msg = await interaction.original_response()
        msg_id = msg.id
        x = 0

        channel = await bot.fetch_channel(channel_id)
        msg = await channel.fetch_message(msg_id)


        for member in guild.members:
            member_id = member.id
            bal = get_balance(str(member_id))

            user_roles = []

            if bal > 10000:
                role = guild.get_role(get_roles("goat"))
                user_roles.append(role)
            if bal > 5000:
                role = guild.get_role(get_roles("unreal_client"))
                user_roles.append(role)
            if bal > 2500:
                role = guild.get_role(get_roles("premium_client"))
                user_roles.append(role)
            if bal > 1000:
                role = guild.get_role(get_roles("godly_client"))
                user_roles.append(role)
            if bal > 500:
                role = guild.get_role(get_roles("super_client"))
                user_roles.append(role)
            if bal > 100:
                role = guild.get_role(get_roles("pro_client"))
                user_roles.append(role)
            if bal > 0:
                role = guild.get_role(get_roles("client"))
                user_roles.append(role)




            
            if member and bal>0:
                print(f"given to {member.id} {len(user_roles)} roles")
                await member.add_roles(*user_roles)
            else:
                print("no role given")

            
            x = x+1


            
            
            await msg.edit(content=f"Loading  {get_emoji('loading')} {x}/{lenght}")


            
        
        await msg.edit(content="Everyone has recieved their client roles ✅")



def get_user_rank(user_id: int) -> int:
    """
    Gets the rank of a user in the balance leaderboard.

    Args:
        user_id (int): The user ID whose rank needs to be found.

    Returns:
        int: The rank of the user, or -1 if the user is not found.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    used_json_path = os.path.join(script_dir, "balance.json")

    # Load existing data from JSON
    with open(used_json_path, "r") as f:
        data = json.load(f)

    # Sort the data by balance in descending order
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)

    # Find the rank of the user ID
    for rank, (uid, _) in enumerate(sorted_data, start=1):
        if int(uid) == user_id:
            return rank

    # If user not found in the leaderboard
    return -1

@bot.tree.command(name="stats",description="Check a user's stats")
async def balance(interaction: discord.Interaction, user: discord.User=None):

    if user == None:
        user = interaction.user

    await interaction.response.send_message(f"**Loading** {get_emoji('loading')}")
    msg = await interaction.original_response()


    id = user.id

    rank = get_user_rank(id)
    author = user
    guild = interaction.guild
    print(id)

    mbalance = get_balance(str(id))
    deals = get_balance2(str(id))

    bal = mbalance

    role_id = get_roles("star")
    role = discord.utils.get(guild.roles, id=role_id)

    owner_id = get_roles("owner")
    owner_role = discord.utils.get(guild.roles, id=owner_id)

    gf = False
        
    if role in author.roles:
        gf = True
        

    

    emoji = ""
    color = get_color()
    pre = ""

    medal = has_medal(str(id))

    if medal:
         emoji = emoji + "🎖️"
         

    if owner_role in author.roles:
        emoji = emoji + f"👑"
        color = get_color_roles("owner")
        print("OWNEEEEER")
        pre = "Owner:"

    

    elif gf == True:
        emoji = emoji + f"{get_emoji('bear')}"
        color = get_color_roles("star")
        
    elif bal >= 10000:
        emoji = emoji + get_emoji("goat")
        color = get_color_roles("goat")
        pre = "10,000+ client:"
    elif bal >= 5000:
        emoji = emoji + get_emoji("unreal_client")
        color = get_color_roles("unreal_client")
        pre = "5,000+ client:"
    elif bal >= 2500:
        emoji = emoji + get_emoji("premium_client")
        color = get_color_roles("premium_client")
        ore = "2,500+ client:"
    elif bal >= 1000:
        emoji = emoji + get_emoji("godly_client")
        color = get_color_roles("godly_client")
        pre = "1,000+ client:"
    elif bal >= 500:
        emoji = emoji + get_emoji("super_client")
        color = get_color_roles("super_client")
        pre = "500+ client:"
    elif bal >= 100:
        emoji = emoji + get_emoji("pro_client")
        color = get_color_roles("pro_client")
        pre = "100+ client:"
    elif bal > 0:
        emoji = emoji + get_emoji("client")
        color = get_color_roles("client")

    if rank == 3:
        emoji = emoji+"🥉"
        pre = "3# client:"
    elif rank == 2:
        emoji = emoji+"🥈"
        pre = "2# client:"
    elif rank == 1:
        emoji = emoji+"🥇"
        pre = "1# client:"

    

    
    if gf == True:
        embed = discord.Embed(
            title=f"✨ {user.name} {emoji}",
            description=f"",
            color=color
        )
    else:
        embed = discord.Embed(
            title=f"{user.name} {emoji}",
            description=f"",
            color=color
        )




    
    
    avatar_url = user.avatar.url if user.avatar else "https://ia600305.us.archive.org/31/items/discordprofilepictures/discordred.png"
    embed.set_thumbnail(url=avatar_url)

    embed.add_field(name="", value=f"**Deals Completed**: **`{str(int(deals))}`**", inline=True)
    embed.add_field(name="", value=f"**Total USD Value**: **``${str((mbalance))}``**", inline=False)
    #embed.set_author(name=",")

    await msg.edit(embed=embed,content=None)


@bot.tree.command(name="create_ticket_msg", description='Create tickets panel')
async def create_ticket_msg(interaction: discord.Interaction):

    channel = interaction.channel
    
    embed = discord.Embed(title="", description=f"### burrito's serv tickets {get_emoji('valk')} \n> create a ticket to purchase our stock",color=get_color() )


    embed.set_thumbnail(url=get_server_data("ticket_thumbnail"))
    embed.add_field(name="", value=f"{get_emoji('arrow')} Check our **current stock** before opening a ticket", inline=True)
    
    #embed.add_field(name="", value=f"{get_emoji("arrow")} You can check our **current stock** at <#{get_channel("stock")}>", inline=True)


    view = ProductSelectView()
    

    
    message = await channel.send(embed=embed, view=view)
    await interaction.response.send_message(f'Message created', ephemeral=True)




@bot.tree.command(name="stock_msg", description = 'Create stock panel')
async def create_ticket_msg(interaction: discord.Interaction):

    channel = interaction.channel

    
    embed = discord.Embed(title="", description=f"### burrito's Stock + Prices {get_emoji('selling')} \n> Check out our current stock in this panel. _To purchase head to <#{get_channel('tickets')}>_",color=get_color() )


    embed.set_thumbnail(url=get_server_data("stock_thumbnail"))
   # embed.add_field(name="", value="<a:bluearrow:1269708797052457063> You can check our **current stock** at <#1269717480603910197>", inline=True)

   # emoji1 = await interaction.guild.fetch_emoji(1269826867226218496)
    #emoji2 = await interaction.guild.fetch_emoji(1277333511539265557)


    view = StockView()
    

    
    message = await channel.send(embed=embed, view=view)
    await interaction.response.send_message(f'Message created', ephemeral=True)


categories = [get_category("robuxs"),
              get_category("buy_dahood_skins2"),
              get_category("giftables"),
              get_category("buy_dahood_skins"),
              get_category("sell_dahood_skins"),
              get_category("buy_bladeball_skins"),
              get_category("sell_bladeball_skins"),
              get_category("buy_bladeball_trade_tokens"),
              get_category("buy_limiteds"),
              get_category("sell_limiteds"),
              get_category("middleman")
              ]


@bot.tree.command(name="close", description = 'close ticket')
async def close(interaction: discord.Interaction):
    print("close")

    
    # Get the current channel where the command is invoked
    channel = interaction.channel
    id = channel.id


    if (channel.category_id) in categories :
        print("received ticket_delete!")
        await interaction.response.send_message(f"**Deleting ticket** {get_emoji('loading')}")
        await handle_transcript(interaction)
        await asyncio.sleep(3)
        await interaction.channel.delete()
  
    else:
        print("not valid")


bot.run(token)
