from google import genai

class DetectMood:
    def __init__(self, user_message):
        self.mood = self.detect_mood(user_message)

    def detect_mood(self, text: str):
        text = text.lower()
        
        positive_words = ["happy", "great", "good", "awesome", "fantastic", "excited", "positive"]
        negative_words = ["sad", "unhappy", "bad", "down","mood off","stress", "depressed", "tired", "angry"]
        hungry_words = ["hungry", "khide", "food", "eat", "khana", "thirsty"]
        bored_words = ["bored", "play", "game", "khelte"]
        greetings = ["hello", "hi", "hey"]
        details = ["how are you", "what's up", "how's it going"]
        who_are_you = ["create","make","who are you", "what's your name", "about you","creator","who made you","who is your creator","inventor","inventor of you","inventing you","who is your inventor" ,"inventing","creating","maker","creating"]
        goodbye = ["bye", "goodbye", "see you"]
        job = ["what can you do", "your job", "your purpose", "your role","job"]

 
        if any(w in text for w in negative_words):
            return "negative"
        if any(w in text for w in positive_words):
            return "positive"
        if any(w in text for w in hungry_words):
            return "hungry"
        if any(w in text for w in bored_words):
            return "bored"
        if any(w in text for w in greetings):
          return "greeting"
        if any(w in text for w in details):
            return "details"
        if any(w in text for w in who_are_you):
            return "who_are_you"
        if any(w in text for w in goodbye):
            return "goodbye"
        if any(w in text for w in job):
            return "job"
        if " " in text :
            bot_reply = "tempurarily is off."
        return "neutral"



import random
class GenerateReply:
  @staticmethod
  def generate_reply(mood: str):

    replies = {
        "positive": [
            {
                "main": "That's awesome! I can feel your positive energy from here!",
                "secondary": "What made today so special for you?"
            },
            {
                "main": "Love that! Keep shining like this!",
                "secondary": "Tell me what boosted your mood?"
            },
            {
                "main": "Great vibes! You sound really happy right now.",
                "secondary": "Wanna share the good news?"
            }
        ],
        "job": [
            {
                "main": "I'm here to assist you with any questions or tasks you might have.",
                "secondary": "I can help with answering questions, providing information, and offering support."
            },
            {
                "main": "My purpose is to be your helpful assistant.",
                "secondary": "Feel free to ask me anything or let me know how I can assist you!"
            },
            {
                "main": "I’m designed to support you in various ways.",
                "secondary": "Whether you need information, advice, or just someone to chat with, I’m here for you!"
            }
        ],
        "negative": [
            {
                "main": "I'm here for you. It’s okay to have tough moments.",
                "secondary": "Try taking a slow breath. Want to talk about it?"
            },
            {
                "main": "Sounds like you're having a rough time.",
                "secondary": "Even a 5-minute walk can help reset your brain."
            },
            {
                "main": "I'm sorry you feel this way.",
                "secondary": "Do something small that comforts you."
            }
        ],

        "hungry": [
            {
                "main": "Food alert! You definitely need to eat something.",
                "secondary": "Even a small snack helps your brain refuel."
            },
            {
                "main": "Your stomach is calling for help!",
                "secondary": "Go grab something — anything. Don’t ignore hunger."
            }
        ],

        "bored": [
            {
                "main": "Sounds like you need a change of pace.",
                "secondary": "Try standing up, stretching, or doing a fun mini-activity."
            },
            {
                "main": "Boredom detected. Time to switch things up!",
                "secondary": "What do you feel like doing right now?"
            }
        ],

        "greeting": [
            {
                "main": "Hey! Good to see you.",
                "secondary": "How are you feeling today?"
            },
            {
                "main": "Hi there!",
                "secondary": "Tell me what's happening in your world."
            }
        ],

        "neutral": [
            {
                "main": "I’m listening. Tell me more.",
                "secondary": "Feel free to express whatever’s on your mind."
            },
            {
                "main": "Got it. I’m here with you.",
                "secondary": "Want to explain a bit more?"
            }
        ]
        ,
        "details": [
            {
                "main": "You're doing great! Keep up the positive energy.",
                "secondary": "What's on your mind right now?"
            },
            {
                "main": "You sound really active. Keep it up!",
                "secondary": "Share something you're doing that's helping you."
            },
            {
                "main": "I'm glad to hear that you're feeling good!",
                "secondary": "What activities are making you feel this way?"
            }
        ],
        "who_are_you": [
            {
                "main": "I am Hanabi AI, your personal assistant. Created by Rik Singha.",
                "secondary": "I'm here to help you with any questions or tasks you need.https://riksingha001.github.io/rik-portfolio/"
            },
            {
                "main": "I'm Hanabi AI, your friendly AI assistant.",
                "secondary": "If you want to know more about RIK, visit https://riksingha001.github.io/rik-portfolio/"
            },
            {
                "main": "You can call me Hanabi AI. I'm here to support you.",
                "secondary": "If you have any questions, feel free to ask.visit https://riksingha001.github.io/rik-portfolio/"
            },
            {
                "main": "I am Hanabi AI, your virtual assistant created by Rik Singha.",
                "secondary": "If you need anything else, just let me know."
            },
                ],
        "goodbye": [
            {
                "main": "Goodbye! Take care.",
                "secondary": "If you need anything else, just let me know."
            },
            {
                "main": "See you later! Have a great day.",
                "secondary": "If you have any questions, feel free to ask."
            }
        ]
    }

    return random.choice(replies[mood]) if mood in replies else random.choice(replies["neutral"])
  

