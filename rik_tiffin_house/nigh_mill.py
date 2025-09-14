# file: night_mill_menu.py
from datetime import datetime

# get current time
current_time = datetime.now()

# only allow orders between 6PM and 8PM
if 18 <= current_time.hour < 20:
    print("✅ Night meal time is OPEN\n")

    # available curry choices
    choice = {"chicken curry": 35, "eggs curry": 15}

    print("Available curry choices:")
    for i, (food, price) in enumerate(choice.items()):
        print(f"{i}. {food} - {price} Rs")

    choice2 = int(input("Enter your choice (0-1): "))

    if 0 <= choice2 < len(choice):
        food_name = list(choice.keys())[choice2]
        food_price = choice[food_name]
        print("You selected:", food_name, "-", food_price, "Rs")
    else:
        print("❌ Invalid choice")
        food_name = None
        food_price = 0

    # base menu
    show_menu = ["roti", "dal"]

    # prices
    roti_price_per_piece = 5
    dal_price = 10

    # roti count
    need_rooti = int(input("Enter how many roti you need: "))
    total_roti_price = roti_price_per_piece * need_rooti

    # total price
    total_price = total_roti_price + dal_price + food_price

    # bill
    print("\nToday's Night Meal:")
    for item in show_menu:
        print("-", item)
    print("-", food_name)

    print("\nBill details:")
    print(f"Roti ({need_rooti} x {roti_price_per_piece}) = {total_roti_price} Rs")
    print(f"Dal = {dal_price} Rs")
    print(f"{food_name} = {food_price} Rs")
    print("Total =", total_price, "Rs")

else:
    print("⛔ Sorry, night meal is CLOSED. Available only between 6PM–8PM.")
