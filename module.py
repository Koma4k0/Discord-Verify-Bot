import config, requests, asyncio, sqlite3

async def exchange_code(code):
    data = {
      'client_id': config.CLIENT_ID,
      'client_secret': config.CLIENT_SECRET,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': config.REDIRECT_URI
    }
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    while True:
        r = requests.post('%s/oauth2/token' % config.API_ENDPOINT, data=data, headers=headers)
        if (r.status_code != 429):
            break

        limitinfo = r.json()
        await asyncio.sleep(limitinfo["retry_after"] + 2)
    return False if "error" in r.json() else r.json()

async def refresh_token(refresh_token):
    data = {
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    while True:
        r = requests.post('%s/oauth2/token' % config.API_ENDPOINT, data=data, headers=headers)
        if (r.status_code != 429):
            break

        limitinfo = r.json()
        await asyncio.sleep(limitinfo["retry_after"] + 2)

    #print(r.json()) # Uncomment this if you need to debug anything.
    return False if "error" in r.json() else r.json()

async def add_user(access_token, guild_id, user_id):
    while True:
        jsonData = {"access_token" : access_token}
        header = {"Authorization" : "Bot " + config.token}
        r = requests.put(f"{config.API_ENDPOINT}/guilds/{guild_id}/members/{user_id}", json=jsonData, headers=header)
        if (r.status_code != 429):
            break

        limitinfo = r.json()
        await asyncio.sleep(limitinfo["retry_after"] + 2)

    if (r.status_code == 201 or r.status_code == 204):
        return True
    else:
        print(f"{config.RED}ERROR{config.RESET}:      Error restoring member. Status Code: {r.status_code}")
        #print(r.json()) # Uncomment this to debug if needed
        return False

def opendb():
    con = sqlite3.connect('db.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
                        id TEXT PRIMARY KEY,
                        refresh_token TEXT
                    );''')
    return con, cur

async def get_user_profile(token):
    header = {"Authorization" : "Bearer " + token}
    res = requests.get("https://discordapp.com/api/v8/users/@me", headers=header)
    ves = res.json()
    print(f"{config.GREEN}INFO{config.RESET}:     New verify from",ves['username'],ves['id'])
    if (res.status_code != 200):
        return False
    else:
        return res.json()