# Not robustly tested but seems to work well
# Review at a future date to streamline / revise / narrow

import os
import string
import random

# Setting all options to 'on' and length to 12
letters = True
digits = True
punctuation = True
length = 12


# Password generator function
def genpass(length):
    options = [string.ascii_letters, string.digits, string.punctuation]
    if letters == False:
        options.remove(string.ascii_letters)
    if digits == False:
        options.remove(string.digits)
    if punctuation == False:
        options.remove(string.punctuation)
    elif letters == False and digits == False and punctuation == False:
        print("You must have at least 1 option enabled!")
        return
    generated = ""
    for i in range(0, length):
        generated += random.choice("+ ".join(options))
    print(f"Password: {generated}")
    return


# Checkbox function for main interface loop
def checkbox(text, checked):
    if checked:
        checked_str = "[X] {}".format(text)
    else:
        checked_str = "[ ] {}".format(text)
    return checked_str


# Main loop
while True:
    os.system("cls")
    print(" # # # # # # # # # # #\n--> Password Generator <--\n # # # # # # # # # # #")
    print("Choose password options.")
    print(checkbox("[L]etters", letters))
    print(checkbox("[D]igits", digits))
    print(checkbox("[P]unctuation", punctuation))
    print(f"Password L[e]ngth: {length}")
    print("Type G to [G]enerate or X to E[x]it!")

    choice = input(">> ").lower().strip()

    # Input loop
    while True:
        if choice == "l":
            letters = not letters
            break
        elif choice == "d":
            digits = not digits
            break
        elif choice == "p":
            punctuation = not punctuation
            break
        elif choice == "e":
            print("How many characters long do you want the password to be?")
            length = int(input(">> ").strip())
            break
        elif choice == "g":
            genpass(length)
            input("Press any key to continue!")
            break
        elif choice == "x":
            break
        else:
            print("Not a valid option.")
            break
    if choice == "x":
        break
