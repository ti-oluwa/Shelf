import datetime
import os
# from typing import NoReturn


def available_actions(username):
    print(f"----------{username.upper()}'S SHELF----------")
    print("Would you like to add/create a note or check an existing note?")
    print("(1) Create note", "(2) Search for an existing note", "(3) Search", "(4) Delete a note", "(5) Exit", sep="\n")
    response = input("=> ")
    try:
        int(response)
        if response == "1":
            new_note(username)
        elif response == "2":
            update_note(username)
        elif response == "3":
            search(username)
        elif response == "4":
            delete_note(username)
        elif response == "5":
            exit()
        else:
            print("Invalid option!")

    except ValueError:
        print("Invalid input!")
        available_actions(username)


def new_note(username):
    print("Create a name for your new note")
    note_name = str(input("=> "))
    is_note_created = False
    while is_note_created is False:
        print("Press any key and <ENTER> to add this note to your shelf")
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
    notes = os.listdir(f"./user_shelfs/{username}")
    if notes != []:
        print('These is a list of the notes in your shelf')
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
                print(f'ENTER [{i}] to open "{items.removesuffix(".txt")}"')
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
        try:
            previous_text = open(f"./user_shelfs/{username}/{note_name}.txt", "r+").read()
            print(f"~~~~~~~~~~~~~~{note_name.upper()}~~~~~~~~~~~~~~")
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

        except FileNotFoundError:
            print("FILE NOT FOUND!")
            available_actions(username)
    else:
        print('~YOUR SHELF IS EMPTY~')
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
    

def search_note_by_name_return_index(username, notename):
    notes = os.listdir(f"./user_shelfs/{username}")
    needed_note_index = ''
    x = 0
    for i in notes:
        if notename.lower() == str(i.removesuffix(".txt").lower()):
            needed_note_index = x
            break
        else:
            needed_note_index = ' '
        x += 1

    return needed_note_index

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
            print(f'ENTER [{i}] to delete "{items.removesuffix(".txt").upper()}"')
            i += 1
        print(f"ENTER [{len(notes)}] to DELETE ALL")
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

    if int(needed_note_index) < len(notes):
        notename = search_note_by_index(username, int(needed_note_index))
        is_valid = False
        print(f"*****ARE SURE YOU WANT TO DELETE {notename.upper()}?*****")
        while is_valid is False:
            user_response = input("y/n => ").lower()
            if user_response == "y":
                os.remove(f"./user_shelfs/{username}/{notename}.txt")
                print(f"~{notename.upper()} DELETED!~")
                available_actions(username)
                is_valid = True
            elif user_response == "n":
                available_actions(username)
                is_valid = True
            else:
                is_valid = False
    else:
        is_valid = False
        print(f"*****ARE SURE YOU WANT TO REMOVE ALL NOTES FROM YOUR SHELF?*****")
        while is_valid is False:
            user_response = input("y/n => ").lower()
            if user_response == "y":
                for items in notes:
                    os.remove(f"./user_shelfs/{username}/{items}")
                    print(f"~SHELF EMPTIED!~")
                    available_actions(username)
                    is_valid = True
            elif user_response == "n":
                available_actions(username)
                is_valid = True
            else:
                print("Invalid response!!\n")
                is_valid = False


def search(username):
    search_ = list(input("SEARCH >> ").lower())
    user_notes = os.listdir(f"./user_shelfs/{username}")
    notes_list = []
    possible_search_result = []
    for items in user_notes:
        notes_list.append((items.removesuffix(".txt").lower()))
    if notes_list != []:
        for i in notes_list:
            x = 0
            while x < len(search_):
                if search_[x] in i:
                    if x == (len(search_) - 1):
                        possible_search_result.append(i)
                    x += 1
                else:
                    x = len(search_)
    else:
        print("NO MATCH FOR SEARCH!( You might have no note created yet )")
        available_actions(username)
    if possible_search_result != []:
        print("SEARCH RESULTS:  ")
        a = 1
        for notes in possible_search_result:
                print(f"({a}) {notes}")
                a += 1
        is_choice_valid = False
        while is_choice_valid is False:
            a = 1
            for notes in possible_search_result:
                print(f"ENTER [{a}] to open {notes}\n")
                a += 1
            response = input(">> ")
            
            try:
                int(response)
                if len(response) == 1:
                    is_choice_valid = True
                
            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False

        note_name = possible_search_result[int(response)-1]
        print(note_name)      
        note_index = search_note_by_name_return_index(username, note_name)
        note_name = search_note_by_index(username, int(note_index))
        note = open_note(username, note_name)
        try:
            previous_text = open(f"./user_shelfs/{username}/{note_name}.txt", "r+").read()
            print(f"~~~~~~~~~~~~~~{note_name.upper()}~~~~~~~~~~~~~~")
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
        except FileNotFoundError:
            print("FILE NOT FOUND!")
            available_actions(username)
    else:
        print("NO MATCH FOR SEARCH!\n")
        search(username)