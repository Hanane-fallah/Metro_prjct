import logging
import datetime
import pickle
from bank import *
import os

# todo: test - os clean - trip file

logging.basicConfig(
    level=logging.DEBUG,  # set logging level debug to check functions work
    format="{asctime} -{name:<10} -{levelname:<16} -{message}", style="{",
    handlers=[
        logging.FileHandler("metro.log"),  # log file
        logging.StreamHandler()
    ]
)


class MetroCard:
    COST = 10

    def __init__(self, card_no: int, value: float):
        self.value = value
        if self.check_value(MetroCard.COST):  # check that initilize value isn`t negative or under one trip cost
            self.num = card_no
            self.save_card()  # saving object info in file
            logging.info(f"***** CARD {self} Exported *****")
        else:
            logging.critical("----- you must have atleast 10 values -----")

    def save_card(self):
        """
        save object in file
        """
        with open("card.pickled", "ab") as f:
            pickle.dump(self, f)

    @classmethod
    def load_info(cls, filename):
        with open(filename, "rb") as f:
            while True:
                try:
                    yield pickle.load(f)
                except EOFError:
                    break

    def update_info(self):
        """
        finding specified card and update its value
        """
        card_list = []
        f1 = open("card.pickled", "rb+")
        while True:
            try:
                L = pickle.load(f1)
                if L.num == self.num:
                    L.value = self.value
                card_list.append(L)

            except EOFError:
                break

        f1.seek(0)
        f1.truncate()
        for i in card_list:
            i.save_card()
        else:
            f1.close()

    def check_value(self, amount) -> bool:
        """
        checking that we can discount specified amount from card value
        :param amount: the amount of value we want to check
        """
        if self.value - amount >= 0:
            logging.debug("----- valid amount -----")
            return True  # FOR TEST
        return False  # FOR TEST

    def trip_func(self):
        start_time = datetime.datetime.now().strftime("%H:%M:%S")  # start trip time
        if self.check_value(MetroCard.COST):
            self.value -= MetroCard.COST
            self.update_info()
            end_time = datetime.datetime.now().strftime("%H:%M:%S")  # end trip time
            logging.info(
                f"***** TRIP DONE start:{start_time} * end:{end_time} * cost => {MetroCard.COST} * remaining value => {self.value} *****")
            # return "Done" # FOR TEST
        else:
            logging.critical("----- you don`t have enough value -----")
            # return "Fail" # FOR TEST

    def charge_value(self, value):
        self.value += value
        self.update_info()
        logging.info(f"CARD {self}")
        return self.value  # FOR TEST

    def __repr__(self):
        return f"-{self.num}- value:{self.value}"


class OneTrip(MetroCard):

    def __init__(self, card_no, value=10):
        super().__init__(card_no, value)

    def trip_func(self):
        """
        overriding parent trip_func
        one trip cards can be used only one time
        """
        if self.value:
            logging.debug("----- One TRIP CARD USED -----")
            self.value = False
            self.update_info()
        else:
            logging.critical("----- CARD EXPIRED -----")

    def charge_value(self, value):
        logging.critical("----- one trip card dont have charge value option -----")


# todo: type anno for child class?
class TimeCredit(MetroCard):

    def __init__(self, card_no: int, value: float, time_op: int):
        self.time = TimeCredit.card_time_func(time_op)
        super().__init__(card_no, value)

    @staticmethod
    def card_time_func(time_op) -> datetime:
        """
        setting time attribute base on user choice
        :param time_op: user choise 1-one day 2-one weeek 3-one month
        :return: value of time attribute (to be initilized in init)
        """
        today = datetime.date.today()
        if time_op == 1:
            return today + datetime.timedelta(days=1)
        elif time_op == 2:
            return today + datetime.timedelta(days=7)
        elif time_op == 3:
            return today + datetime.timedelta(days=30)

    def trip_func(self):
        if self.check_time():
            super().trip_func()
            today = datetime.date.today()
            r_days = self.time - today  # get remaining days of the card
            logging.info(f"----- {r_days.days} Days Remaining -----")

    def check_time(self):
        """
        check card time
        """
        today = datetime.date.today()
        if self.time > today:
            return True  # FOR TEST
        else:
            logging.critical(f"----- CARD -{self.num}- Time EXPIRED -----")
            self.value = False  # because the card is expired and doesn`t have charge option in menu (L 245)
            return False  # FOR TEST

    def __repr__(self):
        return f"-{self.num}- val:{self.value} expire:{self.time}"


class Credit(MetroCard):
    pass


num = 101  # todo: generate number
def card_number_func():
    global num
    num += 1
    return num


menu = """
1- RECEIVE Card
2- USE Card
3- EXIT
"""
receive_menu = """
1- one trip
2- credit time
3- credit
"""
plan = """
1- one day
2- one week
3- one month
"""


def export_card(account):
    card_type = int(input(f"{receive_menu}\nChoose card ~> "))
    if card_type == 1:  # one trip card
        account.withdrawal(MetroCard.COST)
        num = card_number_func()  # generate card number
        card = OneTrip(card_no=num)  # creating card

    elif card_type == 2:  # time credit card
        value = int(input("Enter value => "))
        time_op = int(input(f"TODAY : {datetime.date.today()}{plan}\nchoose plan => "))
        account.withdrawal(value)
        num = card_number_func()  # generate card number
        card = TimeCredit(card_no=num, value=value, time_op=time_op)

    elif card_type == 3:
        value = int(input("enter value => "))
        account.withdrawal(value)
        num = card_number_func()
        card = Credit(num, value)

    else:
        raise ValueError


def main(account):
    print("***** WELCOME *****")
    try:
        menu_func(account)
    except (ValueError, FileNotFoundError):
        print("----- Invalid Input -----")
        main(account)


def menu_func(account):
    while True:
        menu_opt = int(input(f"{menu}\nEnter Option ~> "))
        if menu_opt == 1:
            try:
                export_card(account)
            except ValueError:
                print("----- Invalid Input -----")
            finally:
                continue

        elif menu_opt == 2:
            print(list(MetroCard.load_info("card.pickled")))
            c_list = list(MetroCard.load_info("card.pickled"))
            try:
                card = input("Enter card number => ")
                for c in c_list:
                    if c.num == int(card):
                        logging.debug("----- login successfully -----")
                        c.trip_func()
                        if c.value == False:
                            break
                        else:
                            ans = input("You want to charge your card? y / n\n")
                            if ans == "y":
                                new_val = (int(input(f"{c}\nHow many trips ~>"))) * 10
                                account.withdrawal(new_val)
                                c.charge_value(new_val)
                            break
                else:
                    raise ValueError

            except ValueError:
                print("----- Invalid Input -----")

            finally:
                continue

        elif menu_opt == 3:
            break

        else:
            raise ValueError

# main()
