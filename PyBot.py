import discord
from discord.ext import commands
import MoneySystem

ms = MoneySystem.MoneySystem()

prefix = "!"

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='.', intents=intents)

async def ArgumentException(message: discord.Message):
    await message.channel.send("Unzulässige Argumente")
    return

async def set_prefix(pref):
    global prefix
    prefix = pref

tg_help = ""
tg_prefix = ""
ms_user_create = ""
ms_money_add = ""
ms_money_remove = ""
ms_money_send = ""
ms_bankaccounts_create = ""
ms_bankaccounts_list = ""


async def SetVars():
    global tg_help
    global tg_prefix
    global ms_user_create
    global ms_money_add
    global ms_money_send
    global ms_bankaccounts_create
    global ms_bankaccounts_list

    tg_help = f"{prefix}tg-help"
    tg_prefix = f"{prefix}tg-prefix"

    ms_user_create = f"{prefix}ms-create-user"
    ms_money_add = f"{prefix}ms-money-add"
    ms_money_send = f"{prefix}ms-money-send"
    ms_bankaccounts_create = f"{prefix}ms-bankaccounts-new"
    ms_bankaccounts_list = f"{prefix}ms-bankaccounts-list"


@client.event
async def on_ready():
    await SetVars()
    msg = "bot is ready"
    await client.change_presence(activity=discord.Game(name=f"{prefix}tg-help"))
    print(msg)


@client.event
async def on_member_join(member):
    msg = f'{member.name} has joined this server'
    print(msg)
    # await member.send("Willkommen auf The Gamers!")
    for channel in member.guild.text_channels:
        if channel.name == "welcome":
            await channel.send(f"{member.name} ist dem Server beigetreten.")


@client.event
async def on_member_remove(member):
    print(f'{member.name} was removed')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # ms.user.create
    if message.content.startswith(ms_user_create):
        password = message.content.split("\"")[1]
        ms.create_user_account(
            MoneySystem.UserAccount(str(message.author), password, [MoneySystem.BankAccount("main", 0)]))
        await message.channel.send(f"Benutzerkonto für {str(message.author)} wurde erstellt.")
        print(f"created user-account ({str(message.author)})")
        return

    # ms.money.add
    elif message.content.startswith(ms_money_add):
        if message.author.discriminator != "9624":
            return
        arguments = message.content.split(",")
        if len(arguments) != 2:
            await ArgumentException(message)
            return
        id = arguments[0].split("\"")[1]
        amound = arguments[1].split("\"")[1]
        ms.add_money(id, float(amound))
        print(f"Die Summe {float(amound)} wurde dem Bankkonto {id} zugefügt.")
        return

    # ms.money.remove
    elif message.content.startswith(ms_money_remove):
        if message.author.discriminator != "9624":
            return
        arguments = message.content.split(",")
        if len(arguments) != 2:
            await ArgumentException(message)
            return
        id = arguments[0].split("\"")[1]
        amound = arguments[1].split("\"")[1]
        ms.rem_money(id, float(amound))
        print(f"Die Summe {float(amound)} wurde dem Bankkonto {id} entnommen.")
        return

    # ms.money.send
    elif message.content.startswith(ms_money_send):
        arguments = message.content.split(",")
        if len(arguments) != 2:
            await ArgumentException(message)
            return
        orig = arguments[0].split("\"")[1]
        dest = arguments[1].split("\"")[1]
        amound = float(arguments[2].split("\"")[1])
        test_case = False
        for id in ms.get_user_account(str(message.author)).bank_accs:
            if id == orig:
                test_case = True
                break
        if not test_case:
            return
        if ms.rem_money(orig, amound):
            ms.add_money(dest, amound)
        await message.author.send(f"Summe ({amound}) wurde vom Konto {orig} auf das Konto {dest} transferiert.")
        return

    # ms.bankaccounts.create
    elif message.content.startswith(ms_bankaccounts_create):
        if not ms.test_for_user_account(str(message.author)):
            return
        arguments = message.content.split(",")
        if len(arguments) != 2:
            await ArgumentException(message)
            return
        password = arguments[0].split("\"")[1]
        bank_id = arguments[1].split("\"")[1]
        ms.create_bank_account(str(message.author), password, MoneySystem.BankAccount(bank_id, 0))
        return

    # ms.bankaccounts.list
    elif message.content.startswith(ms_bankaccounts_list):
        if not ms.test_for_user_account(str(message.author)):
            return
        user = ms.get_user_account(str(message.author))
        msg = f"Bankkonten von {str(message.author)}:"
        for account_id in user.bank_accs:
            for account in ms.bank_accounts:
                if account.acc_id == account_id:
                    msg += f"\n\t{account.acc_id}: {account.amd}"
        await message.channel.send(msg)
        return

    # tg.help
    elif message.content.startswith(tg_help):
        msg = "Befehle:"
        msg += "\n\ttg:"
        msg += f"\n\t\t{tg_help}"
        msg += "\n\t\t\tRuft diese Liste ab."
        msg += "\n\tms:"
        msg += f"\n\t\t{ms_user_create} \"[user-password]\""
        msg += "\n\t\t\tGeneriert ein Benutzerkonto und weist es dem Sender der Nachricht zu."
        msg += f"\n\t\t{ms_bankaccounts_list}"
        msg += "\n\t\t\tListet alle zum Sender der Nachricht gehörenden Bankkonten auf."
        msg += f"\n\t\t{ms_bankaccounts_create} \"[user-password]\", \"[id]\""
        msg += "\n\t\t\tErstellt ein Bankkonto mit der eingegeben Id."
        await message.channel.send(msg)
    elif message.content.startswith(tg_prefix):
        new_pref = message.content.split("\"")[1]
        if len(new_pref) != 1:
            await ArgumentException(message)
            return
        await set_prefix(new_pref)
        await client.change_presence(activity=discord.Game(name=f"{prefix}tg-help"))
        await SetVars()
        return


client.run("ODMwNDA1OTM0Mzk2MDgwMTI4.YHGNyg.wtsbdCyHcQahkawXVnV9mp5wa8A")
