# university-verification-discord-bot
An anonymized version of the Discord bot used in the UVic Minecraft Club Discord server.

At the UVic Minecraft Club, we maintain a database of UVic email/Minecraft Username pairs. Students can fill out a form on the website to verify their email and add their MC username to the database. This allows them to automatically add themself to the server and verify their identity without human interaction.

The point of this Discord bot is to allow students to associate their Discord UUID with their email/MC username pair. This gives them a vanity username colour in the Discord and allows them to be pinged before events. The API is written in Lambda functions and uses DynamoDB to store student information using their email as the key.

The Discord bot also has the added functionality of notifying Admins (or all users depending on channel visibility) when someone leaves the Discord server. This can be used to track what might cause people to leave the server (such as too many pings, etcetera).

This whitelisting system will likely be published publicly one day, although not yet. 

## Usage

You will need to have an API endpoint which accepts a Minecraft Username and Discord UUID and returns 200 on success, 400 on failure. Feel free to reach out to me at brennanmcmicking@gmail.com if you are a University student trying to make a Minecraft club/server for your instituation and want to use this Discord bot in your server.