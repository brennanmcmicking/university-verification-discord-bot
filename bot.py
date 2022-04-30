
# Standard library imports
import os
import re
import json
from sys import stderr

# Third-party imports
import requests
import discord

'''
API key and discord secret will be stored in OS environment variables
use os.environ['FIELDNAME'] to get these things
'''
DISCORD_BOT_SECRET = os.environ['BOT_SECRET']
API_KEY = os.environ['API_KEY']

# UUID of Admin Role
ADMIN_ROLE = 123456789012345678

# UUID of Channel to send leave messages in
LEAVES_CHANNEL_ID = 123456789012345678

# UUID of channel for bot to watch commands in
BOT_CHANNEL_ID = 123456789012345678

# List of UUIDs of roles to watch out for when a member is updated
role_list = [123456789012345678, 123456789012345678, ...]

# Minecraft usernames match \w exactly and are minimum 3/maximum 16 characters
username_regex = re.compile('^!link\s+(\w{3,16})\s*$')

# This relies on you to enable the Server Members intent for the bot with the corresponding bot secret on discordapp.com/developers
intents = discord.Intents().default()
intents.members = True

# Create the discord client object
client: discord.Client = discord.Client(intents=intents)

# Discord bot events


@client.event
async def on_ready():
    '''Called when the bot is connected to the Discord API and ready to handle other events'''
    print(f'Logged in as \n{client.user.name}\n{client.user.id}\n')


@client.event
async def on_member_update(before, after):
    '''
    Called when any user in the server has their roles changed.
    This function checks to see if the user received one of the roles in role_list
    and sends them a direct message notifying them that they have received it.
    '''
    for role in after.roles:
        if role not in before.roles and role.id in role_list:
            await after.send(f'Gave you the {role.name} role in {role.guild.name}')
            print(f'{after} got role {role.name} in {role.guild.name}')


@client.event
async def on_member_remove(member):
    '''
    Called when a member leaves the Discord server
    '''
    leaves_channel = client.get_channel(LEAVES_CHANNEL_ID)
    await leaves_channel.send(f'{member.name}#{member.discriminator} ({member.mention}, {member.id}) left')


@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != BOT_CHANNEL_ID:
        return

    # This is where we link the user's discord account to their university email account
    if message.content.startswith('!link'):
        mcusername = None
        discorduuid = message.author.id

        # Verify that the given Minecraft username is of valid length and characters
        match = username_regex.search(message.content)
        try:
            mcusername = match.group(1)
        except AttributeError:
            await message.channel.send(f'That is not a valid Minecraft username. Please try again.')
            print(
                f'Discord user {discorduuid} attempted to link their Minecraft account but failed to provide a valid username', file=stderr)
            return

        print(
            f'Calling API to link MC username {mcusername} to Discord user {discorduuid}')

        res = requests.post(
            '<api endpoint to link discord ID to minecraft username/email pair>',
            headers={
                'X-Api-Key': API_KEY
            },
            data=json.dumps({
                'username': str(mcusername),
                'discordid': str(discorduuid)
            })
        )

        mention = message.guild.get_role(ADMIN_ROLE).mention
        if res.status_code == 200:
            await message.channel.send(
                'An email has been sent to the email account associated with that Minecraft username.'
            )
        elif res.status_code == 400:
            await message.channel.send(
                "Sorry, something went wrong with the Minecraft username you gave me."
            )
        else:
            await message.channel.send(f'Oopsie woopsie! {mention}')
            print(
                f'Something bad happened. status_code: {res.status_code}, response body: {res.json()}')

client.run(DISCORD_BOT_SECRET)
