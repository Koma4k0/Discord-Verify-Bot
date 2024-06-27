import requests, config

URL = "https://discordapp.com/api/v9"

def add_role(guildid,userid,roleid):
        url = f"{URL}/guilds/{guildid}/members/{userid}/roles/{roleid}"

        botToken = config.token

        headers = {
            "Authorization" : f"Bot {botToken}",
            'Content-Type': 'application/json'
        }

        response = requests.put(url=url, headers=headers)
        
        if response.status_code == 204:
            print(f"{config.GREEN}INFO{config.RESET}:     Added role to user ({userid})")
        else:
            print(f"{config.RED}ERROR{config.RESET}:     Error adding role to user, please make sure the bot is higher than the verified role!")
