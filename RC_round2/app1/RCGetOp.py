def getOp(id,userInput):
    if (int(id) ==1):
        print("1st question")
        return get_1(userInput)

def get_1(userInput):
    a =userInput[::-1]
    print(a)
    return a