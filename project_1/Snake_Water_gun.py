import random
computer=random.choice([1,-1,0])# but there is already declair in computer variable
# computer=random.randint(1,-1,0) #error because randint needs to argument 1 to 5 = 1,2,3,4,5 
you = int(input("Enter 1 for Snake, -1 for Water and 0 for Gun: "))
youDecision = {1: "Snake", -1: "Water", 0: "Gun"}
younum=youDecision[you]
print("You chose",younum)
computerDecision = {1: "Snake", -1: "Water", 0: "Gun"}
computernum=computerDecision[computer]
print("Computer chose",computernum)
if(you==computer):
    print("It's a Tie")
elif((you==1 and computer==-1) or (you==0 and computer==-1) or (you==1 and computer==0)):
    print("You Win")
else:
    print("You Lose")
# computer=random.choice([1,-1,0]) # it will choose any one value from the list
# computer=random.randint(1,3) # it will choose any one value from 1 to 3
