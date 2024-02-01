import datetime
def chatBot(query: str):
    answer = ""
    code = -1
    hour = int(datetime.datetime.now().hour)
    if hour <= 4 or hour >= 17:
        greeting = 'good evening '
    elif hour < 12:
        greeting = 'good morning Have a nice day '
        code = 1
    else:
        greeting = 'good afternoon '
    greeting += "the time is " + datetime.datetime.now().strftime("%I:%M")
    if "good morning" in query:
        answer = greeting
    if "good evening" in query:
        answer = greeting
    if "good afternoon" in query:
        answer = greeting
    if "good night" in query:
        answer = greeting
    if "hello" in query.split() or "hi" in query.split() or "hai" in query.split():
        answer = "Hello How may I help you"
    if "how are you" in query or "how you" in query:
        answer = "I am fine thanks"
    if "what are you doing" in query or "what you doing" in query:
        answer = "I am talking to you and improving every day"
    if ("who" in query.split() and "you" in query.split()) or ("what are you" in query.split()):
        answer = "Hello I am Jarvis a voice assistant created by master Sparsh"
    if "what" in query.split() and "can" in query.split() and "you" in query.split():
        answer = "Sir there are many things that I can do which include defining any word, repeating what you said, how to do anything and et cetera"
    if "happy" in query.split():
        answer = "Great I too am happy"
    if "bored" in query.split():
        answer = "Would you like to play a game"
        code = 2
    if "i love you" in query.lower():
        answer = "I love you too but as a friend"
    if "what have you learnt" in query:
        answer = "I have learnt to answer you"
    if "what else can you" in query:
        answer = "I can try to help you with everything I can"
    if "can" in query.split() and "you" in query.split() and "sing" in query.split():
        answer = "Oh would love to but haven't learnt that till now"
    if "what" in query.split() and "up" in query.split():
        answer = "Nothing much preparing to become efficient"
    if "i" in query.lower().split() and "angry" in query.split():
        answer = "Oh sir I can help you with that. May I"
        code = 3
    if "who created you" in query.lower() or "who made you" in query.lower():
        answer = "Master Sparsh"
    if "your name" in query:
        answer = "I am Jarvis"
    if "slept only for 5 minutes" in query:
        answer = "Yes I know the feeling sir"
        code = 5
    if "bye" in query.lower().split() or "shut up" in query.lower() or "stop" in query.lower().split() or "sleep" in query.lower().split():
        answer = "Bye Sir. See you Soon"
        code = 0
    if "5 minutes more" in query.lower():
        answer = "Sir please wake up it's a bright sunny day outside and you have to do a lot of work"
    return answer, code
