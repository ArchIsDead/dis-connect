import os
import sys
import asyncio

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    YELLOW = '\033[93m'

def clear():
    os.system('clear')

def print_ascii():
    print(Colors.CYAN + Colors.BOLD)
    print(r"""
________  .__                 _________                                     __   
\______ \ |__| ______         \_   ___ \  ____   ____   ____   ____   _____/  |_ 
 |    |  \|  |/  ___/  ______ /    \  \/ /  _ \ /    \ /    \_/ __ \_/ ___\   __\
 |    `   \  |\___ \  /_____/ \     \___(  <_> )   |  \   |  \  ___/\  \___|  |  
/_______  /__/____  >          \______  /\____/|___|  /___|  /\___  >\___  >__|  
        \/        \/                  \/            \/     \/     \/     \/      
    """ + Colors.END)
    print(Colors.GREEN + "[" + Colors.CYAN + "Dis-Connect" + Colors.GREEN + "] Discord Bot Stuff" + Colors.END)
    print(Colors.YELLOW + "=" * 50 + Colors.END + "\n")

async def loading_animation(text):
    chars = "|/-\\"
    for i in range(15):
        sys.stdout.write(f'\r{Colors.CYAN}{text} {chars[i % len(chars)]}{Colors.END}')
        sys.stdout.flush()
        await asyncio.sleep(0.1)
    sys.stdout.write('\r' + ' ' * 50 + '\r')
