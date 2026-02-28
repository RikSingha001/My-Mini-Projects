# # file: hanabi/main_work.py
# import speech_recognition as sr
# import webbrowser
# import pyttsx3
# import music_lybery
# import requests
# from sambanova import SambaNova
# news = "33d2e07b85154ea59c04d7f5fff08f68"
# recognizer = sr.Recognizer()
# #this is recognizer object to recognize the speech

# def speak(text):
#     engine = pyttsx3.init()
#     engine.say(text)
#     engine.runAndWait()
#     engine.stop()
#     #this is speak function to speak the text

# def aiProses(comand):
#     client = SambaNova(api_key="d25f20f2-8af1-4f78-986c-599c521d8bac")
#     completion = client.chat.completions.create(
#         model="Llama-4-Maverick-17B-128E-Instruct",
#         messages=[
#             {"role": "system", "content": "You are a virtual assistant named Jervis. skilled in general task like alexa and google assistant."},
#             {"role": "user", "content": comand}
#         ]
#     )
#     return completion.choices[0].message.content
# def processed_command(c):
#     if "open youtube" in c.lower():
#         speak("Opening YouTube")
#         webbrowser.open("https://www.youtube.com")
#     elif "open google" in c.lower():
#         speak("Opening Google")
#         webbrowser.open("https://www.google.com")
#     elif "open stack overflow" in c.lower():
#         speak("Opening Stack Overflow")
#         webbrowser.open("https://www.stackoverflow.com")
#     elif "open facebook" in c.lower():
#         speak("Opening Facebook")
#         webbrowser.open("https://www.facebook.com")
#     elif "open whatsapp" in c.lower():
#         speak("Opening WhatsApp")
#         webbrowser.open("https://www.whatsapp.com/")
#     elif c.lower().startswith("play"):
#         song = c.lower().split(" ",1)[1]
#         link= music_lybery.music[song]
#         webbrowser.open(link)
#         speak(f"Playing {song}")
#     elif "news" in c.lower():
#         r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=33d2e07b85154ea59c04d7f5fff08f68")
#         if r.status_code == 200:
#             news_data = r.json()
#             articles = news_data.get('articles', [])  # Get top 5 news articles
#             for article in articles:
#                 speak(article['title'])
        
    
#     elif "exit" in c.lower() or "quit" in c.lower():
#         speak("Goodbye!")
#         exit()
#     else:
#         output = aiProses(c)
#         print("AI Response:", output)
#         speak(output)

# if __name__ == "__main__":
#     speak("Hello! Say 'Hanabi' to wake me up.")
#     while True:
#         r = sr.Recognizer()
#         print("recognizing...")
#         try:
#             with sr.Microphone() as source:
#                 print("Listening...")
#                 audio = r.listen(source, timeout=4, phrase_time_limit=4)

#             word = r.recognize_google(audio)
#             print(f"You said: {word}")

#             if word.lower() == "hanabi":
#                 speak("Yes sir")

#                 # Listening for further commands
#                 with sr.Microphone() as source:#this function is used to take input from microphone
#                     print("Hanabi active... waiting for command")
#                     audio = r.listen(source, timeout=5, phrase_time_limit=5)
#                 command = r.recognize_google(audio)
#                 print(f"Command: {command}")
#                 processed_command(command)

#         except Exception as e:
#             print("Error:", str(e))








