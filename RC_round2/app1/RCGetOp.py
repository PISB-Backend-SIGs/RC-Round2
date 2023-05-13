def getOp(id,userInput):
    if (int(id) ==1):
        return get_1(userInput)

def get_1(userInput):
    a =userInput[::-1]
    print(a)
    return a