# Prime number finder -- finds prime numbers within user specific range


print("""\n\n
█ ▄▄  █▄▄▄▄ ▄█ █▀▄▀█ ▄███▄          ▄     ▄   █▀▄▀█ ███   ▄███▄   █▄▄▄▄ 
█   █ █  ▄▀ ██ █ █ █ █▀   ▀          █     █  █ █ █ █  █  █▀   ▀  █  ▄▀ 
█▀▀▀  █▀▀▌  ██ █ ▄ █ ██▄▄        ██   █ █   █ █ ▄ █ █ ▀ ▄ ██▄▄    █▀▀▌  
█     █  █  ▐█ █   █ █▄   ▄▀     █ █  █ █   █ █   █ █  ▄▀ █▄   ▄▀ █  █  
 █      █    ▐    █  ▀███▀       █  █ █ █▄ ▄█    █  ███   ▀███▀     █   
  ▀    ▀         ▀               █   ██  ▀▀▀    ▀                  ▀    
                                                                        
▄████  ▄█    ▄   ██▄   ▄███▄   █▄▄▄▄                                    
█▀   ▀ ██     █  █  █  █▀   ▀  █  ▄▀                                    
█▀▀    ██ ██   █ █   █ ██▄▄    █▀▀▌                                     
█      ▐█ █ █  █ █  █  █▄   ▄▀ █  █                                     
 █      ▐ █  █ █ ███▀  ▀███▀     █                                      
  ▀       █   ██                ▀                                       \n
""")

print("Pick the range you'd like to find prime numbers in.")
low = int(input("Minimum: "))
high = int(input("Maximum: "))
primes = []

# why +1? obviously required
for i in range(low, high):
    if all(i % j != 0 for j in range(2, int(i**0.5) + 1)):
        print(str(i) + " <-- prime number")
        primes.append(i)

print("Number of primes in specified range: " + str(len(primes)))
print("Sum of the primes in the specified range: " + str(sum(primes)))
