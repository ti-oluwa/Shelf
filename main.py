import os
import validations
import notes

# My diary project
# 1. create and account for user
# 2. create login for existing users
# 3. create a diary with a name they choose
# 4. create a text file with the name provided
# 5. ask user for entry to be saved in the directory with its date
# 6.  allow user create folders(section)
# 7. delete, edit and search functionality


def init():
    print("*~~~~~~~~~~SHELF~~~~~~~~~~*", "      Shelf is simple and user friendly note taking app you can use for taking down \nquick thoughts or logging down daily events", sep="\n")
    print("\n")
    print("Create and account today! or Login into your Shelf")
    init2()


def init2():
    print("(1) SignUp", "(2) Login", sep="\n")
    user_choice = input("> ")
    try:
        int(user_choice)
        if user_choice == "1":
            signup()
        elif user_choice == "2":
            login()
        else:
            print("Invalid option!")
            init2()
    except ValueError:
        print("Invalid input!!", "Choose 1 to signup or 2 to login", sep="\n")
        init2()


def login():
    print("LOGIN")
    username = str(input("Enter your username: "))
    password = str(input("Password: "))
    is_logged_in = validations.user_validation(username, password)
    if is_logged_in:
        print("Login Successful")
        notes.available_actions(username)
    else:
        print("Invalid Login details")
        login()


def signup():
    print("SIGNUP")
    print("Would you like to create an account? if yes type 'yes' and if no type 'no'.")
    user_resp = str(input("> ").lower())
    try:
        int(user_resp)
        print("Incorrect input, Try again!")
        signup()

    except ValueError or TypeError:
        if user_resp == "yes":
            create_account()
        elif user_resp == "no":
            print("Thanks for checking Shelf out. You are now exiting Shelf", "..............................", "GOODBYE", sep="\n")
            exit()
        else:
            print("invalid response")
            signup()


def create_account():
    firstname = str(input("Enter your first name> \n"))
    lastname = str(input("Enter your last name> \n"))
    user_age = input("How old are you? \n")
    try:
        int(user_age)
        username = create_user(firstname, lastname, user_age)
        print("~USER ACCOUNT CREATED SUCCESSFULLY~\n")
        notes.available_actions(username)
    except ValueError:
        print("Age is supposed to be a number")
        create_account()



def create_user(firstname, lastname, user_age):
    username = str(input("Create a username> \n"))
    print("Your password should contain at least a number and/ or a symbol")
    password = input("Create a strong password> ")
    is_strong = validations.password_checker(password)
    is_user_dir_created = False
    if is_strong:
        try:
            os.mkdir(f"./user_shelfs/{username}")
            is_user_dir_created = True

        except OSError:
            is_user_dir_created = False
            print(f"Username already exists")
            print("Choose another username")
            create_user(firstname, lastname, user_age)
    else:
        print("Error! Password is to weak")
        create_user(firstname, lastname, user_age)

    if is_user_dir_created:
        f = open(f"./login_details/{username}.txt", "x")
        f.write(f"{firstname}\n{lastname}\n{user_age}\n{password}")
        f.close()
        return username


init()

