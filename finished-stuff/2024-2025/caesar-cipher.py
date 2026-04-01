# Success! Basic Caesar from scratch.

alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
shift = 3


def caesar(message):
    encrypted_message = ""
    for char in message:
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index + shift) % len(alphabet)
            # encrypted_message.append(alphabet[new_index]) <-- non-string variant
            encrypted_message += alphabet[new_index]
        else:
            encrypted_message += char
    return encrypted_message


while True:
    print("What message do you want encrypted?")
    message = input("Message: ")
    encrypted_message_print = caesar(message)
    print(f"Caesar-ified! --> {encrypted_message_print}")
    print(alphabet[0])

    while True:
        another = (
            input("Do you want another message to be encrypted? (y/n)").strip().lower()
        )
        if another == "n":
            break
        elif another != "y":
            print("That's not y/n!")
        else:
            break

    if another == "n":
        break
