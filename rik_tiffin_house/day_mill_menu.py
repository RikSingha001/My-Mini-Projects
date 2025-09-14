# file name day_mill _menu
from datetime import datetime, date

# base meal and price
day_mil = ["rice", "dal", "1st tarka", "2nd tarka", "shak", "mithi chatni"]
day_mil_price = 50

# class
class Menu:
    def __init__(self, special_item):
        self.day_mil = day_mil + [special_item]

    def show_menu(self):
        print("\nToday's Menu:")
        for item in self.day_mil:
            print("-", item)

choice = {"fish fry": 25, "chicken curry": 35, "eggs curry": 15, "fish curry": 25}

current_time = datetime.now()
if 9 <= current_time.hour < 11:
    print("✅ Day meal time is OPEN\n")
    
    print("Available special items:")
    for i, (food, price) in enumerate(choice.items()):
        print(f"{i}. {food} - {price} Rs")

    choice2 = int(input("Enter your choice (0-3): "))
    if 0 <= choice2 < len(choice):
        food_name = list(choice.keys())[choice2]
        food_price = choice[food_name]
        print("You selected:", food_name, "-", food_price, "Rs")

        today_menu = Menu(food_name)
        today_menu.show_menu()

        total_price = day_mil_price + food_price
        print("\nTotal price:", total_price, "Rs")
    else:
        print("❌ Invalid choice")

else:
    print("⛔ Sorry, day meal is CLOSED. Available only between 9AM–11AM.")
