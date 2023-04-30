

def askForAnotherRound():
    while True:
        decision = input("Wanna play again? (y/n)")
        if decision == 'y':
            return True
        if decision == 'n':
            return False
        else:
            print("Please answer with 'y' or 'n'. ")
