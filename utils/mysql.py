import sqlite3
import discord

from utils.tools import convert_to_bool

conn = sqlite3.connect("data/Ruby.db")
conn.row_factory = sqlite3.Row
cur = conn.cursor()

def create_tables():
    cur.execute("""CREATE TABLE IF NOT EXISTS servers(id TEXT, type TEXT, value TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS blacklist(id TEXT, name TEXT, discrim TEXT, reason TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS economy(id TEXT, balance INTEGER, data TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS ranking(userid TEXT, serverid TEXT, waittime TEXT, level INTEGER, xp INTEGER, xpneeded INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS rankuproles(serverid TEXT, roles TEXT)""")

def insert_data_entry(id, type, value):
    cur.execute("""INSERT INTO servers(id, type, value) VALUES (?, ?, ?)""", (id, type, value))
    conn.commit()

def read_data_entry(id, type):
    cur.execute("""SELECT value FROM servers WHERE id=(?) AND type=(?)""", (id, type))
    val = None
    try:
        val = cur.fetchone()[0]
    except:
        if type == "mod-role":
            insert_data_entry(id, type, "Mods")
            val = "Mods"
        elif type == "mute-role":
            insert_data_entry(id, type, "Muted")
            val = "Muted"
        elif type == "join-message":
            insert_data_entry(id, type, None)
            val = None
        elif type == "leave-message":
            insert_data_entry(id, type, None)
            val = None
        elif type == "join-leave-channel":
            insert_data_entry(id, type, None)
            val = None
        elif type == "join-role":
            insert_data_entry(id, type, None)
            val = None
        elif type == "enable-ranking":
            insert_data_entry(id, type, False)
            val = False
    if type == "enable-ranking":
        # sqlite likes to convert bools to ints smh
        val = convert_to_bool(val)
    return val

def update_data_entry(id, type, value):
    exists = read_data_entry(id, type)
    cur.execute("""UPDATE servers SET value=(?) WHERE id=(?) AND type=(?)""", (value, id, type))
    conn.commit()

def delete_data_entry(id, type):
    cur.execute("""DELETE FROM servers WHERE id=(?) AND type=(?)""", (id, type))
    conn.commit()

def blacklistuser(id, name, discrim, reason):
    cur.execute("""INSERT INTO blacklist(id, name, discrim, reason) VALUES (?, ?, ?, ?)""", (id, name, discrim, reason))
    conn.commit()

def unblacklistuser(id):
    cur.execute("""DELETE FROM blacklist WHERE id=""" + id)
    conn.commit()

def getblacklistentry(id):
    cur.execute("""SELECT id FROM blacklist WHERE id=""" + id)
    id = None
    name = None
    discrim = None
    reason = None
    try:
        id = cur.fetchone()[0]
    except:
        return None
    cur.execute("""SELECT name FROM blacklist WHERE id=""" + id)
    name = cur.fetchone()[0]
    cur.execute("""SELECT discrim FROM blacklist WHERE id=""" + id)
    discrim = cur.fetchone()[0]
    cur.execute("""SELECT reason FROM blacklist WHERE id=""" + id)
    reason = cur.fetchone()[0]
    blacklistentry = {"id":id, "name":name, "discrim":discrim, "reason":reason}
    return blacklistentry

def getblacklist():
    cur.execute("""SELECT id, name, discrim, reason FROM blacklist""")
    entries = []
    rows = cur.fetchall()
    for row in rows:
        entry = "ID: \"{}\" Name: \"{}\" Discrim: \"{}\" Reason: \"{}\"".format(row["id"], row["name"], row["discrim"], row["reason"])
        entries.append(entry)
    return entries

eco_data_defaults = {"headpats":0, "lastdailyroses":None}

def get_user_economy_data(user):
    cur.execute("""SELECT id, balance, data FROM economy WHERE id=""" + user.id)
    try:
        cur.fetchone()[0]
    except:
        cur.execute("""INSERT INTO economy(id, balance, data) VALUES (?, ?, ?)""", (user.id, 0, str(eco_data_defaults)))
        conn.commit()
        cur.execute("""SELECT id, balance, data FROM economy WHERE id=""" + user.id)
        cur.fetchone()[0]
    cur.execute("""SELECT balance FROM economy WHERE id=""" + user.id)
    balance = cur.fetchone()[0]
    cur.execute("""SELECT data FROM economy WHERE id=""" + user.id)
    data = cur.fetchone()[0]
    eco_data = {"balance":balance, "data":eval(data)}
    return eco_data

def set_balance(user, amount):
    exists = get_user_economy_data(user)
    cur.execute("""UPDATE economy SET balance=(?) WHERE id=(?)""", (amount, user.id))
    conn.commit()

def update_eco_data_entry(user, key, value):
    exists = get_user_economy_data(user)
    data = get_user_economy_data(user)["data"]
    data[key] = value
    cur.execute("""UPDATE economy SET data=(?) WHERE id=(?)""", (str(data), user.id))
    conn.commit()

def get_rank_data(user, server):
    cur.execute("""SELECT waittime, level, xp, xpneeded FROM ranking WHERE userid=(?) AND serverid=(?)""", (user.id, server.id))
    try:
        data = cur.fetchall()[0]
    except:
        cur.execute("""INSERT INTO ranking(userid, serverid, waittime, level, xp, xpneeded) VALUES (?, ?, ?, ?, ? ,?)""", (user.id, server.id, None, 0, 0, 1000))
        conn.commit()
        data = cur.execute("""SELECT waittime, level, xp, xpneeded FROM ranking WHERE userid=(?) AND serverid=(?)""", (user.id, server.id))
        cur.fetchall()[0]
    try:
        waittime = data["waittime"]
    except TypeError:
        waittime = None
    level = data["level"]
    xp = data["xp"]
    xpneeded = data["xpneeded"]
    return {"waittime":waittime, "level":level, "xp":xp, "xpneeded":xpneeded}

def update_all_rank_data(user, server, waittime, level, xp, xpneeded):
    exists = get_rank_data(user, server)
    cur.execute("""UPDATE ranking SET waittime=(?), level=(?), xp=(?), xpneeded=(?) WHERE userid=(?) AND serverid=(?)""", (waittime, level, xp, xpneeded, user.id, server.id))
    conn.commit()

def get_rankup_roles(server):
    cur.execute("""SELECT roles FROM rankuproles WHERE serverid=""" + server.id)
    entries = []
    try:
        data = cur.fetchone()[0]
    except:
        cur.execute("""INSERT INTO rankuproles(serverid, roles) VALUES (?, ?)""", (server.id, "{}"))
        conn.commit()
        cur.execute("""SELECT roles FROM rankuproles WHERE serverid=""" + server.id)
        data = cur.fetchone()[0]
    for level, roleid in eval(data).items():
        role = discord.utils.get(server.roles, id=roleid).name
        entries.append("Level {}: {}".format(level, role))
    return entries

def get_rankup_role_dict(server):
    exists = get_rankup_roles(server)
    cur.execute("""SELECT roles FROM rankuproles WHERE serverid=""" + server.id)
    data = cur.fetchone()[0]
    return eval(data)

def set_rankup_roles(server, roles):
    exists = get_rankup_roles(server)
    cur.execute("""UPDATE rankuproles SET roles=(?) WHERE serverid=(?)""", (str(roles), server.id))
    conn.commit()

def get_user_ranks(server):
    cur.execute("""SELECT userid, level, xp FROM ranking WHERE serverid=""" + server.id)
    return cur.fetchall()

create_tables()
