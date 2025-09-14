from datetime import datetime
from datetime import date
name = input("Enter the name of the person: ")


class Person:
  def __init__(self,name,age):
        self.name = name
        self.age = age
        print(f"the name is {self.name} and age is {self.age}")
class Duty:
    def dutyStary(self):
        print("duty is on")
    def dutyEnd(self):
        print("duty is off other vish pey fine")
    def break_time(self):
        print("break time")
    def second_end(self):
        print("second shift")
    

class job:
    def programer(self):
        print("write code and problem solver")
    def manager(self):
        print("manage the team")
    def designer(self):
        print("design the ui")  
    def tester(self):
        print("test the ui")
    def writer(self):
        print("write the documentation")

man ={"Rik" :22,"Joy":23,"Rohit":24,"Anuj":22,"astha":22}

current_date = date.today()
current_time = datetime.now()


if name in man:
    print(f"the age is {man[name]}")
else:
    print("the name is not in the list")

job = job()
Duty = Duty()
def time():
    if current_time.hour >= 9 and current_time.hour < 12:
      Duty.dutyStary()
    elif current_time.hour >= 12 and current_time.hour < 12.30:
      Duty.break_time()
    elif current_time.hour >= 12.30 and current_time.hour < 17:
      Duty.second_end()
    elif current_time.hour >= 17 and current_time.hour < 9:
      Duty.dutyEnd()
    else:
      print("the time is not in the range") 

if name == "Rik":
    job.manager()
    time()
elif name == "Joy":
      job.designer()
      time()
elif name == "Rohit":
      job.programer()
      time()
elif name == "Anuj":
      job.tester()
      time()
elif name == "astha":
      job.writer()
      time()