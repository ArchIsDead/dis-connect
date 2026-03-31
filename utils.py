import os
import sys
import time

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
    print(Colors.GREEN + "[" + Colors.CYAN + "Dis-Connect" + Colors.GREEN + "] Discord Bot Manager v1.0" + Colors.END)
    print(Colors.WARNING + "=" * 50 + Colors.END + "\n")
