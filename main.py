import discord
import asyncio
import sys
from utils import Colors, clear, print_ascii

discord_token = input(Colors.CYAN + "[?] Enter Discord Bot Token: " + Colors.END)

class BotClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_guild = None
        self.current_channel = None
        self.cached_messages = []
        self.cursor_pos = 0
        
    async def on_ready(self):
        await self.main_menu()
    
    def clear_screen(self):
        clear()
        print_ascii()
    
    async def main_menu(self):
        while True:
            self.clear_screen()
            print(Colors.GREEN + "[1]" + Colors.END + " View Servers")
            print(Colors.GREEN + "[2]" + Colors.END + " View Direct Messages")
            print(Colors.GREEN + "[3]" + Colors.END + " Bot Info")
            print(Colors.RED + "[4]" + Colors.END + " Exit")
            print()
            
            choice = input(Colors.CYAN + "Select option: " + Colors.END)
            
            if choice == "1":
                await self.show_servers()
            elif choice == "2":
                await self.show_dms()
            elif choice == "3":
                await self.show_bot_info()
            elif choice == "4":
                self.clear_screen()
                print(Colors.GREEN + "Goodbye!" + Colors.END)
                await self.close()
                sys.exit(0)
    
    async def show_servers(self):
        self.clear_screen()
        servers = list(self.guilds)
        
        for i, guild in enumerate(servers, 1):
            print(Colors.GREEN + f"[{i}]" + Colors.END + f" {guild.name} ({guild.member_count} members)")
        
        print(Colors.WARNING + "\n[0] Back to Main Menu" + Colors.END)
        choice = input(Colors.CYAN + "\nSelect server: " + Colors.END)
        
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
        print(Colors.WARNING + "-" * 40 + Colors.END)
        
        channels = [ch for ch in self.current_guild.text_channels if ch.permissions_for(self.current_guild.me).read_messages]
        
        for i, channel in enumerate(channels, 1):
            print(Colors.GREEN + f"[{i}]" + Colors.END + f" #{channel.name}")
        
        print(Colors.WARNING + "\n[0] Back" + Colors.END)
        choice = input(Colors.CYAN + "\nSelect channel: " + Colors.END)
        
        if choice == "0":
            return
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(channels):
                self.current_channel = channels[idx]
                await self.channel_menu()
        except:
            pass
    
    async def channel_menu(self):
        while True:
            self.clear_screen()
            print(Colors.CYAN + f"Channel: #{self.current_channel.name}" + Colors.END)
            print(Colors.WARNING + "=" * 50 + Colors.END)
            print(Colors.GREEN + "[1]" + Colors.END + " View Messages")
            print(Colors.GREEN + "[2]" + Colors.END + " Send Message")
            print(Colors.GREEN + "[3]" + Colors.END + " View Users")
            print(Colors.GREEN + "[4]" + Colors.END + " Manage Roles")
            print(Colors.RED + "[5]" + Colors.END + " Back")
            print()
            
            choice = input(Colors.CYAN + "Select option: " + Colors.END)
            
            if choice == "1":
                await self.view_messages()
            elif choice == "2":
                await self.send_message()
            elif choice == "3":
                await self.view_users()
            elif choice == "4":
                await self.manage_roles()
            elif choice == "5":
                break
    
    async def view_messages(self, offset=0):
        self.clear_screen()
        print(Colors.CYAN + f"Messages in #{self.current_channel.name}" + Colors.END)
        print(Colors.WARNING + "=" * 50 + Colors.END)
        
        messages = []
        async for msg in self.current_channel.history(limit=20, offset=offset):
            messages.append(msg)
        
        if not messages:
            print(Colors.RED + "No messages found" + Colors.END)
            input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
            return
        
        for i, msg in enumerate(reversed(messages)):
            timestamp = msg.created_at.strftime("%H:%M:%S")
            author = msg.author.name[:20]
            content = msg.content[:50] if msg.content else "[Attachment/Embed]"
            print(Colors.GREEN + f"[{timestamp}]" + Colors.END + f" {Colors.BOLD}{author}{Colors.END}: {content}")
            
            if len(msg.content) > 50:
                print(Colors.BLUE + f"  ... (continued, press 'r' to read full)" + Colors.END)
        
        print(Colors.WARNING + "\nCommands:" + Colors.END)
        print("[r] Reply to message  [u] User info  [n] Next page  [b] Back")
        
        cmd = input(Colors.CYAN + "\n> " + Colors.END).lower()
        
        if cmd == "r":
            msg_num = int(input("Message number to reply: ")) - 1
            if 0 <= msg_num < len(messages):
                reply_msg = input("Your reply: ")
                await messages[msg_num].reply(reply_msg)
                print(Colors.GREEN + "Reply sent!" + Colors.END)
                await asyncio.sleep(1)
                await self.view_messages(offset)
        elif cmd == "u":
            msg_num = int(input("Message number: ")) - 1
            if 0 <= msg_num < len(messages):
                await self.user_info(messages[msg_num].author)
        elif cmd == "n":
            await self.view_messages(offset + 20)
        elif cmd == "b":
            return
    
    async def send_message(self):
        self.clear_screen()
        print(Colors.CYAN + f"Sending message to #{self.current_channel.name}" + Colors.END)
        print(Colors.WARNING + "=" * 50 + Colors.END)
        
        message = input(Colors.GREEN + "Message: " + Colors.END)
        
        if message.lower() == 'cancel':
            return
        
        await self.current_channel.send(message)
        print(Colors.GREEN + "Message sent!" + Colors.END)
        await asyncio.sleep(1)
    
    async def view_users(self):
        self.clear_screen()
        print(Colors.CYAN + f"Users in {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "=" * 50 + Colors.END)
        
        users = [member for member in self.current_guild.members]
        
        for i, member in enumerate(users[:20], 1):
            status = "🟢" if member.status == discord.Status.online else "🟡" if member.status == discord.Status.idle else "🔴"
            print(f"{Colors.GREEN}[{i}]{Colors.END} {status} {member.name}")
        
        print(Colors.WARNING + "\n[0] Back" + Colors.END)
        choice = input(Colors.CYAN + "\nSelect user (or 0): " + Colors.END)
        
        if choice != "0":
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(users):
                    await self.user_info(users[idx])
            except:
                pass
    
    async def user_info(self, user):
        self.clear_screen()
        print(Colors.CYAN + f"User Information" + Colors.END)
        print(Colors.WARNING + "=" * 50 + Colors.END)
        print(f"Name: {user.name}")
        print(f"ID: {user.id}")
        print(f"Status: {user.status}")
        print(f"Created: {user.created_at.strftime('%Y-%m-%d')}")
        if hasattr(user, 'joined_at') and user.joined_at:
            print(f"Joined: {user.joined_at.strftime('%Y-%m-%d')}")
        print()
        print(Colors.GREEN + "[1]" + Colors.END + " Send DM")
        print(Colors.GREEN + "[2]" + Colors.END + " Kick")
        print(Colors.GREEN + "[3]" + Colors.END + " Ban")
        print(Colors.RED + "[0]" + Colors.END + " Back")
        
        choice = input(Colors.CYAN + "\nSelect option: " + Colors.END)
        
        if choice == "1":
            msg = input("DM message: ")
            await user.send(msg)
            print(Colors.GREEN + "DM sent!" + Colors.END)
            await asyncio.sleep(1)
        elif choice == "2" and self.current_guild:
            try:
                await self.current_guild.kick(user)
                print(Colors.GREEN + "User kicked!" + Colors.END)
            except:
                print(Colors.RED + "Failed to kick" + Colors.END)
            await asyncio.sleep(1)
        elif choice == "3" and self.current_guild:
            try:
                await self.current_guild.ban(user)
                print(Colors.GREEN + "User banned!" + Colors.END)
            except:
                print(Colors.RED + "Failed to ban" + Colors.END)
            await asyncio.sleep(1)
    
    async def manage_roles(self):
        self.clear_screen()
        print(Colors.CYAN + f"Roles in {self.current_guild.name}" + Colors.END)
        print(Colors.WARNING + "=" * 50 + Colors.END)
        
        roles = self.current_guild.roles[1:]
        
        for i, role in enumerate(roles[:20], 1):
            print(f"{Colors.GREEN}[{i}]{Colors.END} {role.name}")
        
        print(Colors.WARNING + "\n[0] Back" + Colors.END)
        choice = input(Colors.CYAN + "\nSelect role: " + Colors.END)
        
        if choice != "0":
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(roles):
                    await self.role_menu(roles[idx])
            except:
                pass
    
    async def role_menu(self, role):
        self.clear_screen()
        print(Colors.CYAN + f"Managing role: {role.name}" + Colors.END)
        print(Colors.WARNING + "=" * 50 + Colors.END)
        print(Colors.GREEN + "[1]" + Colors.END + " Assign to user")
        print(Colors.GREEN + "[2]" + Colors.END + " Remove from user")
        print(Colors.GREEN + "[3]" + Colors.END + " View users with role")
        print(Colors.RED + "[0]" + Colors.END + " Back")
        
        choice = input(Colors.CYAN + "\nSelect option: " + Colors.END)
        
        if choice == "1" or choice == "2":
            users = [m for m in self.current_guild.members]
            self.clear_screen()
            for i, user in enumerate(users[:20], 1):
                print(f"{Colors.GREEN}[{i}]{Colors.END} {user.name}")
            
            user_choice = input(Colors.CYAN + "\nSelect user: " + Colors.END)
            try:
                idx = int(user_choice) - 1
                if 0 <= idx < len(users):
                    if choice == "1":
                        await users[idx].add_roles(role)
                        print(Colors.GREEN + "Role assigned!" + Colors.END)
                    else:
                        await users[idx].remove_roles(role)
                        print(Colors.GREEN + "Role removed!" + Colors.END)
                    await asyncio.sleep(1)
            except:
                pass
        elif choice == "3":
            self.clear_screen()
            users_with_role = [m for m in self.current_guild.members if role in m.roles]
            print(Colors.CYAN + f"Users with {role.name} role:" + Colors.END)
            for user in users_with_role[:20]:
                print(f"- {user.name}")
            input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
    
    async def show_dms(self):
        self.clear_screen()
        print(Colors.CYAN + "Direct Messages" + Colors.END)
        print(Colors.WARNING + "=" * 50 + Colors.END)
        
        dms = []
        for dm in self.private_channels:
            if isinstance(dm, discord.DMChannel):
                dms.append(dm)
        
        if not dms:
            print(Colors.RED + "No DM channels found" + Colors.END)
            input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)
            return
        
        for i, dm in enumerate(dms[:20], 1):
            print(f"{Colors.GREEN}[{i}]{Colors.END} {dm.recipient.name}")
        
        choice = input(Colors.CYAN + "\nSelect DM: " + Colors.END)
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
        print(Colors.WARNING + "=" * 50 + Colors.END)
        print(f"Name: {self.user.name}")
        print(f"ID: {self.user.id}")
        print(f"Servers: {len(self.guilds)}")
        print(f"Total Members: {sum(g.member_count for g in self.guilds)}")
        print(f"Latency: {round(self.latency * 1000)}ms")
        input(Colors.WARNING + "\nPress Enter to continue..." + Colors.END)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = BotClient(intents=intents)

try:
    client.run(discord_token)
except Exception as e:
    print(Colors.RED + f"Error: {e}" + Colors.END)
