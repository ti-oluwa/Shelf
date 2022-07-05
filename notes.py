import datetime
import os
import shutil
# from typing import NoReturn


def available_actions(username):
    print(f"----------{username.upper()}'S SHELF----------")
    print("Would you like to add/create a note or check an existing note?")
    print("(1) Create note", "(2) Search for an existing note(IF THE NOTE IS IN A SECTION, NAVIGATE TO SECTIONS OR USE SEARCH)", "(3) Search", "(4) Delete a note", "(5) Create Section", "(6) Sections", "(7) Exit", sep="\n")
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
            make_folder(username)
        elif response == '6':
            sections(username)
        elif response == '7':
            exit()
        else:
            print("Invalid option!")

    except ValueError:
        print("Invalid input!")
        available_actions(username)


def new_note(username):
    print("Create a name for your new note")
    note_name = str(input("=> ").lower())
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
                print("Name is already used for an existing note\n")
                is_valid = False
                while is_valid is False:
                            user_response = input("Do you still want to proceed? y/n => ").lower()
                            if user_response == "y":
                                is_valid = True
                            elif user_response == "n":
                                new_note(username)
                                is_valid = True
                            else:
                                is_valid = False
                if is_valid:
                    destination_folder = os.listdir(f'./user_shelfs/{username}')
                    no_of_like_notes = 0
                    like_notes = []
                    for notes in destination_folder:
                        if note_name in notes.removesuffix('.txt'):
                            like_notes.append(notes.removesuffix('.txt'))
                            no_of_like_notes += 1
                            
                    if no_of_like_notes > 0:
                        indices = []
                        for index,notes in enumerate(like_notes):
                            indices.append(index)
                        
                        new_index =int(indices[-1]) + 1
                        new_note_name = note_name + str(new_index)
                        f = open(f'./user_shelfs/{username}/{note_name}.txt', "x")
                        print(f"\n'{note_name}' has been created as {new_note_name}")
                        f.close()
                        is_note_created = True
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
    for items in notes:
        if items == 'sections':
            notes.remove(items)
    if notes != []:
        print('These is a list of the notes in your shelf')
        x = 1
        for items in notes:
            if '.txt' in items:
                print(f"[{x}] {items.removesuffix('.txt')}")
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
                if int(needed_note_index) in choices:
                    is_choice_valid = True
                else:
                    is_choice_valid = False
            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False
        needed_note_index = int(needed_note_index) + 1
        print(needed_note_index)
        note_name = search_note_by_index(username, needed_note_index)
        print(note_name)
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
            print("FILE NOT FOUND!\n")
            available_actions(username)
    else:
        print('\n~YOUR SHELF IS EMPTY~', '~TRY CHECKING SECTIONS~\n', sep='\n')
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

def open_note_for_section(username, section_name, note_name):
    try:
        f = open(f"./user_shelfs/{username}/sections/{section_name}/{note_name}.txt", "r+")
        listed_note = f.read().split("\n")
        if listed_note == []:
            f = open(f"./user_shelfs/{username}/sections/{section_name}/{note_name}.txt", "a+")
            f.write(f"This note was created {datetime.date.today()}\n")
            f.write(f"{datetime.datetime.now().strftime('%H:%M')}\n")
            f.write("\n")
            f.write("\n")
            f.write("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            note = f
        else:
            f = open(f"./user_shelfs/{username}/sections/{section_name}/{note_name}.txt", "a+")
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
    print(notes)
    # f = open(f"./user_shelfs/{username}/{notes[note_index]}", "r+")
    needed_note = notes[note_index].removesuffix(".txt")
    print(needed_note)
    return needed_note

def search_section_by_index(username, section_index):
    sections = os.listdir(f"./user_shelfs/{username}/sections")
    # f = open(f"./user_shelfs/{username}/{notes[note_index]}", "r+")
    needed_section = sections[section_index]
    return needed_section


def search_note_by_index_for_section(username, section_name, note_index):
    notes = os.listdir(f"./user_shelfs/{username}/sections/{section_name}")
    # f = open(f"./user_shelfs/{username}/{notes[note_index]}", "r+")
    needed_note = notes[note_index].removesuffix(".txt")
    return needed_note



def delete_note(username):
    notes = os.listdir(f"./user_shelfs/{username}")
    if notes != []:
        print('These is a list of the notes in your shelf')
        x = 1
        for items in notes:
            if '.txt' in items:
                print(f"[{x}] {items}")
                x += 1
        print("*************************************************\n")

        is_choice_valid = False
        needed_note_index = ""
        while is_choice_valid is False:
            i = 0
            for items in notes:
                if '.txt' in items:
                    print(f'ENTER [{i}] to delete "{items.removesuffix(".txt").upper()}"')
                    i += 1
            print(f"ENTER [{len(notes)}] to DELETE ALL")
            print("\n")
            needed_note_index = input("=>> ")
            try:
                int(needed_note_index)        
                is_choice_valid = True

            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False
        
        if int(needed_note_index) < len(notes):
            notename = search_note_by_index(username, int(needed_note_index) + 1)
            is_valid = False
            print(f"*****ARE SURE YOU WANT TO DELETE {notename.upper()}?*****")
            while is_valid is False:
                user_response = input("y/n => ").lower()
                if user_response == "y":
                    os.remove(f"./user_shelfs/{username}/{notename}.txt")
                    print(f"~{notename.upper()} DELETED!~\n")
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
                        print(f"~SHELF EMPTIED!~\n")
                        available_actions(username)
                        is_valid = True
                elif user_response == "n":
                    available_actions(username)
                    is_valid = True
                else:
                    print("Invalid response!!\n")
                    is_valid = False
    else:
        print('\n~YOUR SHELF IS ALREADY EMPTY~\n')
        available_actions(username)


def delete_section(username):
    sections_ = os.listdir(f"./user_shelfs/{username}/sections")
    if sections_ != []:
        print('These is a list of the sections in your shelf')
        x = 1
        for items in sections_:
            if '.txt' in items:
                print(f"[{x}] {items}")
                x += 1
        print("*************************************************\n")

        is_choice_valid = False
        needed_section_index = ""
        while is_choice_valid is False:
            i = 0
            for items in sections_:
                print(f'ENTER [{i}] to delete "{items.upper()}"')
                i += 1
            print(f"ENTER [{len(sections_)}] to DELETE ALL")
            print("\n")
            needed_section_index = input("=>> ")
            try:
                int(needed_section_index)        
                is_choice_valid = True

            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False
        
        if int(needed_section_index) < len(sections_):
            section_name = search_section_by_index(username, int(needed_section_index))
            is_valid = False
            print(f"*****ARE SURE YOU WANT TO DELETE {section_name.upper()}?*****")
            while is_valid is False:
                user_response = input("y/n => ").lower()
                if user_response == "y":
                    os.rmdir(f"./user_shelfs/{username}/sections/{section_name}")
                    print(f"~{section_name.upper()} DELETED!~\n")
                    sections(username)
                    is_valid = True
                elif user_response == "n":
                    sections(username)
                    is_valid = True
                else:
                    is_valid = False
        else:
            is_valid = False
            print(f"*****ARE SURE YOU WANT TO REMOVE ALL NOTES FROM YOUR SHELF?*****")
            while is_valid is False:
                user_response = input("y/n => ").lower()
                if user_response == "y":
                    for items in sections_:
                        os.rmdir(f"./user_shelfs/{username}/sections/{items}")
                        print(f"~SHELF EMPTIED!~\n")
                        sections(username)
                        is_valid = True
                elif user_response == "n":
                    sections(username)
                    is_valid = True
                else:
                    print("Invalid response!!\n")
                    is_valid = False
    else:
        print('\n~YOUR HAVE NO SECTION CREATED~\n')
        sections(username)



def delete_note_for_section(username, section_name):
    notes = os.listdir(f"./user_shelfs/{username}/sections/{section_name}")
    if notes != []:
        print('These is a list of the notes in this section')
        x = 1
        for items in notes:
            if '.txt' in items:
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
                is_choice_valid = True
            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False
    
        if int(needed_note_index) < len(notes):
            notename = search_note_by_index_for_section(username, section_name, int(needed_note_index))
            is_valid = False
            print(f"*****ARE SURE YOU WANT TO DELETE {notename.upper()}?*****")
            while is_valid is False:
                user_response = input("y/n => ").lower()
                if user_response == "y":
                    os.remove(f"./user_shelfs/{username}/sections/{section_name}/{notename}.txt")
                    print(f"~{notename.upper()} DELETED!~\n")
                    sections(username)
                    is_valid = True
                elif user_response == "n":
                    sections(username)
                    is_valid = True
                else:
                    is_valid = False
        else:
            is_valid = False
            print(f"*****ARE SURE YOU WANT TO REMOVE ALL NOTES FROM {section_name.upper()}?*****") 
            while is_valid is False:
                user_response = input("y/n => ").lower()
                if user_response == "y":
                    for items in notes:
                        os.remove(f"./user_shelfs/{username}/sections/{section_name}/{items}")
                        print(f"~SECTION EMPTIED!~\n")
                        sections(username)
                        is_valid = True
                elif user_response == "n":
                    sections(username)
                    is_valid = True
                else:
                    print("Invalid response!!\n")
                    is_valid = False
    else:
        print('\n~THIS SECTION IS ALREADY EMPTY~\n')
        sections(username)


def search(username):
    search_ = list(input("SEARCH >> ").lower())
    user_notes = os.listdir(f"./user_shelfs/{username}")
    user_sections = os.listdir(f'./user_shelfs/{username}/sections')
    if user_sections != []:
        notes_in_sections = []
        for item in user_sections:
            section = os.listdir(f'./user_shelfs/{username}/sections/{item}')
            for notes in section:
                notes_in_sections.append(notes)
    user_notes_and_sections = user_notes + user_sections +notes_in_sections
    print(user_notes_and_sections)
    notes_list = []
    possible_search_result = []
    for items in user_notes_and_sections:
        if '.txt' in items:
            notes_list.append((items.removesuffix(".txt").lower()))
        else:
            notes_list.append((items.lower()))

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
            if notes != 'sections':
                print(f"({a}) {notes}")
                a += 1
        is_choice_valid = False
        while is_choice_valid is False:
            a = 1
            choices = []
            for notes in possible_search_result:
                if notes != 'sections':
                    choices.append(a)
                    print(f"ENTER [{a}] to open {notes}\n")
                    a += 1
            response = input(">> ")
          #continue from here  
            try:
                int(response)
                if len(response) == 1:
                    if response in choices:
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
        available_actions(username)

def sections(username):
    print('\n**********SECTIONS**********\n')
    print("(1) Create section", "(2) Search", "(3) Sections", "(4) Move note to section", "(5) Delete section", "(6) Redirect back to main shelf ", sep="\n")
    response = input("=> ")
    try:
        int(response)
        if response == "1":
            make_folder(username)
        elif response == "2":
            search(username)
        elif response == "3":
            list_folders(username)
        elif response == "4":
            add_to_folder(username)
        elif response == "5":
            delete_section(username)
        elif response == "6":
            available_actions(username)
        else:
            print("Invalid option!")
            sections(username)

    except ValueError:
        print("Invalid input!")
        sections(username)


def make_folder(username):
    is_created = False
    try:
        is_already_created = True
        os.makedirs(f'./user_shelfs/{username}/sections')
        is_already_created = False
        if is_already_created is False:
            while is_created is False:
                    folder_name = input('Enter section name>> ')
                    if folder_name and  folder_name != ' ':
                        try:
                            os.makedirs(f'./user_shelfs/{username}/sections/{folder_name}(section)')
                            print(f"'{folder_name}' has been created!\n")
                            sections(username)
                            is_created = True
                            
                        except FileExistsError:
                            print('Section name has already been used\n')
                            is_created = False
                    else:
                        print('\n~ENTER A NAME~\n')
                        is_created = False
    except FileExistsError:
                while is_created is False:    
                    folder_name = input('Enter section name>> ')
                    if folder_name and  folder_name != ' ':
                        print(folder_name)
                        try:
                            os.makedirs(f'./user_shelfs/{username}/sections/{folder_name}(section)')
                            print(f"'{folder_name}' has been created!\n")
                            sections(username)
                            is_created = True 
                        except FileExistsError:
                            print('Section name has already been used\n')
                            is_created = False
                    else:
                        print('\n~ENTER A NAME~\n')
                        is_created = False


def list_folders(username):
    sections_ = os.listdir(f'./user_shelfs/{username}/sections')
    print('*****SECTIONS*****/n')
    x = 1
    for section in sections_:
        if len(sections_) == 0:
            print('SORRY NO NOTE FOUND!')
            sections(username)
        else:
            print(f"[{x}] {section}")
            x += 1
    
    is_choice_valid = False
    needed_section_index = ""
    choices = []
    while is_choice_valid is False:
        i = 0
        for items in sections_:
            choices.append(i)
            print(f'ENTER [{i}] to open "{items.removesuffix(".txt")}"')
            i += 1
        print("\n")
        needed_section_index = input("=>> ")
        try:
            int(needed_section_index)
            if int(needed_section_index) in choices:
                is_choice_valid = True
            else:
                is_choice_valid = False
        except ValueError:
            print("Invalid Choice!\n")
            is_choice_valid = False

        if is_choice_valid:
            section_name = search_section_by_index(username, int(needed_section_index))
            section_content = open_section(username, section_name)
            print('\n ~~~DO YOU WANT TO DELETE A NOTE, OPEN AN EXISTING NOTE, REMOVE A NOTE FROM THIS SECTION?~~~\n', '=>> ENTER [1] TO OPEN AN EXISTING NOTE' ,'=>> ENTER [2] TO REMOVE A NOTE FROM THIS SECTION', '=>> ENTER [3] TO DELETE A NOTE', sep='\n')
            is_choice_valid = False
            while is_choice_valid is False:
                response = input("=>> ")
                try:
                    int(response)
                    if len(response) == 1:
                        if response in ['1', '2', '3']:
                            is_choice_valid = True
                    else:
                        is_choice_valid = False
                except ValueError:
                    print("Invalid Choice!\n")
                    is_choice_valid = False
            if response == '1':
                update_note_for_section(username, section_name, section_content)
            elif response == '2':
                remove_from_folder(username, section_name)
            else:
                delete_note_for_section(username, section_name)
           


def update_note_for_section(username, section_name, section_notes):
    notes = section_notes
    if notes != []:
        print(f'These is a list of the notes in {section_name}')
        x = 1
        for items in notes:
            if '.txt' in items:
                print(f"[{x}] {items.removesuffix('.txt')}")
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
                if int(needed_note_index) in choices:
                    is_choice_valid = True
                else:
                    is_choice_valid = False
            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False

        note_name = search_note_by_index_for_section(username, section_name, int(needed_note_index))
        note = open_note_for_section(username, section_name, note_name)
        try:
            previous_text = open(f"./user_shelfs/{username}/sections/{section_name}/{note_name}.txt", "r+").read()
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
                        sections(username)
                    if response == "n":
                        print("~NOTE DISCARDED~\n")
                        sections(username)
                    else:
                        is_note_saved = False
            else:
                note.write(f"{text}\n")
                note.write(f"{datetime.date.today()}\n")
                note.write(f"{datetime.datetime.now().strftime('%H:%M')}\n")
                note.write("\n")
                note.close()
                print("~NOTE SAVED~\n")
                sections(username)

        except FileNotFoundError:
            print("FILE NOT FOUND!")
            sections(username)
    else:
        print('~THIS SECTION IS EMPTY~')
        sections(username)






def open_section(username, section_name):
    section_content = os.listdir(f'./user_shelfs/{username}/sections/{section_name}')
    return section_content


def add_to_folder(username):
    notes = os.listdir(f"./user_shelfs/{username}")
    if notes != []:
        print('These is a list of the notes in your shelf')
        x = 1
        for items in notes:
            if '.txt' in items:
                print(f"[{x}] {items.removesuffix('.txt')}")
                x += 1
            elif len(notes) == 1 and '.txt' not in items:
                print('SORRY NO NOTE FOUND!')
                exit()
                
        print("*************************************************\n")

        is_choice_valid = False
        needed_note_index = ""
        choices = []
        while is_choice_valid is False:
            i = 0
            for items in notes:
                if items != 'sections':
                    choices.append(i)
                    print(f'ENTER [{i}] to move "{items.removesuffix(".txt")}"')
                    i += 1
            print("\n")
            needed_note_index = input("Which note do you want to move?>> ")
            try:
                int(needed_note_index)         
                if int(needed_note_index) in choices:
                    for items in notes:
                        if items == 'sections':
                            needed_note_index = int(needed_note_index) + 1
                    is_choice_valid = True
                else:
                    is_choice_valid = False
            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False

            if is_choice_valid:
                notename = search_note_by_index(username, int(needed_note_index))
                sections = os.listdir(f'./user_shelfs/{username}/sections')
                if sections != []:
                    print('These is a list of the sections in your shelf')
                    x = 1
                    for items in sections:
                        print(f"[{x}] {items.removesuffix('.txt')}")
                        x += 1
                    print("*************************************************\n")

                    is_choice_valid = False
                    needed_section_index = ""
                    choices = []
                    while is_choice_valid is False:
                        i = 0
                        for items in sections:
                            choices.append(i)
                            print(f'ENTER [{i}] to move to "{items}"')
                            i += 1
                        print("\n")
                        needed_section_index = input(f"Which section do you to move {notename} to?>> ")
                        try:
                            int(needed_section_index)
                            if int(needed_section_index) in choices:
                                is_choice_valid = True
                            else:
                                is_choice_valid = False
                        except ValueError:
                            print("Invalid Choice!\n")
                            is_choice_valid = False
                    if is_choice_valid:
                        section_name = search_section_by_index(username, int(needed_section_index)) 
                        root = f'./user_shelfs/{username}/{notename}.txt'
                        destination_folder = os.listdir(f'./user_shelfs/{username}/sections/{section_name}')
                        no_of_like_notes = 0
                        like_notes = []
                        for notes in destination_folder:
                            if notename in notes.removesuffix('.txt'):
                                like_notes.append(notes.removesuffix('.txt'))
                                no_of_like_notes += 1
                                
                        if no_of_like_notes > 0:
                            indices = []
                            for index,notes in enumerate(like_notes):
                                indices.append(index)
                           
                            new_index =int(indices[-1]) + 1
                            root = f'./user_shelfs/{username}/{notename}.txt'
                            destination = f'./user_shelfs/{username}/sections/{section_name}/{notename}{new_index}.txt'
                            shutil.move(root, destination)
                            print(f"\n'{notename}' has been moved to {section_name} as {notename}{new_index}")
                            sections(username)
                        
                        else:
                            destination = f'./user_shelfs/{username}/sections/{section_name}/{notename}.txt'
                            shutil.move(root, destination)                       
                            print(f"\n'{notename}' has been moved to {section_name}")
                            sections(username)
                            
    else:
        print('NO SECTION HAS BEEN CREATED')


def remove_from_folder(username, section_name):
    notes = os.listdir(f"./user_shelfs/{username}/sections/{section_name}")
    if notes != []:
        print('These is a list of the notes in this section')
        x = 1
        for items in notes:
            if '.txt' in items:
                print(f"[{x}] {items.removesuffix('.txt')}")
                x += 1
             
        print("*************************************************\n")
        is_choice_valid = False
        needed_note_index = ""
        choices = []
        while is_choice_valid is False:
            i = 0
            for items in notes:
                if items != 'sections':
                    choices.append(i)
                    print(f'ENTER [{i}] to remove "{items.removesuffix(".txt")}"')
                    i += 1
            print("NOTES WILL BE MOVED TO YOUR SHELF\n")
            needed_note_index = input("Which note do you want to remove?>> ")
            try:
                int(needed_note_index)         
                if int(needed_note_index) in choices:
                    for items in notes:
                        if items == 'sections':
                            needed_note_index = int(needed_note_index) + 1
                    is_choice_valid = True
                else:
                    is_choice_valid = False
            except ValueError:
                print("Invalid Choice!\n")
                is_choice_valid = False

            if is_choice_valid:
                notename = search_note_by_index_for_section(username, section_name, int(needed_note_index))
                root = f'./user_shelfs/{username}/sections/{section_name}/{notename}.txt'
                destination_folder = os.listdir(f'./user_shelfs/{username}')
                no_of_like_notes = 0
                like_notes = []
                for notes in destination_folder:
                    if notename in notes.removesuffix('.txt'):
                        like_notes.append(notes.removesuffix('.txt'))
                        no_of_like_notes += 1
                        
                if no_of_like_notes > 0:
                    indices = []
                    for index,notes in enumerate(like_notes):
                        indices.append(index)
                    new_index =int(indices[-1]) + 1
                    destination = f'./user_shelfs/{username}/{notename}{new_index}.txt'
                    shutil.move(root, destination)
                    print(f"\n'{notename}' has been removed from {section_name} and saved as {notename}{new_index} because a new note with the name '{notename}' already exist in your shelf ")
                    sections(username)
                
                else:
                    destination = f'./user_shelfs/{username}/{notename}.txt'
                    shutil.move(root, destination)                       
                    print(f"\n'{notename}' has been removed from {section_name} and moved to your shelf")
                    sections(username)
                    

    else:
        print('NO NOTES IN THIS SECTION')

                            
search_note_by_index('ti_oluwa', 1)