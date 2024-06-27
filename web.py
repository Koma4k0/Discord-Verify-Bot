from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from module import exchange_code, opendb, get_user_profile
import role, config

app = FastAPI()

@app.get("/callback")
async def callback(code: str):
    exchange_res = await exchange_code(code)
    if not exchange_res:
        raise HTTPException(status_code=400, detail="Permission not granted")
    profile = await get_user_profile(exchange_res["access_token"])
    if not profile:
        raise HTTPException(status_code=400, detail="Permission not granted")
    con, cur = opendb()
    cur.execute("INSERT OR REPLACE INTO users VALUES (?, ?);", (profile["id"], exchange_res["refresh_token"]))
    con.commit()
    con.close()
    role.add_role(config.guildid, profile["id"], config.roleid)
    return RedirectResponse("https://discord.com/oauth2/authorized")

