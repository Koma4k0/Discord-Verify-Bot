import config
from threading import Thread

if config.WEB_PORT != 3000:
    port = config.WEB_PORT
else:
    port = 3000

def run_web():
    import uvicorn
    print(f"{config.BOLD}{config.YELLOW}Starting webserver{config.RESET}")
    uvicorn.run("web:app", host=config.WEB_IP, port=port, log_level="info")

print(f"{config.BOLD}{config.BLUE}------------ Oauth Restore Bot ------------{config.RESET}")
print(f"{config.BOLD}{config.BLUE}----- By: Koma4k (https://koma4k.xyz) -----{config.RESET}")

web_thread = Thread(target=run_web)
web_thread.daemon = True
web_thread.start()

print(f"{config.BOLD}{config.GREEN}Webserver Running{config.RESET}")
print(f"{config.BOLD}{config.YELLOW}Starting discord bot{config.RESET}")

if config.token == '':
    print(f'{config.BOLD}ERROR{config.RED}:     Discord Bot Token is missing, please make sure the config.json has the bot token!')
else:
    __import__("bot")
