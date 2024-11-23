# Copyright (c) 2024 NULL Lab
# All rights reserved.
# 
# This file is part of the NULL Lab project.
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.

# moderation.py

import discord
from .logger import log_to_mongo, log_error

def setup(bot):

    # Define the `/kick` command
    @bot.command()
    async def kick(ctx, user: discord.User = None, *, reason: str = None):  # Notice the '*' before 'reason'
        # Check if the bot has the right permission to kick
        if not ctx.author.guild_permissions.kick_members:
            await ctx.send("⚠️ You do not have permission to kick members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to kick.")
            return

        try:
            # Fetch the member object from the guild
            member = ctx.guild.get_member(user.id)
            
            if member is None:
                await ctx.send(f"⚠️ {user.name} is not a member of this server.")
                return
            
            # Send a DM to the user with the reason for the kick
            try:
                dm_message = f"Hello {user.name},\n\nYou have been kicked from the server '{ctx.guild.name}'."
                dm_message += f"\nReason: {reason if reason else 'No reason provided.'}"
                await user.send(dm_message)
            except discord.Forbidden:
                # If the user has DMs disabled, this will be caught
                await ctx.send(f"⚠️ Could not send a DM to {user.name}. They may have DMs disabled.")

            # Kick the mentioned member
            await member.kick(reason=reason)
            await ctx.send(f"✅ {user.name} has been kicked from the server.", delete_after=5)

            # Log the kick action
            # log_to_mongo(
            #     author_name=ctx.author.name,
            #     author_id=str(ctx.author.id),
            #     action="kick",
            #     target_name=user.name,
            #     target_id=str(user.id),
            #     reason=reason if reason else "No reason provided",
            #     channel_name=ctx.channel.name,
            # )

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to kick this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to kick the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in kicking user: {e}")

    # Define the `/ban` command
    @bot.command()
    async def ban(ctx, user: discord.User = None, *, reason: str = None):  # Using '*' to capture the reason
        # Check if the bot has the right permission to ban
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("⚠️ You do not have permission to ban members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to ban.")
            return

        try:
            # Fetch the member object from the guild
            member = ctx.guild.get_member(user.id)

            if member is None:
                await ctx.send(f"⚠️ {user.name} is not a member of this server.")
                return
            
            # Send a DM to the user with the reason for the ban
            try:
                dm_message = f"Hello {user.name},\n\nYou have been banned from the server '{ctx.guild.name}'."
                dm_message += f"\nReason: {reason if reason else 'No reason provided.'}"
                await user.send(dm_message)
            except discord.Forbidden:
                # If the user has DMs disabled, this will be caught
                await ctx.send(f"⚠️ Could not send a DM to {user.name}. They may have DMs disabled.")

            # Ban the mentioned member
            await member.ban(reason=reason)
            await ctx.send(f"✅ {user.name} has been banned from the server.", delete_after=5)

            # Log the ban action
            # log_to_mongo(
            #     author_name=ctx.author.name,
            #     author_id=str(ctx.author.id),
            #     action="ban",
            #     target_name=user.name,
            #     target_id=str(user.id),
            #     reason=reason if reason else "No reason provided",
            #     channel_name=ctx.channel.name,
            # )

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to ban this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to ban the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in banning user: {e}")

    # Define the `/mute` command
    @bot.command()
    async def mute(ctx, user: discord.Member = None, *, reason: str = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to mute members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to mute.")
            return

        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role:
                muted_role = await ctx.guild.create_role(name="Muted")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, speak=False, send_messages=False, add_reactions=False)

            if muted_role in user.roles:
                await ctx.send(f"⚠️ {user.name} is already muted.")
                return

            await user.add_roles(muted_role, reason=reason)
            await ctx.send(f"✅ {user.name} has been muted. Reason: {reason if reason else 'No reason provided.'}")

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to mute this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to mute the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in muting user: {e}")

    # Define the `/unmute` command
    @bot.command()
    async def unmute(ctx, user: discord.Member = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to unmute members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to unmute.")
            return

        try:
            muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
            if not muted_role or muted_role not in user.roles:
                await ctx.send(f"⚠️ {user.name} is not muted.")
                return

            await user.remove_roles(muted_role)
            await ctx.send(f"✅ {user.name} has been unmuted.")

        except discord.Forbidden:
            await ctx.send("⚠️ I do not have permission to unmute this user.")
        except discord.HTTPException:
            await ctx.send("⚠️ An error occurred while trying to unmute the user.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in unmuting user: {e}")

    # Define the `/warn` command
    @bot.command()
    async def warn(ctx, user: discord.Member = None, *, reason: str = None):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to warn members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to warn.")
            return

        reason = reason if reason else "No reason provided."
        # Log warning to MongoDB or any database
        # log_to_mongo(user_id=str(user.id), action="warn", reason=reason)
        await ctx.send(f"⚠️ {user.name} has been warned. Reason: {reason}")

    # Define the `/warnings` command
    @bot.command()
    async def warnings(ctx, user: discord.Member = None):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to view warnings.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user whose warnings you want to view.")
            return

        # Fetch warnings from MongoDB or any database
        # warnings = fetch_warnings(user_id=str(user.id))
        warnings = ["Example Warning 1", "Example Warning 2"]  # Placeholder
        if warnings:
            warning_list = "\n".join([f"{idx+1}. {warning}" for idx, warning in enumerate(warnings)])
            await ctx.send(f"⚠️ {user.name}'s warnings:\n{warning_list}")
        else:
            await ctx.send(f"✅ {user.name} has no warnings.")

    # Define the `/lockdown` command
    @bot.command()
    async def lockdown(ctx, channel: discord.TextChannel = None):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("⚠️ You do not have permission to lockdown channels.")
            return

        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"🔒 {channel.name} has been locked down.")

    # Define the `/unlock` command
    @bot.command()
    async def unlock(ctx, channel: discord.TextChannel = None):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("⚠️ You do not have permission to unlock channels.")
            return

        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None  # Reset to default
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send(f"🔓 {channel.name} has been unlocked.")

    # Define the `/slowmode` command
    @bot.command()
    async def slowmode(ctx, seconds: int = 0):
        if not ctx.author.guild_permissions.manage_channels:
            await ctx.send("⚠️ You do not have permission to set slowmode.")
            return

        if seconds < 0:
            await ctx.send("⚠️ Slowmode duration must be 0 or greater.")
            return

        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(f"✅ Slowmode has been disabled for {ctx.channel.name}.")
        else:
            await ctx.send(f"✅ Slowmode has been set to {seconds} seconds for {ctx.channel.name}.")

    # Define the `/addrole` command
    @bot.command()
    async def addrole(ctx, user: discord.Member = None, *, role_name: str = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to manage roles.")
            return

        if not user or not role_name:
            await ctx.send("⚠️ Please mention a user and specify a role.")
            return

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"⚠️ Role '{role_name}' not found.")
            return

        await user.add_roles(role)
        await ctx.send(f"✅ {role_name} role has been assigned to {user.name}.")

    # Define the `/removerole` command
    @bot.command()
    async def removerole(ctx, user: discord.Member = None, *, role_name: str = None):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to manage roles.")
            return

        if not user or not role_name:
            await ctx.send("⚠️ Please mention a user and specify a role.")
            return

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            await ctx.send(f"⚠️ Role '{role_name}' not found.")
            return

        await user.remove_roles(role)
        await ctx.send(f"✅ {role_name} role has been removed from {user.name}.")

    # Define the `/userinfo` command
    @bot.command()
    async def userinfo(ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(title="User Info", color=discord.Color.blue())
        embed.set_thumbnail(url=user.avatar.url)
        embed.add_field(name="Username", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Joined Server", value=user.joined_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Account Created", value=user.created_at.strftime("%Y-%m-%d"), inline=True)
        roles = [role.mention for role in user.roles if role != ctx.guild.default_role]
        embed.add_field(name="Roles", value=", ".join(roles) if roles else "None", inline=False)
        await ctx.send(embed=embed)

    # Define the `/serverinfo` command
    @bot.command()
    async def serverinfo(ctx):
        guild = ctx.guild
        embed = discord.Embed(title=f"Server Info - {guild.name}", color=discord.Color.green())
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="Owner", value=guild.owner.mention, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Created At", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="Region", value=str(guild.region), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        await ctx.send(embed=embed)

    # Define the `/temprole` command
    @bot.command()
    async def temprole(ctx, user: discord.Member = None, role_name: str = None, duration: int = 0):
        if not ctx.author.guild_permissions.manage_roles:
            await ctx.send("⚠️ You do not have permission to manage roles.")
            return

        if not user or not role_name or duration <= 0:
            await ctx.send("⚠️ Please mention a valid user, role, and duration (in seconds).")
            return

        try:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                await ctx.send(f"⚠️ Role '{role_name}' not found.")
                return

            await user.add_roles(role)
            await ctx.send(f"✅ {role_name} has been assigned to {user.name} for {duration} seconds.")

            await asyncio.sleep(duration)
            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send(f"✅ {role_name} has been removed from {user.name}.")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in temprole command: {e}")

    # Define the `/softban` command
    @bot.command()
    async def softban(ctx, user: discord.Member = None, *, reason: str = None):
        if not ctx.author.guild_permissions.ban_members:
            await ctx.send("⚠️ You do not have permission to ban members.")
            return

        if not user:
            await ctx.send("⚠️ Please mention the user you want to softban.")
            return

        try:
            await user.ban(reason=reason)
            await user.unban(reason="Softban removal")
            await ctx.send(f"✅ {user.name} has been softbanned. Reason: {reason if reason else 'No reason provided.'}")
        except Exception as e:
            await ctx.send("⚠️ Something went wrong.")
            log_error(f"Error in softbanning user: {e}")

    # Define the `/poll` command
    @bot.command()
    async def poll(ctx, *, question: str):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to create polls.")
            return

        embed = discord.Embed(title="📊 Poll", description=question, color=discord.Color.blue())
        poll_message = await ctx.send(embed=embed)
        await poll_message.add_reaction("👍")  # Yes
        await poll_message.add_reaction("👎")  # No

    # Define the `/announce` command
    @bot.command()
    async def announce(ctx, channel: discord.TextChannel = None, *, message: str = None):
        if not ctx.author.guild_permissions.manage_messages:
            await ctx.send("⚠️ You do not have permission to make announcements.")
            return

        if not channel or not message:
            await ctx.send("⚠️ Please mention a channel and provide a message.")
            return

        embed = discord.Embed(title="📢 Announcement", description=message, color=discord.Color.gold())
        await channel.send(embed=embed)
        await ctx.send(f"✅ Announcement sent to {channel.mention}.")
