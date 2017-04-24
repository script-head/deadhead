from .mysql import *
from utils.tools import *

daily_rose_amount = 50

def add_roses(user, amount):
    balance = get_user_economy_data(user)["balance"]
    set_balance(user, (balance + amount))

def remove_roses(user, amount):
    balance = get_user_economy_data(user)["balance"]
    new_amount = balance - amount
    if amount < 0:
        new_amount = 0
    set_balance(user, new_amount)

def get_roses(user):
    return get_user_economy_data(user)["balance"]

def can_afford(user, amount):
    balance = get_user_economy_data(user)["balance"]
    new_amount = balance - amount
    if new_amount < 0:
        return False
    else:
        return True

def format_currency(amount):
    return ":rose:**{}**".format(format_number(amount))

def get_eco_data_entry(user, key):
    data = get_user_economy_data(user)["data"]
    try:
        entry = data[key]
    except KeyError:
        entry = eco_data_defaults[key]
        update_eco_data_entry(user, key, entry)
    return entry

def needs_amount(amount):
    return "You need at least {} to use this".format(format_currency(amount))
