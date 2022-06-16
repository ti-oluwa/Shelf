import datetime
import os


def available_actions(username):
    print(f"----------{username.upper()}'S SHELF----------")
    print("Would you like to add/create a note or check an existing note?")
    print("(1) Create note", "(2) Search for an existing note", "(3) Delete a note", "(4) Exit",  sep="\n")
    response = input("=> ")
    try:
        int(response)
        if response == "1":
            new_note(username)
        elif response == "2":
            update_note(username)
        elif response == "3":
            delete_note(username)
        elif response == "4":
            exit()
        else:
            print("Invalid option!")

    except ValueError:
        print("Invalid input!!", "Choose 1 to signup or 2 to login", sep="\n")
        available_actions(username)


def new_note(username):
    print("Create a name for your new note")
    note_name = str(input("=> "))
    is_note_created = False
    while is_note_created is False:
        print("Press any key and <Enter> to add this note to your shelf")
        key = str(input(">> "))
        try:
            str(key)
            try:
                f = open(f'./user_shelfs/{username}/{note_name}.txt', "x")
                f.close()
                is_note_created = True
            except FileExistsError:
                print("Name is already used for an existing note")
                new_note(username)
        except ValueError:
            is_note_created = False

    if is_note_created:
        note = open_note(username, note_name)
        print("Note Opened\n")
        print(f"~~~~~~~~~~~~~~{note_name.upper()}~~~~~~~~~~~~~~")
        text = str(input("Type in text >>> \n"))
        if len(text) < 16:
            is_note_saved = False
            while is_note_saved is False:
                print("ARE YOU SURE YOU WANT TO SAVE THIS NOTE ? IT DOESN'T CONTAIN MUCH TEXT!\n")
                response = input("y/n>> ")
                if response == "y":
                    note.write(f"{text}\n")
                    note.write(f"{datetime.date.today()}\n")
                    note.write(f"{datetime.datetime.now().strftime('%H:%M')}\n")
                    note.write("\n")
                    note.close()
                    print("~NOTE SAVED~\n")
                    available_actions(username)
                if response == "n":
                    print("~NOTE DISCARDED~\n")
                    available_actions(username)
                else:
                    is_note_saved = False
        else:
            note.write(f"{text}\n")
            note.write(f"{datetime.date.today()}\n")
            note.write(f"{datetime.datetime.now().strftime('%H:%M')}\n")
            note.write("\n")
            note.close()
            print("~NOTE SAVED~\n")
            available_actions(username)


def update_note(username):
    print('These is a list of the notes in your shelf')
    notes = os.listdir(f"./user_shelfs/{username}")
    x = 1
    for items in notes:
        print(f"[{x}] {items.removesuffix('txt')}")
        x += 1
    print("*************************************************\n")

    is_choice_valid = False
    needed_note_index = ""
    choices = []
    while is_choice_valid is False:
        i = 0
        for items in notes:
            choices.append(i)
            print(f'Enter ({i}) to open "{items.removesuffix(".txt")}"')
            i += 1
        print("\n")
        needed_note_index = input("=>> ")
        try:
            int(needed_note_index)
            if len(needed_note_index) == 1:
                if int(needed_note_index) in choices:
                    is_choice_valid = True
            else:
                is_choice_valid = False
        except ValueError:
            print("Invalid Choice!\n")
            is_choice_valid = False

    note_name = search_note_by_index(username, int(needed_note_index))
    note = open_note(username, note_name)
    print(f"~~~~~~~~~~~~~~{note_name.upper()}~~~~~~~~~~~~~~")
    previous_text = open(f"./user_shelfs/{username}/{note_name}.txt", "r+").read()
    print(previous_text)
    text = str(input("Type in text >>> "))
    if len(text) < 16:
        is_note_saved = False
        while is_note_saved is False:
            print("ARE YOU SURE YOU WANT TO SAVE THIS NOTE ? IT DOESN'T CONTAIN MUCH TEXT!\n")
            response = input("y/n>> ")
            if response == "y":
                note.write(f"{text}\n")
                note.write(f"{datetime.date.today()}\n")
                note.write(f"{datetime.datetime.now().strftime('%H:%M')}\n")
                note.write("\n")
                note.close()
                print("~NOTE SAVED~\n")
                available_actions(username)
            if response == "n":
                print("~NOTE DISCARDED~\n")
                available_actions(username)
            else:
                is_note_saved = False
    else:
        note.write(f"{text}\n")
        note.write(f"{datetime.date.today()}\n")
        note.write(f"{datetime.datetime.now().strftime('%H:%M')}\n")
        note.write("\n")
        note.close()
        print("~NOTE SAVED~\n")
        available_actions(username)


def open_note(username, note_name):
    try:
        f = open(f"./user_shelfs/{username}/{note_name}.txt", "r+")
        listed_note = f.read().split("\n")
        if listed_note == []:
            f = open(f"./user_shelfs/{username}/{note_name}.txt", "a+")
            f.write(f"This note was created {datetime.date.today()}\n")
            f.write(f"{datetime.datetime.now().strftime('%H:%M')}\n")
            f.write("\n")
            f.write("\n")
            f.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            note = f
        else:
            f = open(f"./user_shelfs/{username}/{note_name}.txt", "a+")
            note = f
        return note
    except FileNotFoundError:
        return False


def search_note_by_name(username, notename):
    notes = os.listdir(f"./user_shelfs/{username}")
    needed_note = False
    for i in notes:
        if notename == str(i.removesuffix(".txt")):
            needed_note = i
            break
        else:
            needed_note = False
    return needed_note


def search_note_by_index(username, note_index):
    notes = os.listdir(f"./user_shelfs/{username}")
    # f = open(f"./user_shelfs/{username}/{notes[note_index]}", "r+")
    needed_note = notes[note_index].removesuffix(".txt")
    return needed_note


def delete_note(username):
    print('These is a list of the notes in your shelf')
    notes = os.listdir(f"./user_shelfs/{username}")
    x = 1
    for items in notes:
        print(f"[{x}] {items}")
        x += 1
    print("*************************************************\n")

    is_choice_valid = False
    needed_note_index = ""
    while is_choice_valid is False:
        i = 0
        for items in notes:
            print(f'Enter ({i}) to delete "{items.removesuffix(".txt")}"')
            i += 1
        print("\n")
        needed_note_index = input("=>> ")
        try:
            int(needed_note_index)
            if len(needed_note_index) == 1:
                is_choice_valid = True
            else:
                is_choice_valid = False
        except ValueError:
            print("Invalid Choice!\n")
            is_choice_valid = False
    notename = search_note_by_index(username, int(needed_note_index))
    is_valid = False
    print(f"*****ARE SURE YOU WANT TO DELETE {notename.upper()}?*****")
    while is_valid is False:
        user_response = input("y/n => ").lower()
        if user_response == "y":
            os.remove(f"./user_shelfs/{username}/{notename}.txt")
            print(f"{notename.upper()} DELETED!")
            available_actions(username)
            is_valid = True
        elif user_response == "n":
            available_actions(username)
            is_valid = True
        else:
            is_valid = False
