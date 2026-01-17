from datetime import datetime

DAYS_ITEMS = {
    "Veg thali with Rice": 55,
    "Chicken Curry": 50,
    "Egg": 20,
    "Fish Fry": 40,
    "Rice": 25,
}

NIGHT_ITEMS = {
    "Dal": 10,
    "Chicken Curry": 50,
    "Roti": 5,
    "Egg": 20,
    "Rice": 25,
}

class MenuManager:
    def __init__(self):
        current_hour = datetime.now().hour

        if 9 <= current_hour < 11:
            self.choices = DAYS_ITEMS
            self.meal_type = "lunch"
            self.status = "OPEN (Day Menu)"
        elif 17 <= current_hour < 19:
            self.choices = NIGHT_ITEMS
            self.meal_type = "dinner"
            self.status = "OPEN (Night Menu)"
        else:
            self.choices = {}
            self.meal_type = "closed"
            self.status = "CLOSED"

# class NIGHT_ITEMS :
#     night_item = {
#     "Dal": 10,
#     "Chicken Curry": 50,
#     "Egg": 20,
#     "Rice": 25
# }
# class DAYS_ITEMS:
#     day_item ={
#     "Vej": 55,
#     "Chicken Curry": 50,
#     "Egg": 20,
#     "Fish Fry": 40,
#     "Rice": 25,
#     }