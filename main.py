import discord
import asyncio
import sys
import os
from datetime import datetime
from utils import Colors, clear, print_ascii

discord_token = input(Colors.CYAN + "Enter Discord Bot Token: " + Colors.END)

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_guild = None
        self.current_channel = None
        self.message_page = 0
        self.loop = asyncio.get_event_loop()
    
    async def async_input(self, prompt):
        return await self.loop.run_in_executor(None, input, prompt)
    
    async def on_ready(self):
        await self.main_menu()
    
    def clear_screen(self):
        clear()
        print_ascii()
    
    async def main_menu(self):
        while True:
            self.clear_screen()
            print(Colors.GREEN + "+" + "-" * 48 + "+" + Colors.END)
            print(Colors.GREEN + "|" + Colors.CYAN + " " * 18 + "MAIN MENU" + " " * 24 + Colors.GREEN + "|" + Colors.END)
            print(Colors.GREEN + "+" + "-" * 48 + "+" + Colors.END)
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "1" + Colors.END + "  Servers and Channels")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "2" + Colors.END + "  Direct Messages")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "3" + Colors.END + "  Bot Information")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "4" + Colors.END + "  User Management")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "5" + Colors.END + "  Search Messages")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "6" + Colors.END + "  Server Analytics")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "7" + Colors.END + "  Voice Channels")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.GREEN + "8" + Colors.END + "  Moderation Tools")
            print(Colors.GREEN + "|" + Colors.END + "  " + Colors.RED + "0" + Colors.END + "  Exit")
            print(Colors.GREEN + "+" + "-" * 48 + "+" + Colors.END)
            print()
            
            choice = await self.async_input(Colors.CYAN + "Select option: " + Colors.END)
            
            if choice == "1":
                await self.show_servers()
            elif choice == "2":
                await self.show_dms()
            elif choice == "3":
                await self.show_bot_info()
            elif choice == "4":
                await self.user_management()
            elif choice == "5":
                await self.search_messages()
            elif choice == "6":
                await self.server_analytics()
            elif choice == "7":
                await self.voice_channels()
            elif choice == "8":
                await self.moderation_tools()
            elif choice == "0":
                self.clear_screen()
                print(Colors.GREEN + "Thank you for using Dis-Connect. Goodbye!" + Colors.END)
                await self.close()
                sys.exit(0)
    
    async def show_servers(self):
        self.clear_screen()
        servers = list(self.guilds)
        
        print(Colors.CYAN + "Your Servers" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        for i, guild in enumerate(servers, 1):
            online = sum(1 for m in guild.members if m.status == discord.Status.online)
            print(f"{Colors.GREEN}[{i:2}]{Colors.END} {Colors.BOLD}{guild.name}{Colors.END}  Members: {guild.member_count}  Online: {online}")
        
        print(Colors.WARNING + "-" * 50 + Colors.END)
        print(Colors.GREEN + "0" + Colors.END + " Back to Menu")
        choice = await self.async_input(Colors.CYAN + "Select server: " + Colors.END)
        
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(servers):
                self.current_guild = servers[idx]
                await self.show_channels()
        except:
            pass
    
    async def show_channels(self):
        self.clear_screen()
        print(Colors.CYAN + f"Server: {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        channels = [ch for ch in self.current_guild.text_channels if ch.permissions_for(self.current_guild.me).read_messages]
        
        categories = {}
        for ch in channels:
            if ch.category:
                if ch.category.name not in categories:
                    categories[ch.category.name] = []
                categories[ch.category.name].append(ch)
            else:
                if "General" not in categories:
                    categories["General"] = []
                categories["General"].append(ch)
        
        for cat_name, cat_channels in categories.items():
            print(f"\n{Colors.BLUE}[{cat_name}]{Colors.END}")
            for ch in cat_channels[:15]:
                print(f"  {Colors.GREEN}#{ch.name}{Colors.END}")
        
        print(Colors.WARNING + "\n" + "-" * 50 + Colors.END)
        print(Colors.GREEN + "0" + Colors.END + " Back")
        channel_name = await self.async_input(Colors.CYAN + "Channel name: " + Colors.END)
        
        if channel_name == "0":
            return
        
        for ch in channels:
            if ch.name.lower() == channel_name.lower():
                self.current_channel = ch
                await self.channel_menu()
                return
        
        print(Colors.RED + "Channel not found" + Colors.END)
        await asyncio.sleep(1)
    
    async def channel_menu(self):
        while True:
            self.clear_screen()
            print(Colors.CYAN + f"Channel: #{self.current_channel.name}" + Colors.END)
            print(Colors.WARNING + "-" * 50 + Colors.END)
            print(Colors.GREEN + "1" + Colors.END + " View Messages")
            print(Colors.GREEN + "2" + Colors.END + " Send Message")
            print(Colors.GREEN + "3" + Colors.END + " Send Image")
            print(Colors.GREEN + "4" + Colors.END + " Pin Message")
            print(Colors.GREEN + "5" + Colors.END + " Clear Messages")
            print(Colors.GREEN + "6" + Colors.END + " Channel Users")
            print(Colors.GREEN + "7" + Colors.END + " Channel Info")
            print(Colors.RED + "0" + Colors.END + " Back")
            print()
            
            choice = await self.async_input(Colors.CYAN + "Select option: " + Colors.END)
            
            if choice == "1":
                await self.view_messages()
            elif choice == "2":
                await self.send_message()
            elif choice == "3":
                await self.send_image()
            elif choice == "4":
                await self.pin_message()
            elif choice == "5":
                await self.clear_messages()
            elif choice == "6":
                await self.channel_users()
            elif choice == "7":
                await self.channel_info()
            elif choice == "0":
                break
    
    async def view_messages(self):
        self.message_page = 0
        while True:
            self.clear_screen()
            print(Colors.CYAN + f"Channel: #{self.current_channel.name} - Page {self.message_page + 1}" + Colors.END)
            print(Colors.WARNING + "-" * 50 + Colors.END)
            
            messages = []
            async for msg in self.current_channel.history(limit=20, offset=self.message_page * 20):
                messages.append(msg)
            
            if not messages:
                print(Colors.RED + "No messages found" + Colors.END)
                break
            
            for i, msg in enumerate(reversed(messages), 1):
                timestamp = msg.created_at.strftime("%H:%M:%S")
                author = msg.author.name[:20]
                
                if msg.attachments:
                    content = "[IMAGE] " + msg.attachments[0].url
                elif msg.embeds:
                    content = "[EMBED]"
                else:
                    content = msg.content[:60] if msg.content else "[EMPTY]"
                
                if msg.pinned:
                    print(f"{Colors.YELLOW}[PIN]{Colors.END} {timestamp} {Colors.GREEN}{author}{Colors.END}: {content}")
                else:
                    print(f"{timestamp} {Colors.CYAN}{author}{Colors.END}: {content}")
            
            print(Colors.WARNING + "\n" + "-" * 50 + Colors.END)
            print("Commands: [n]ext  [p]revious  [r]eply  [u]ser  [d]elete  [q]uit")
            
            cmd = await self.async_input(Colors.CYAN + "> " + Colors.END)
            cmd = cmd.lower()
            
            if cmd == "n":
                self.message_page += 1
            elif cmd == "p" and self.message_page > 0:
                self.message_page -= 1
            elif cmd == "r":
                try:
                    msg_num = int(await self.async_input("Message number: ")) - 1
                    if 0 <= msg_num < len(messages):
                        reply_msg = await self.async_input("Your reply: ")
                        await messages[msg_num].reply(reply_msg)
                        print(Colors.GREEN + "Reply sent!" + Colors.END)
                        await asyncio.sleep(1)
                except:
                    pass
            elif cmd == "u":
                try:
                    msg_num = int(await self.async_input("Message number: ")) - 1
                    if 0 <= msg_num < len(messages):
                        await self.user_info(messages[msg_num].author)
                except:
                    pass
            elif cmd == "d":
                try:
                    msg_num = int(await self.async_input("Message number: ")) - 1
                    if 0 <= msg_num < len(messages):
                        if messages[msg_num].author.id == self.user.id:
                            await messages[msg_num].delete()
                            print(Colors.GREEN + "Message deleted!" + Colors.END)
                        else:
                            print(Colors.RED + "Can only delete your own messages" + Colors.END)
                        await asyncio.sleep(1)
                except:
                    pass
            elif cmd == "q":
                break
    
    async def send_message(self):
        self.clear_screen()
        print(Colors.CYAN + f"Sending to #{self.current_channel.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        message = await self.async_input(Colors.GREEN + "Message: " + Colors.END)
        
        if message.lower() == 'cancel':
            return
        
        await self.current_channel.send(message)
        print(Colors.GREEN + "Message sent!" + Colors.END)
        await asyncio.sleep(1)
    
    async def send_image(self):
        self.clear_screen()
        print(Colors.CYAN + f"Send Image to #{self.current_channel.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        print(Colors.BLUE + "Enter image URL or file path" + Colors.END)
        
        image_input = await self.async_input(Colors.GREEN + "Image URL or Path: " + Colors.END)
        
        if image_input.lower() == 'cancel':
            return
        
        try:
            if image_input.startswith('http'):
                await self.current_channel.send(image_input)
                print(Colors.GREEN + "Image link sent!" + Colors.END)
            else:
                if os.path.exists(image_input):
                    with open(image_input, 'rb') as f:
                        file = discord.File(f)
                        await self.current_channel.send(file=file)
                    print(Colors.GREEN + "Image sent!" + Colors.END)
                else:
                    print(Colors.RED + "File not found" + Colors.END)
        except Exception as e:
            print(Colors.RED + f"Error: {e}" + Colors.END)
        
        await asyncio.sleep(2)
    
    async def pin_message(self):
        self.clear_screen()
        print(Colors.CYAN + f"Pin/Unpin Message in #{self.current_channel.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        messages = []
        async for msg in self.current_channel.history(limit=10):
            messages.append(msg)
        
        for i, msg in enumerate(messages, 1):
            status = "[PINNED]" if msg.pinned else ""
            print(f"{i}. {msg.author.name}: {msg.content[:40]} {status}")
        
        try:
            choice = int(await self.async_input("Message number to pin/unpin: ")) - 1
            if 0 <= choice < len(messages):
                msg = messages[choice]
                if msg.pinned:
                    await msg.unpin()
                    print(Colors.GREEN + "Message unpinned!" + Colors.END)
                else:
                    await msg.pin()
                    print(Colors.GREEN + "Message pinned!" + Colors.END)
        except:
            pass
        
        await asyncio.sleep(1)
    
    async def clear_messages(self):
        self.clear_screen()
        print(Colors.RED + "Clear Messages" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        try:
            amount = int(await self.async_input("Number of messages to clear (1-100): "))
            if 1 <= amount <= 100:
                deleted = await self.current_channel.purge(limit=amount)
                print(Colors.GREEN + f"Deleted {len(deleted)} messages!" + Colors.END)
            else:
                print(Colors.RED + "Invalid amount" + Colors.END)
        except:
            print(Colors.RED + "Invalid input" + Colors.END)
        
        await asyncio.sleep(2)
    
    async def channel_users(self):
        self.clear_screen()
        print(Colors.CYAN + f"Users in #{self.current_channel.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        users = []
        async for msg in self.current_channel.history(limit=200):
            if msg.author not in users:
                users.append(msg.author)
        
        for i, user in enumerate(users[:30], 1):
            print(f"{Colors.GREEN}[{i}]{Colors.END} {user.name}")
        
        await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
    
    async def channel_info(self):
        self.clear_screen()
        print(Colors.CYAN + "Channel Information" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        print(f"Name: #{self.current_channel.name}")
        print(f"ID: {self.current_channel.id}")
        print(f"Category: {self.current_channel.category}")
        print(f"Position: {self.current_channel.position}")
        print(f"NSFW: {'Yes' if self.current_channel.is_nsfw() else 'No'}")
        print(f"Created: {self.current_channel.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"Topic: {self.current_channel.topic or 'None'}")
        print(f"Slowmode: {self.current_channel.slowmode_delay} seconds")
        
        await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
    
    async def user_management(self):
        if not self.current_guild:
            print(Colors.RED + "No server selected" + Colors.END)
            await asyncio.sleep(1)
            return
        
        self.clear_screen()
        print(Colors.CYAN + f"User Management - {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        members = list(self.current_guild.members)
        
        for i, member in enumerate(members[:20], 1):
            status = "ON" if member.status == discord.Status.online else "ID" if member.status == discord.Status.idle else "DN" if member.status == discord.Status.dnd else "OF"
            print(f"{Colors.GREEN}[{i:2}]{Colors.END} [{status}] {member.name}")
        
        print(Colors.WARNING + "\n-" * 50 + Colors.END)
        choice = await self.async_input(Colors.CYAN + "Select user number: " + Colors.END)
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(members):
                await self.user_info(members[idx])
        except:
            pass
    
    async def user_info(self, user):
        self.clear_screen()
        print(Colors.CYAN + "User Information" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        member = self.current_guild.get_member(user.id) if self.current_guild else None
        
        print(f"Name: {Colors.BOLD}{user.name}{Colors.END}")
        print(f"ID: {user.id}")
        print(f"Display Name: {user.display_name}")
        print(f"Created: {user.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        
        if member:
            print(f"Joined: {member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Status: {member.status}")
            if member.activity:
                print(f"Activity: {member.activity.name}")
            roles = [r.name for r in member.roles[1:]]
            if roles:
                print(f"Roles: {', '.join(roles[:5])}")
        
        print(Colors.WARNING + "\n-" * 50 + Colors.END)
        print(Colors.GREEN + "1" + Colors.END + " Send DM")
        print(Colors.GREEN + "2" + Colors.END + " Kick")
        print(Colors.GREEN + "3" + Colors.END + " Ban")
        print(Colors.GREEN + "4" + Colors.END + " Timeout")
        print(Colors.GREEN + "5" + Colors.END + " Manage Roles")
        print(Colors.RED + "0" + Colors.END + " Back")
        
        choice = await self.async_input(Colors.CYAN + "Option: " + Colors.END)
        
        if choice == "1":
            msg = await self.async_input("DM message: ")
            await user.send(msg)
            print(Colors.GREEN + "DM sent!" + Colors.END)
        elif choice == "2" and member:
            reason = await self.async_input("Kick reason: ")
            await member.kick(reason=reason)
            print(Colors.GREEN + "User kicked!" + Colors.END)
        elif choice == "3" and member:
            reason = await self.async_input("Ban reason: ")
            await member.ban(reason=reason)
            print(Colors.GREEN + "User banned!" + Colors.END)
        elif choice == "4" and member:
            duration = int(await self.async_input("Timeout duration (seconds): "))
            await member.timeout(discord.utils.utcnow() + discord.timedelta(seconds=duration))
            print(Colors.GREEN + f"Timed out for {duration}s!" + Colors.END)
        elif choice == "5" and member:
            await self.manage_user_roles(member)
        
        await asyncio.sleep(2)
    
    async def manage_user_roles(self, member):
        self.clear_screen()
        print(Colors.CYAN + f"Manage Roles - {member.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        roles = self.current_guild.roles[1:]
        
        for i, role in enumerate(roles[:15], 1):
            has_role = "YES" if role in member.roles else "NO"
            print(f"{Colors.GREEN}[{i}]{Colors.END} [{has_role}] {role.name}")
        
        try:
            choice = int(await self.async_input("Select role number: ")) - 1
            if 0 <= choice < len(roles):
                role = roles[choice]
                if role in member.roles:
                    await member.remove_roles(role)
                    print(Colors.GREEN + "Role removed!" + Colors.END)
                else:
                    await member.add_roles(role)
                    print(Colors.GREEN + "Role added!" + Colors.END)
                await asyncio.sleep(1)
        except:
            pass
    
    async def search_messages(self):
        self.clear_screen()
        print(Colors.CYAN + "Search Messages" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        query = await self.async_input("Search term: ")
        
        results = []
        for guild in self.guilds[:3]:
            for channel in guild.text_channels[:2]:
                try:
                    async for msg in channel.history(limit=50):
                        if query.lower() in msg.content.lower():
                            results.append((channel, msg))
                            if len(results) >= 15:
                                break
                except:
                    continue
                if len(results) >= 15:
                    break
            if len(results) >= 15:
                break
        
        if not results:
            print(Colors.RED + "No messages found" + Colors.END)
        else:
            for i, (channel, msg) in enumerate(results, 1):
                print(f"{Colors.GREEN}[{i}]{Colors.END} #{channel.name}: {msg.author.name}: {msg.content[:60]}")
        
        await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
    
    async def server_analytics(self):
        if not self.current_guild:
            print(Colors.RED + "No server selected" + Colors.END)
            await asyncio.sleep(1)
            return
        
        self.clear_screen()
        print(Colors.CYAN + f"Server Analytics - {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        total = self.current_guild.member_count
        online = sum(1 for m in self.current_guild.members if m.status == discord.Status.online)
        idle = sum(1 for m in self.current_guild.members if m.status == discord.Status.idle)
        dnd = sum(1 for m in self.current_guild.members if m.status == discord.Status.dnd)
        offline = total - (online + idle + dnd)
        
        print(f"Total Members: {total}")
        print(f"Online: {online}")
        print(f"Idle: {idle}")
        print(f"Do Not Disturb: {dnd}")
        print(f"Offline: {offline}")
        print(f"\nChannels: {len(self.current_guild.channels)}")
        print(f"Text Channels: {len(self.current_guild.text_channels)}")
        print(f"Voice Channels: {len(self.current_guild.voice_channels)}")
        print(f"Roles: {len(self.current_guild.roles)}")
        print(f"Created: {self.current_guild.created_at.strftime('%Y-%m-%d')}")
        
        await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
    
    async def voice_channels(self):
        if not self.current_guild:
            print(Colors.RED + "No server selected" + Colors.END)
            await asyncio.sleep(1)
            return
        
        self.clear_screen()
        print(Colors.CYAN + f"Voice Channels - {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        for vc in self.current_guild.voice_channels:
            if vc.members:
                members = ', '.join([m.name for m in vc.members])
                print(f"{Colors.GREEN}[{vc.name}]{Colors.END} ({len(vc.members)} users): {members}")
            else:
                print(f"{Colors.GREEN}[{vc.name}]{Colors.END} (Empty)")
        
        await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
    
    async def moderation_tools(self):
        if not self.current_guild:
            print(Colors.RED + "No server selected" + Colors.END)
            await asyncio.sleep(1)
            return
        
        self.clear_screen()
        print(Colors.CYAN + f"Moderation Tools - {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        print(Colors.GREEN + "1" + Colors.END + " View Bans")
        print(Colors.GREEN + "2" + Colors.END + " Unban User")
        print(Colors.GREEN + "3" + Colors.END + " Create Channel")
        print(Colors.GREEN + "4" + Colors.END + " Delete Channel")
        print(Colors.GREEN + "5" + Colors.END + " Create Role")
        print(Colors.GREEN + "6" + Colors.END + " Server Info")
        print(Colors.RED + "0" + Colors.END + " Back")
        
        choice = await self.async_input(Colors.CYAN + "Option: " + Colors.END)
        
        if choice == "1":
            bans = [entry async for entry in self.current_guild.bans()]
            for ban in bans[:10]:
                print(f"{ban.user.name}: {ban.reason or 'No reason'}")
            await self.async_input(Colors.WARNING + "\nPress Enter..." + Colors.END)
        elif choice == "2":
            user_id = int(await self.async_input("User ID to unban: "))
            user = await self.fetch_user(user_id)
            await self.current_guild.unban(user)
            print(Colors.GREEN + "User unbanned!" + Colors.END)
            await asyncio.sleep(1)
        elif choice == "3":
            name = await self.async_input("Channel name: ")
            await self.current_guild.create_text_channel(name)
            print(Colors.GREEN + "Channel created!" + Colors.END)
            await asyncio.sleep(1)
        elif choice == "4":
            channel_id = int(await self.async_input("Channel ID to delete: "))
            channel = self.current_guild.get_channel(channel_id)
            if channel:
                await channel.delete()
                print(Colors.GREEN + "Channel deleted!" + Colors.END)
            await asyncio.sleep(1)
        elif choice == "5":
            name = await self.async_input("Role name: ")
            await self.current_guild.create_role(name=name)
            print(Colors.GREEN + "Role created!" + Colors.END)
            await asyncio.sleep(1)
        elif choice == "6":
            await self.server_info()
    
    async def server_info(self):
        self.clear_screen()
        print(Colors.CYAN + f"Server Information - {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        print(f"ID: {self.current_guild.id}")
        print(f"Owner: {self.current_guild.owner}")
        print(f"Verification Level: {self.current_guild.verification_level}")
        print(f"Boost Level: {self.current_guild.premium_tier}")
        print(f"Boost Count: {self.current_guild.premium_subscription_count or 0}")
        print(f"Description: {self.current_guild.description or 'None'}")
        
        await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
    
    async def show_dms(self):
        self.clear_screen()
        print(Colors.CYAN + "Direct Messages" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        
        dms = [dm for dm in self.private_channels if isinstance(dm, discord.DMChannel)]
        
        if not dms:
            print(Colors.RED + "No DM channels found" + Colors.END)
            await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
            return
        
        for i, dm in enumerate(dms[:20], 1):
            print(f"{Colors.GREEN}[{i}]{Colors.END} {dm.recipient.name}")
        
        choice = await self.async_input(Colors.CYAN + "Select DM: " + Colors.END)
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(dms):
                self.current_channel = dms[idx]
                await self.channel_menu()
        except:
            pass
    
    async def show_bot_info(self):
        self.clear_screen()
        print(Colors.CYAN + "Bot Information" + Colors.END)
        print(Colors.WARNING + "-" * 50 + Colors.END)
        print(f"Name: {self.user.name}")
        print(f"ID: {self.user.id}")
        print(f"Servers: {len(self.guilds)}")
        print(f"Total Members: {sum(g.member_count for g in self.guilds)}")
        print(f"Latency: {round(self.latency * 1000)}ms")
        print(f"Created: {self.user.created_at.strftime('%Y-%m-%d')}")
        
        await self.async_input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = BotClient(intents=intents)

try:
    client.run(discord_token)
except Exception as e:
    print(Colors.RED + f"Error: {e}" + Colors.END)
