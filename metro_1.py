import logging
import datetime
import pickle
import os
# todo: test - os clean
# logging.basicConfig(filename='metro.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class MetroCard:
    COST = 10
    def __init__(self, card_no:int, value:float):
        self.value = value
        if self.check_value(10):
            self.num = card_no
            self.save_card()
            logging.info(f"***** CARD {self} Exported *****")
        else:
            logging.critical("----- you must have atleast 10 values -----")

    def save_card(self):
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
        # todo: faster way?
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

    def check_value(self, amount):
        if self.value - amount >= 0:
            logging.debug("----- valid amount -----")
            return True

    def trip_func(self):
        if self.check_value(MetroCard.COST):
            self.value -= MetroCard.COST
            self.update_info()
            logging.info(f"***** TRIP DONE remaining value => {self.value} *****")
        else:
            logging.critical("----- you don`t have enough value -----")

    def charge_value(self, value):
        self.value += value
        self.update_info()
        print("CARD ", self)

    def __repr__(self):
        return f"-{self.num}- value:{self.value}"

class OneTrip(MetroCard):

    def trip_func(self):
        if self.value:
            logging.debug("----- One TRIP CARD USED -----")
            self.value = False
            self.update_info()
        else:
            logging.critical("----- CARD EXPIRED -----")

    def charge_value(self, value):
        pass

# todo: type anno for child class?
class TimeCredit(MetroCard):

    def __init__(self, card_no:int, value:float, time_op):
        # self.time = time
        self.card_time_func(time_op)
        super().__init__(card_no, value)

    def card_time_func(self, time_op) -> datetime:
        today = datetime.date.today()
        if time_op == 1:
            self.time = today + datetime.timedelta(days=1)
        if time_op == 2:
            self.time = today + datetime.timedelta(days=7)
        if time_op == 3:
            self.time = today + datetime.timedelta(days=30)

    def trip_func(self):
        if self.check_time():
            super().trip_func()
            r_days = self.time.day - datetime.date.today().day
            logging.info(f"----- {r_days} Days Remaining -----")

    def check_time(self):
        today = datetime.date.today()
        if self.time >= today:
            return True
        else:
            logging.critical(f"----- CARD -{self.num}- Time EXPIRED -----")
            return False

    def __repr__(self):
        return f"-{self.num}- val:{self.value} expire:{self.time}"


class Credit(MetroCard):
    pass


num = 100 # todo: generate number
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

def export_card():
    card_type = int(input(f"{receive_menu}\nChoose card ~> "))
    if card_type == 1:
        num = card_number_func()
        card = OneTrip(card_no=num, value=10)

    if card_type == 2:
        value = int(input("Enter value => "))
        time = int(input(f"TODAY : {datetime.date.today()}\n{plan}\nchoose plan => "))
        num = card_number_func()
        card = TimeCredit(card_no=num, value=value, time_op=time)

    if card_type == 3:
        value = int(input("enter value => "))
        num = card_number_func()
        card = Credit(num, value)

    else:
        raise ValueError


def main():
    print("***** WELCOME *****")
    try:
        menu_func()
    except ValueError:
        print("----- Invalid Input -----")
        menu_func()

def menu_func():
    while True:
        menu_opt = int(input(f"{menu}\nEnter Option ~> "))
        if menu_opt == 1:
            try:
                export_card()
            except ValueError:
                print("----- Invalid Input -----")
            finally:
                continue

        if menu_opt == 2:
            print(list(MetroCard.load_info("card.pickled")))
            c_list = list(MetroCard.load_info("card.pickled"))
            try:
                card = input("Enter card number => ")
                for c in c_list:
                    if c.num == int(card):
                        logging.debug("----- login successfully -----")
                        c.trip_func()
                        if c.value == False or c.check_time == False:
                            break
                        ans = input("You want to charge your card? y / n\n")
                        if ans == "y":
                            new_val = (int(input(f"{c}\nHow many trips ~>"))) * 10
                            c.charge_value(new_val)
                        break
                else:
                    raise ValueError

            except ValueError:
                print("----- Invalid Input -----")

            finally:
                continue

        if menu_opt == 3:
            break

        else:
            raise ValueError
main()
