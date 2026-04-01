# Practicing with lists
import os

list1 = ["meow", "bro", "food"]

os.system("cls")

while True:
    menu = (
        input(
            "Do you want to (l)ist, (a)dd, (r)emove, (c)hange, (s)ort, or (e)xit? We also have (x)tra options.\n\t>> "
        )
        .strip()
        .lower()
    )

    ### List ###
    if menu == "l":
        # print(list1) <-- this prints the list in ugly brackets
        print(
            ", ".join(list1) + "\nYou have " + str(len(list1)) + " items in your list."
        )

    ### Add ###
    elif menu == "a":
        print("What would you like to add to the list?")
        list_add = input(">> ")
        if len(list1) > 1:
            add_where = input(
                "Would you like to add it to the (b)egginning, (m)iddle, or (e)nd?\n\t>> "
            )
            if add_where == "b":
                list1.insert(0, list_add)
            elif add_where == "m":
                list_middle = int(len(list1) / 2)
                list1.insert(list_middle, list_add)
            elif add_where == "e":
                list1.append(list_add)
            else:
                print("\nThat's not a valid option.\n")
        else:
            list1.append(list_add)

    ### Remove ###
    elif menu == "r":
        print("What would you like to remove from the list?")
        print("\t" + ", ".join(list1))
        list_remove = input(">> ")
        if list_remove in list1:
            # list1.remove(list_remove) <-- also works...
            list_removed = list1.pop(list1.index(list_remove))  # practice using .pop()
            print("Removed the following item: " + list_removed)
        elif list_remove not in list1:
            print("Lucky you! That's already not in the list.")

    ### Change ###
    elif menu == "c":
        print("What item would you like to change")
        print("\t" + str(list1))
        list_change_from = input(">> ")
        if list_change_from in list1:
            list_change_from_index = list1.index(list_change_from)
            print("What would you like to change " + list_change_from + " to?")
            list_change_to = input(">> ")
            list1.insert(list_change_from_index, str(list_change_to).strip())
            list1.remove(list_change_from.strip())
            print(
                str(list_change_from)
                + " has been changed to "
                + str(list_change_to)
                + "!"
            )
        elif list_change_from not in list1:
            print(
                "That is not in the list! \n Here are the items in the list: "
                + ", ".join(list1)
            )

    ### Sort ###
    elif menu == "s":
        if len(list1) == 0:
            print("List is empty!")
        elif len(list1) == 1:
            print("The list only has 1 item. Cannot sort.")
        elif len(list1) > 1:
            sort_choice = (
                input(
                    "Do you want to sort (a)lphabetically or (r)everse alphabetically?"
                )
                .strip()
                .lower()
            )
            if sort_choice == "a":
                list1.sort(key=str.lower)
                print("Sorted alphabetically!\n\tSorted List: " + ", ".join(list1))
            elif sort_choice == "r":
                list1.sort(key=str.lower, reverse=True)
                print(
                    "Sorted reverse-alphabetically!\n\tSorted list: " + ", ".join(list1)
                )
            else:
                print("That's not 'a' or 'r'")

    ##### xtra shit ######

    ### number each item (for loop practice...)
    elif menu == "x":
        print("\nExtra shit: (n)umber each list item or (r)eturn to previous menu.")
        x_menu = input("\n\t>> ")
        if x_menu == "n":
            for item in list1:
                print(item + " - #" + str(list1.index(item)))
        elif x_menu == "r":
            print("Returning!\n\n")
        else:
            print("That's not a valid option. Returning anyway.")

    ## Exit ###
    elif menu == "e":
        os.system("cls")
        break

    else:
        print("That's not a valid option.")
