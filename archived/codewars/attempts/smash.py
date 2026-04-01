words = ['hello', 'world', 'this', 'is', 'great']

def smash(words):
    sentence = ""
    for word in words:
        sentence += " " + str(word) 
    return str(sentence).rstrip().lstrip()