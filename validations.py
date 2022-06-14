import os


def password_checker(password):
    # symbols = ("!", "~", ">", "<", "?", "/", "*", "&", "^", "%", "$", '#', "@", "-", "_", " ")
    # numbers = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    is_strong = False
    for char in password:
        try:
            int(char)
            is_strong = True
            break
        except ValueError:
            is_strong = False
    return is_strong


def user_validation(username, password):
    reg_users = os.listdir("./login_details")
    is_valid = False
    for users in reg_users:
        if username == str(users.removesuffix(".txt")):
            f = open(f"./login_details/{users}", "r")
            user_details = f.read().split("\n")
            if password == user_details[3]:
                is_valid = True
                break
            else:
                is_valid = False
                break
        else:
            is_valid = False

    return is_valid
