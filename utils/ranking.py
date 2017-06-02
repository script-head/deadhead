from datetime import datetime, timedelta
from .mysql import *

def level_up(user, server):
    now = datetime.now()
    data = get_rank_data(user, server)
    wait_time = data["waittime"]
    level = data["level"]
    xp = data["xp"]
    xpneeded = data["xpneeded"]
    addxp = False
    if wait_time is None:
        addxp = True
    else:
        last = datetime.fromtimestamp(float(wait_time))
        if (last - now).total_seconds() < 0:
            addxp = True
    if not addxp:
        return
    xp += 500
    wait_time = now + timedelta(minutes=2)
    leveled_up = False
    if xp >= xpneeded:
        leveled_up = True
        level += 1
        xp = (xpneeded - xp)
        xpneeded += 1000
    update_all_rank_data(user, server, str(wait_time.timestamp()), level, xp, xpneeded)
    return leveled_up

