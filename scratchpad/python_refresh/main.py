# This is my refresher file to get back some of the muscle memory for Python.
# I'm going to annotate some stuff to re-orient my 1.25 year of focus on C++
# to Python.

# Variables -- python manages objects itself, every variable is like a 
#   smart pointer, python handles reference counting
# We can use type hinting for variables and function return type

# Lists are like std::vector, .append() is like push_back
ports = [22, 80, 443]
first_port = ports[0]
ports.append(8080)

# Dictionaries are like std::unordered_map
service = {"port": 80, "protocol": "HTTP"}

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
    
    # Tuples are like fixed-size std::array (or POD-style structs) but they're immutable
    andy = ("Andy", 35, "Oregon")
    print(andy)
    

if __name__ == "__main__":
    main()
