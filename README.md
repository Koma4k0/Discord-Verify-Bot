# 🔐 Discord Verify Bot
This is a bare bones version of my discord verify bot using discord oauth2 to pull members back into a guild if it were to be termed.

# 💬 Features
- Saves the users refresh token to the database
- Gives role upon successful verification
- Ability to pull all verified members back into a new guild or the current guild

# ⛔️ Features I removed from the free version
- Advanced Logging
- VPN Detection & Blocking
- Custom Home/Verified/Error Pages
- Ability to pull back a single user
- Ability to kick members if they don't verify within a set period
- Removal of their verified role if they deauthorize the bot
- If they leave and join back they will get the verified role again (If they have not deauthorized the bot)

If you are interested in any of the features that are not provided in the free version feel free to contact me [here](https://discord.com/users/1133030912397938820).

You can checkout the non-free version here: https://verify.koma4k.xyz/

# 📥 Installation & Usage
- Make sure to have [Python](https://python.org) installed
- Open command prompt and cd to the directory
- Run `setup.bat` or `py/python -m pip install -r requirements.txt` (Installs all required packages)
- Fill in all the empty fields in `config.py`
- Run `start.bat` or `py/python app.py` (Starts the bot and webserver)
- Once the bot & webserver are running, run `/setup` in your servers verify channel
