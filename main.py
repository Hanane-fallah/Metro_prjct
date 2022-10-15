import os

from bank import *
import logging
import hashlib
import uuid


# todo: exceptions handle - test -

logging.basicConfig(
    level=logging.DEBUG, # set logging level debug for check functions work
    format="{asctime} -{name:<10} -{levelname:<16} -{message}", style="{")

class User:
    user_dict = []

    def __init__(self, username, password, phone_number=None):
        self.username = username
        self.phone_number = phone_number
        self.__password = User.set_password(password)
        self.__id = uuid.uuid1()
        self.save_user()
        User.user_dict.append(self)
        logging.info(f"**user {self.username} with user id {self.__id} created**")

    def get_id(self):
        return self.__id

    def save_user(self):
        """
        save object in file
        """
        with open("users.pickled", "ab") as f:
            pickle.dump(self, f)

    @staticmethod
    def set_password(password):
        # encrypting password for more security
        password = password.encode('utf-8')
        return hashlib.md5(password).hexdigest()

    @staticmethod
    def check_password(password):
        # password must be at least 4 characters
        if len(password) > 3:
            return True
        else:
            logging.error("--invalid password--")

    @staticmethod
    def check_username(username):
        for usr in User.user_dict:
            if username == usr.username:
                logging.error("--invalid username--")
                return False
        else:
            return True

    @classmethod
    def user_assign(cls, username, password, phone_number=None):
        if User.check_password(password) and User.check_username(username):
            return cls(username, password, phone_number)

    def edit_user(self, username, phonenumber):
        if User.check_username(username):
            self.username = username
            self.phone_number = phonenumber
            logging.info(self)
        else:
            logging.error("user name taken!")

    def change_password(self, prepass, newpass):
        if User.set_password(prepass) == self.__password and User.check_password(newpass):
            self.__password = User.set_password(newpass)
            logging.debug("**password changed successfully**")
        else:
            logging.critical("--try again--")

    @staticmethod
    def user_login(username:str, password:str, user_id:str):
        # first check user exist
        for usr in User.user_dict:
            if str(user_id) == str(usr.__id):
                logging.debug("valid id")
                # second check username
                if username == usr.username:
                    logging.debug("valid username")
                    # last check password
                    if User.set_password(password) == usr.__password:
                        logging.debug("**login successfully**")
                        return usr
                    else:
                        logging.error("--wrong password--")
                else:
                    logging.error("--wrong username--")
            else:
                logging.error("--user does not exist--")

    def __str__(self):
        return f"user info ~> id = -{self.__id}- username = -{self.username}- phone number = -{self.phone_number}-"

    def __repr__(self):
        return f"id: {self.__id} username: {self.username}"


user_menu = """
1- display user info
2- edit username & phone number
3- change password
4- BANK
5- back to menu
"""
menu = """
0- quit program
1- user assignment
2- user login
"""


# user menu
def user_menu_func(opt, user):
    while opt != 5:
        if opt == 1:
            print(user)

        elif opt == 2:
            new_username = input("enter your new username:")
            new_phone_number = input("enter your new phone number:")
            user.edit_user(new_username, new_phone_number)

        elif opt == 3:
            prepass = input("enter your old password:")
            newpass = input("enter your new password:")
            user.change_password(prepass, newpass)

        elif opt == 4:
            clear()
            bank_main(user)

        clear()
        opt = int(input(f"{user_menu}enter option ~>"))
        clear()



# main menu
while True:
    clear()
    menu_opt = int(input(f"{menu}enter option ~> "))
    clear()
    try:
        if menu_opt == 1:
            # todo : optional phone number - constrained user & pass
            username = input("enter your username:")
            password = input("enter your password:")
            phonenumber = input("enter your phonenumber(optional):")
            if len(username) != 0: #check username length
                user = User.user_assign(username, password, phonenumber)
            else:
                logging.error("you must enter username")
                continue

        elif menu_opt == 2:
            print(User.user_dict)
            user_id = input("enter your id:")
            username = input("enter your username:")
            password = input("enter your password:")
            usr = User.user_login(username, password, user_id)
            if usr:
                clear()
                user_opt = int(input(f"{user_menu}enter option ~>"))
                user_menu_func(user_opt, usr)

        elif menu_opt == 0:
            break

        else:
            raise ValueError
    except ValueError:
        logging.error("--invalid input--")
