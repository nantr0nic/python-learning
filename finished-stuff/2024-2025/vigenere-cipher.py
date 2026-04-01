# Vigenere from scratch. Fuck.
import os

alphabet = '0a1b2c3d4e5f6g7h8i9j!k@l#m$n"%/ ^o&p*q(r)s-t_u+v=w.x,y?zABCD:EFGHIJK;LMNOPQRSTUVWXYZ'
key = ""

os.system("cls")


# Cipher function
def vigenere(message, key, direction=1):
    result = ""
    key_index = 0
    for char in message:
        if char in alphabet:
            key_char = key[key_index % len(key)]
            key_index += 1
            msg_index = alphabet.index(char)
            key_index2 = alphabet.index(key_char)
            new_index = (msg_index + key_index2 * direction) % len(alphabet)
            result += alphabet[new_index]
        elif char not in alphabet:
            result += char
    return result


# Encrypt/decrypt (write) to file
# this feature might run into some weird loops...
def filewrite(choice):
    while True:
        writechoice = input("Do you want to write this to file? (y/n) ").strip().lower()
        if writechoice == "y":
            if choice == "e":
                with open("encrypted.txt", "w") as file:
                    file.write(vigenere(message, key, direction=1))
                    print("Written to encrypted.txt!\n")
                break
            elif choice == "d":
                with open("decrypted.txt", "w") as file:
                    file.write(vigenere(message, key, direction=-1))
                    print("Written to decrypted.txt!\n")
                break
        elif writechoice == "n":
            break
        else:
            print("That's not y/n!")
            break
    return


# Encrypt/decrypt (read) from a file
def fileread(choice):
    while True:
        if choice == "e":
            with open("decrypted.txt", "r") as file:
                message = file.read()
                key = input("Input a key (Don't forget it!): ")
                print(
                    "Encrypted message: " + vigenere(message, key, direction=1) + "\n"
                )
            break
        elif choice == "d":
            with open("encrypted.txt", "r") as file:
                message = file.read()
                key = input("What was the key for this message? --> ")
                print(
                    "Decrypted message: " + vigenere(message, key, direction=-1) + "\n"
                )
            break
    return


# Choose from file or not
def fromfile(readchoice):
    while True:
        if readchoice == "y":
            fileread(choice)
            break
        elif readchoice == "n":
            break
        else:
            break
    return


# Interface script
while True:
    choice = input("Do you wish to encrypt, decrypt, or quit? (e/d/q) ").strip().lower()
    while True:
        if choice == "e":
            readchoice = input("From file or no? (y/n) --> ").strip().lower()
            if readchoice == "y":
                fileread(choice)
                break
            elif readchoice == "n":
                message = input("Enter a message: ")
                key = input("Input a key (Don't forget it!): ")
                print(
                    "Encrypted message: " + vigenere(message, key, direction=1) + "\n"
                )
                filewrite(choice)
                break
        elif choice == "d":
            readchoice = input("From file or no? (y/n) --> ").strip().lower()
            if readchoice == "y":
                fileread(choice)
                break
            elif readchoice == "n":
                message = input("Enter a message: ")
                key = input("Input a key: ")
                print(
                    "Decrypted message: " + vigenere(message, key, direction=-1) + "\n"
                )
                filewrite(choice)
                break
        elif choice == "q":
            print("Farewell!\n\n")
            break
        else:
            print("That's not e or d or q!")
            break
    if choice == "q":
        break
