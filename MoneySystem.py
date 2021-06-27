import discord
from discord.ext import commands


class UserAccount:
    def __init__(self, username, password, bank_accounts):
        self.usrname = username
        self.pw = password
        self.bank_accs = bank_accounts

    def set_bank_accounts(self):
        self.bank_accs = []
        return self


class BankAccount:
    def __init__(self, account_id: str, money_amound: float):
        self.acc_id = account_id
        self.amd = money_amound


class MoneySystem:
    def __init__(self):
        self.user_accounts = [UserAccount("test", "test", ["test"])]
        self.bank_accounts = [BankAccount("test", 0)]
        self.user_error_case = UserAccount("ERROR", "ERROR", [BankAccount("ERROR", 0)])

    def test_for_user_account(self, user_name):
        for user in self.user_accounts:
            if user.usrname == user_name:
                return True
        return False

    def get_user_account(self, username):
        for user in self.user_accounts:
            if user.usrname == username:
                return user
        return None

    def create_user_account(self, user_account: UserAccount):
        if self.test_for_user_account(user_account.usrname):
            return self.get_user_account(user_account.usrname)
        self.user_accounts.append(user_account)
        return user_account

    def add_money(self, account_id: str, amound: float):
        for account in self.bank_accounts:
            if account.acc_id == account_id:
                account.amd += amound
                break
        return

    def rem_money(self, account_id: str, amound: float):
        for account in self.bank_accounts:
            if account.acc_id == account_id:
                if account.amd - amound >= 0:
                    account.amd -= amound
                    return True
                break
        return False

    def create_bank_account(self, username, password, new_bank_account):
        if not self.test_for_user_account(username):
            return
        for account in self.bank_accounts:
            if account.acc_id == new_bank_account.acc_id:
                return
        user = self.get_user_account(username)
        if user.pw != password:
            return
        user.bank_accs.append(new_bank_account.acc_id)
        self.bank_accounts.append(new_bank_account)
        return
