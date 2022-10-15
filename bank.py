from metro_prj import *
# import uuid
import logging


logging.basicConfig(
    level=logging.INFO, # set logging level info
    format="{asctime} -{name:<10} -{levelname:<16} -{message}", style="{")


class BankAccount:
    all_accounts = [] # all accounts list
    MINBALANCE = 10

    def __init__(self, name, balance, id):
        if self.check_id(id):
            self.balance = balance
            self.__id = id # account id is same as user id (for access)
            self.name = name
            BankAccount.all_accounts.append(self)
            logging.info(f"account {self.__id} created, total balance : {self.balance}")
        else:
            logging.error("account exists with this id")

    def get_id(self):
        return self.__id

    @staticmethod
    def check_id(id):
        for acc in BankAccount.all_accounts:
            if id == acc.__id:
                return False
        return True


    def withdrawal(self, amount):
        if amount < (self.balance - BankAccount.MINBALANCE): #checking that withdrawal do
            self.balance -= amount
            logging.info(f"withdraw -{amount} and your total balance : {self.balance}")
            return self
        else:
            logging.error(f'invalid amount\tyour total balance: {self.balance}')

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            logging.info(f"deposit +{amount} and your total balance : {self.balance}")
            return self
        else:
            logging.error('invalid amount')

    def transfer(self, amount):
        sec_account = input("enter second account id => ")
        if amount < (self.balance - BankAccount.MINBALANCE):
            for acc in BankAccount.all_accounts:
                if str(sec_account) == str(acc.get_id()):
                    acc.deposit(amount)
                    self.withdrawal(amount)
                    logging.info(f"transfer +{amount} to {acc.__id} done!\tyour total balance : {self.balance}")
                    break
            else:
                logging.error('account not found')

        else:
            logging.error(f"you don't have enough money to transfer\tyour total money : {self.balance}")

    def __repr__(self):
        return f"account: {self.__id} balance: {self.balance}"



menu = """
__menu__:
1) create account
2) access account
3) quit
"""
account_menu = """
__options__:
1) display account info
2) deposit money
3) withdraw money
4) transfer
5) Metro
6) quit
"""


def account_opt(option, account):
    while option != 6:

        if option == 1:
            print(account)

        elif option == 2:
            print("_._.deposit._._")
            amount = float(input("Enter amount: "))
            account = account.deposit(amount)

        elif option == 3:
            print("_._.withdraw._._")
            amount = float(input("Enter amount: "))
            account = account.withdrawal(amount)

        elif option == 4:
            print("_._.transfer._._")
            amount = int(input("Enter amount: "))
            account = account.transfer(amount)

        elif option == 5:
            clear()
            main(account)

        else:
            logging.error("invalid input!")

        clear()
        option = int(input(f'{account_menu}\nEnter option: '))
        clear()


def bank_main(user):
    menu_option = input(f'{menu}\nEnter option: ')
    clear()
    while menu_option != 3:
        try:
            if int(menu_option) == 1:
                print("_._.create account._._\n")
                name = user.username
                id = user.get_id()
                money = float(input("Enter money: "))
                if money >= BankAccount.MINBALANCE:
                    account = BankAccount(name, money, id)
                else:
                    logging.error(f"minimun money is {BankAccount.MINBALANCE}")

            elif int(menu_option) == 2:
                print("_._.access account._._\n")
                account_num = input("Enter your account id: ")
                for account in BankAccount.all_accounts:
                    if str(account_num) == str(account.get_id()):
                        clear()
                        logging.info("login successfully")
                        account_option = int(input(f'{account_menu}\nEnter option: '))
                        account_opt(account_option, account)
                        break
                else:
                    logging.error("account not exist!")
            else:
                raise ValueError
        except ValueError:
            logging.critical("invalid input!")
        finally:
            clear()
            menu_option = int(input(f'{menu}\nEnter option: '))
            clear()


# if __name__ == "__main__":
#    bank_main()


