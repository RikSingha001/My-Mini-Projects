# number= int(input("enter the number: "))


# upload= int(input("enter the number: "))

# if upload > number:
#     print("upload is greater than number")

# else:
#     print("upload is less than number")
# for i in range(upload, number+1):
#     print(f"Playing song {i} time(s)")

# from playsound import playsound

# number = int(input("Enter how many times to play the song: "))

# for i in range(1, number + 1):
#     print(f"Playing song {i} time(s)")
#     playsound("song.mp3")

import pygame
import time

pygame.mixer.init()

number = int(input("Enter how many times to play the song: "))

for i in range(1, number + 1):
    print(f"Playing song {i} time(s)")
    pygame.mixer.music.load("C:/Users/loade/Downloads/Besabriyaan - M.S. Dhoni - The Untold Story 128 Kbps.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():   
        time.sleep(1)
