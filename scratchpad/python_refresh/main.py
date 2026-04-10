# This is my refresher file to get back some of the muscle memory for Python.
# I'm going to annotate some stuff to reflect comparisons with C++

# I'm going to go through the "Learn Python in Y Minutes" file to refresh
# Please note that some explanations here may be from that file, I'll annotate
# them with LPYM

# Variables -- python manages objects itself, every variable is like a 
#   smart pointer, python handles reference counting
# We can use type hinting for variables and function return type

# Lists are like std::vector, .append() is like push_back
ports = [22, 80, 443]
first_port = ports[0]
ports.append(8080)

# Dictionaries are like std::unordered_map
service = {"port": 80, "protocol": "HTTP"}

'''
    Some functions with type hinting
'''
def add_one(number: int) -> int:
    return number + 1

# Use f-strings instead of concatenation
def greet(name: str) -> str:
    # DON'T do: return "Hello, " + name
    return f"Hello, {name}!"

# Note the list[int] type hints
def audit_ports(ports: list[int]) -> tuple[list[int], list[int]]:
    system_ports = []
    user_ports = []
    
    '''
    for port in ports:
        if port < 1024:
            system_ports.append(port)
        else:
            user_ports.append(port)
    '''
    
    # list comprehension is the preferred and idiomatic way
    # it is also "optimized at the bytecode level and is faster than .append() loops"
    system_ports = [p for p in ports if p < 1024]
    user_ports = [p for p in ports if p >= 1024]
    
    # can return multiple values as a tuple!
    return system_ports, user_ports

# ----- Functions ----- #
def add(x, y):
    print("x is {} and y is {}".format(x, y))
    return x + y  # Return values with a return statement
    
# You can define functions that take a variable number of
# positional arguments
def varargs(*args):
    return args # returns a tuple
    
# You can define functions that take a variable number of
# keyword arguments, as well
def keyword_args(**kwargs):
    return kwargs # returns a dictionary
    
def add_nums(*args: int) -> int:
    ''' C++-ism way
    result = 0
    for i in args:
        result += i
    return result
    '''
    return sum(args)
    
# You can do both at once, if you like
def all_the_args(*args, **kwargs):
    print(args)
    print(kwargs)

def main():
    name_str: str = "refresher folder python learner"
    print(greet(name_str))
    
    num: int = 6
    print(add_one(num))
    
    print(f"Port: {service["port"]} / Protocol: {service["protocol"]}")
    
    open_ports = [22, 80, 443, 8080, 31227]
    target_name: str = "Localhost"
    if 80 in open_ports:
        print(f"Warning! {target_name} has HTTP port open!")
    
    # Tuple unpacking here
    sys, usr = audit_ports(open_ports)
    print(f"Open system ports: {sys}\nOpen user ports: {usr}")
        
    # In Python, try to use for each iterator every time 
    for port in open_ports:
        print(f"{port} is open")
        
    # You can iterate through index but it's frowned upon
    for index, port in enumerate(open_ports):
        print(f"{index + 1}. {port} is open")
        
    # Slicing in python is easy, its built into the square brackets
    # list[start:stop:step]
    data = [1, 2, 3, 4, 5, 6]
    first_two = data[:2]
    the_rest = data[2:]
    reversed = data[::-1]
    
    # We can mix data types in lists unlike std::vector
    mixed_data = [1, 2, "apple", 6, "seven"]
    three_and_on = mixed_data[1:]
    every_other = mixed_data[::2]
    
    print(f"{every_other}")
    
    # Tuples are like fixed-size std::array (or POD-style structs) and they're immutable
    # being immutable makes them faster (simple hash)
    andy_tup = ("Andy", 35, "Oregon")
    print(andy_tup)
    
    # if can be used as an expression, like ?:
    print(f"{andy_tup[1]} is 35") if 35 == 35 else print("Something went wrong")
    print(f"{andy_tup[0]} lives in {andy_tup[-1]}") # [-1] for last element
    
    andy_list = ["Andy", 35, "Oregon"]
    print(f"{andy_list[0]} lives in {andy_list[-1]}")
    # del removes
    del andy_list[-1] # you'd use .pop() but just demonstrating here
    print(f"{andy_list[0]} lives in {andy_list[-1]}")
    andy_list.remove(35) # removes first instance of 35
    print(f"{andy_list[0]} lives in {andy_list[-1]}") # Andy lives in Andy
    andy_list.append(35)
    andy_list.insert(2, "Oregon")
    print(f"{andy_list[0]} lives in {andy_list[-1]}")
    print(f"\"Oregon\"\'s index is {andy_list.index("Oregon")}")
    
    # Tuple unpacking
    name, age, location = andy_tup
    print(f"{name} is {age} years old and lives in {location}")
    
    # Extended tuple unpacking
    a, *b, c = (1, 2, 3, 4) # b is now [2, 3]
    # we can easily swap values like this
    a, c = c, a
    print(f"{a}, {b}, {c}") # 4, [2, 3], 1
    # If we wanted to get just the first and last and throw  away the rest... 
    a, *_, c = (0.01, 24, 5234, 123, 54, 234, 234, 53252, 12432433234234, 0.02)
    print(f"{a} is first, {c} is last")
    
    # Dictionary stuff
    empty_dict = {}
    filled_dict = {"one": 1, "two": 2, "three": 3}
    # Note keys for dictionaries have to be immutable types. This is to ensure that
    # the key can be converted to a constant hash value for quick look-ups.
    # Immutable types include ints, floats, strings, tuples. (LPYM)
    valid_dict = {(1,2,3):[1,2,3]}
    # ^^ Here the key is the tuple (1, 2, 3) -- it would be like:
    # std::map<std::tuple<int, int, int>, std::vector<int>> valid_map;
    
    # We can get all keys/values as an iterable with keys() and we can get a list of them
    # like so:
    print(f"The keys in filled_dict are: {list(filled_dict.keys())}\n\
The values are: {list(filled_dict.values())}")
    # we can use get() method to avoid KeyError
    filled_dict.get("four") # this returns "None"
    # the get method supports a default argument when the value is missing (LPYM)
    filled_dict.get("four", 4)
    print(f"{filled_dict}")
    filled_dict.setdefault("four", 4)
    print(f"{filled_dict}")
    filled_dict.setdefault("four", 5) # Won't add/overwrite existing
    print(f"{filled_dict}")
    # And then the other operations... normal stuff
    filled_dict["five"] = 5
    del filled_dict["one"]
    filled_dict.update({"six": 6})
    print(f"{filled_dict}")
    # Use comprehension to delete even values
    filled_dict = {key: value for key, value in filled_dict.items() if value %2 != 0}
    print(f"{filled_dict}")
    
    # Sets
    empty_set = set()
    some_set = {1, 2, 2, 3, 3, 3, 4, 4, 4, 4} # some_set is now {1, 2, 3, 4}
    # elements of a set have to be immutable
    filled_set = some_set
    # sets do NOT have duplicate elements
    filled_set.add(5)
    other_set = {3, 4, 5, 6, 7}
    # set operations = intersection, union, difference, symmetric difference
    print(f"some and other sets share members: {some_set & other_set}")
    print(f"some set contains members other set does not: {some_set - other_set}")
    print(f"other set contains members some set does not: {other_set - some_set}")
    print(f"taken together, the members of the sets are: {some_set | other_set}")
    print(f"the symmetric difference of some set to other set is: {some_set ^ other_set}")
    print(f"is 1, 2 a superset of 1, 2, 3? { {1, 2} >= {1, 2, 3} }")
    print(f"is 1, 2 a subset of 1, 2, 3? { {1, 2} <= {1, 2, 3} }")
    
    # Container information:
    '''
    List is like std::vector, it is ordered, mutable, allows duplicates, and is O(n)
    Tuple is like std::tuple, it is ordered, immutable, allows duplicates, and is O(n)
    Dictionary is like std::unordered_map, it is ordered, mutable, unique keys, and is O(1)
    Set is like std::unordered_set, it is unordered, mutable, unique elements, and is O(1)
    ---------
    List: Use for a sequence of items where the order matters and you may need 
    to change the values or the size (e.g., a message queue, a list of filenames to process).
    
    Tuple: Use for fixed records or "struct-like" data. Because they are immutable, 
    they are safer for data integrity and can be used as dictionary keys 
    (e.g., a coordinate (x, y)).
    
    Dictionary: Use when you have a logical mapping between a unique identifier 
    and a value (e.g., a database cache, a configuration object).
    
    Set: Use for uniqueness and high-speed membership checking.
    '''
    
    # You can cast to set to find unique values in a collection (idiomatic and very fast)
    raw_data = [1, 5, 2, 3, 6, 3, 4, 7, 8, 9, 1, 3, 4, 8, 7, 3, 5, 1, 8, 4, 67]
    unique_data = list(set(raw_data))
    print(f"{raw_data} has these unique elements: {unique_data}")
    
    
    # ----- Control Flow and Iterables ----- #
    # I'm gonna skip some stuff I'm familiar with so this is NOT an exhaustive overview
    
    command: str = "run"
    match command:
        case "run":
            print("Running")
        case "stop":
            print("Stopping")
        case code if command.isdigit(): # conditional!
            print(f"A digit was entered: {code}")
        case _: # _ is a wildcard like in Rust (like default/else)
            print("Invalid command")
            
    # range(lower, upper, step) - open/closed (won't print 8) - step isn't necessary, defaults to 1
    for i in range(4, 8, 2):
        print(i)
        
    # Handle eceptions with a try/except block
    try:
        # use 'raise' to raise an error
        raise IndexError("This is an index error")
    except IndexError as e:
        pass
    except (TypeError, NameError): # multiple exceptions can be processed jointly
        pass
    else: # optional, runs only if the code in try raises no exceptions
        print("All good!")
    finally: # executes under all circumstances
        print("Clean up resources etc here")
        
    # Handling files
    with open("file1.txt") as file:
        for line in file:
            print(line)
    
    contents = {"first_new": "First new line!", "second_new": "Second new line!"}
    with open("file1.txt", "w") as file:
        file.write(str(contents))
        
    with open("file1.txt", "r") as file:
        contents = file.read()
    print(f"contents: {contents}")
    
    # Iterables
    filled_dict = {"one": 1, "two": 2, "three": 3}
    our_iterable = filled_dict.keys()
    print(our_iterable)
    for i in our_iterable:
        print(i)
    our_iterator = iter(our_iterable) # can create an iterator
    # our iterator is an object that can remember the state as we traverse through
    next(our_iterator) # "one"
    next(our_iterator) # "two"
    object = next(our_iterator) # "three"
    print(object) # prints "three"
    
    # ----- Functions ----- #
    # you can call functions with keywork arguments in any order
    eleven: int = add(y = 6, x = 5) 
    print(eleven)
    
    varargs(1, 2, 3)
    keyword_args(first=1, second=2)
    all_the_args(1, 2, a=3, b=4)
    
    print(f"123 + 123 = {add_nums(123, 123)}")
    print(f"456 + 123 + 234 = {add_nums(456, 123, 234)}")
    
    # lambdas!
    (lambda x, y: x ** 2 + y ** 2)(2, 1)  # result 5
    
    
if __name__ == "__main__":
    main()