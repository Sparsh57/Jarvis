#importing the libraries
import datetime
import multiprocessing
import os
import pandas as pd
import platform
import random
import smtplib
import time
import webbrowser
import subprocess
from itertools import permutations
from threading import Timer
import keyboard
import psutil
import pyautogui
import pyttsx3
import speech_recognition as sr
from pywikihow import search_wikihow
import re
import requests
import playsound
import music_recommender
from chatbot import chatBot
import datefinder
import json
from urllib.request import urlopen
import pyperclip
from englisttohindi.englisttohindi import EngtoHindi
from gtts import gTTS
from pynput.keyboard import Key, Controller
from Weather import greeting
from Instagram_and_facebook import instagram, facebook
import sounddevice as sd
import wavio
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


code = -1
running = True
master = "Sparsh"
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
process = []
contact = pd.read_csv('contacts.csv', sep='|')
name=list(contact['Name'])
number = list(contact['Number'])
email = list(contact['Email'])
contacts = {}
for i in range(len(name)):
    contacts[name[i]] = [number[i], email[i]]
contacts = pd.read_csv('contacts.csv')

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()


def speak_hindi(text):
    obj = gTTS(text, lang='hi', slow=False)
    obj.save("Hindi.mp3")
    playsound.playsound("Hindi.mp3")


def control(text):
    if len(process) > 0:
        process.clear()
    process.append(multiprocessing.Process(target=speak, args=(text,)))
    for pr in process:
        pr.start()
        take_command_speaking()


def take_command_speaking():
    r = sr.Recognizer()
    task_calling = 0
    query = ""
    for i in range(2000):
        with sr.Microphone(device_index=0) as source:
            print("Listening...")
            audio = r.listen(source)
        # noinspection PyBroadException
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(query)
        except Exception:
            query = ""
        process_break = 0
        for pr in process:
            process_break = 0
            if not pr.is_alive():
                process_break = 1
        if process_break == 1:
            break
        if "jarvis" in query.lower():
            for pr in process:
                pr.kill()
            process.clear()
            task_calling = 1
            break
    if task_calling == 1:
        TaskExecution(query)


def say(query):
    try:
        query = query[query.index("say"):]
        query = query.replace("say", "", 1)
    except:
        try:
            query = query[query.index("speak"):]
            query = query.replace("speak", "", 1)
        except:
            query = query[query.index("repeat"):]
            query = query.replace("repeat", "", 1)
    query = query.rstrip().lstrip()
    if query == "":
        speak("What do you want me to say")
        query = takecommand()
    speak(query)
    print(query)


def typing(query):
    query = query[query.index("type"):]
    query = query.replace("type", "", 1)
    query = query.rstrip().lstrip()
    if query == "":
        speak("What do you want me to type")
        query = takecommand()
    time.sleep(4)
    print(query)
    keyboard.write(query)
    speak('typed')


def wish():
    hour = int(datetime.datetime.now().hour)
    if hour <= 4 or hour >= 19:
        speak('Good Evening ' + master)
    elif hour < 12:
        speak('Good morning ' + master)
    else:
        speak('Good afternoon' + master)


def meaning(query):
    try:
        query = query.lower()[query.lower().index("jarvis")]
    except:
        pass
    query = query.lower().split()
    for i, j in enumerate(query):
        if j == "meaning":
            query[i] = ""
        if j == "mean":
            query[i] = ""
        if j == "means":
            query[i] = ""
        if j == "define":
            query[i] = ""
        if j == "definition":
            query[i] = ""
        if j == "of":
            query[i] = ""
        if j == "off":
            query[i] = ""
        if j == "what":
            query[i] = ""
        if j == "does":
            query[i] = ""
    query = " ".join(query)
    if len(query.split()) > 4:
        number_of_words = 4
    else:
        number_of_words = len(query.split())
    iterations = 0
    got_the_definition = False
    for i in range(number_of_words, 0, -1):
        if len(query.split()) > 5:
            list_of_words = list(permutations(query.split()[-5:], i))
        else:
            list_of_words = list(permutations(query.split(), i))
        if i == 1:
            list_of_words = list(permutations(query.split()[::-1], 1))
        while not got_the_definition and iterations < len(list_of_words):
            string = " ".join(list_of_words[iterations])
            response = requests.get("https://api.dictionaryapi.dev/api/v2/entries/en_US/" + string).text
            if "definition\":" in response:
                definition_index = response.index("definition\":") + len("definition\":\"")
                index_till_last_word = response[definition_index:].index(".\"") + definition_index
                print(str(list_of_words[iterations]).replace(",", "").replace("(", "").replace(")", "").replace("'",
                                                                                                                "") + " is defined as " + response[
                                                                                                                                          definition_index:index_till_last_word])
                speak(str(list_of_words[iterations]).replace(",", "") + "is defined as " + response[
                                                                                           definition_index:index_till_last_word])
                got_the_definition = True
            iterations += 1
        iterations = 0
    if not got_the_definition:
        speak("Sorry can't help you with that")


def how_to(query):
    try:
        query = query[query.index("how to "):]
    except:
        query = query[query.index("how do "):]
    try:
        max_results = 1
        how_tos = search_wikihow(query, max_results)
        assert len(how_tos) == 1
        how_tos[0].print()
        speak(how_tos[0].summary)
    except Exception:
        pass


def search(query):
    query = query[query.index("search"):]
    query = query.replace("search", "", 1)
    query = query.rstrip().lstrip()
    if query == "":
        speak("What do you want me to search")
        query = takecommand()
    speak("searching " + query)
    webbrowser.open("https://www.google.com/search?q=" + query)


def read_magazine():
    webbrowser.open_new("https://www.scientificamerican.com/")
    webbrowser.open_new("https://www.smithsonianmag.com/")
    webbrowser.open_new("https://www.theatlantic.com/world/")
    webbrowser.open_new("https://hbr.org/")
    webbrowser.open_new("https://www.technologyreview.com/")
    webbrowser.open_new("https://www.nationalgeographic.com/")
    webbrowser.open_new("https://www.newyorker.com/")
    webbrowser.open_new("https://time.com/")
    webbrowser.open_new("https://www.newsweek.com/")
    webbrowser.open_new("https://www.wired.com/")
    webbrowser.open_new("https://www.aaas.org/")
    webbrowser.open_new("https://timesofindia.indiatimes.com/blogs/toi-editorials/")


def music(query):
    query = query.replace("play", "")
    query = query.replace("hit", "")
    query = query.rstrip().lstrip()
    if query == "":
        pyautogui.hotkey('playpause')
    else:
        answer_code = 4
        music_recommender.main(query.lower())


def chrome_main_automation(query):
    value = if_program_is_running()
    if  value== "RIW":
        subprocess.run(['chrome.exe'])
        if "incognito" in query.lower():
            speak("Opening Incognito")
            pyautogui.hotkey('ctrl', 'shift', 'n')
        elif "new window" in query.lower():
            speak("Opening a new Window")
            pyautogui.hotkey('ctrl', 'n')
        elif "tab" in query.lower().split():
            if "previous" in query.lower().split():
                speak("Opening the previous tab")
                pyautogui.hotkey('ctrl', 'shift', 'tab')
            elif "next" in query.lower().split():
                pyautogui.hotkey('ctrl', 'tab')
            elif "switch" in query.lower():
                speak("Switching tab")
                random_switch = random.randint(1, 4)
                if random_switch == 1:
                    pyautogui.hotkey('ctrl', 'tab')
                if random_switch == 2:
                    pyautogui.hotkey('ctrl', 'shift', 'tab')
                if random_switch == 3 or random_switch == 4:
                    random_number = random.randint(1, 5)
                    pyautogui.hotkey('ctrl', str(random_number))
            elif "close" in query.lower().split():
                speak("Closing this tab")
                pyautogui.hotkey('ctrl', 'w')
            elif "new" in query.lower().split():
                speak("Opening a new tab")
                pyautogui.hotkey('ctrl', 't')
        elif "close window" in query.lower():
            speak("Closing this window")
            pyautogui.hotkey('ctrl', 'shift', 'w')
    elif value == "RIM":
        subprocess.run(['open', '-a', "Google Chrome"])
        if "incognito" in query.lower():
            speak("Opening Incognito")
            pyautogui.hotkey('command', 'shift', 'n', interval=0.1)
        elif "new window" in query.lower():
            speak("Opening a new Window")
            pyautogui.hotkey('command', 'n', interval=0.1)
        elif "tab" in query.lower().split():
            if "previous" in query.lower().split():
                speak("Opening the previous tab")
                pyautogui.hotkey('command', 'shift', 'tab', interval=0.1)
            elif "next" in query.lower().split():
                pyautogui.hotkey('command', 'tab', interval=0.1)
            elif "switch" in query.lower():
                speak("Switching tab")
                random_switch = random.randint(1, 4)
                if random_switch == 1:
                    pyautogui.hotkey('command', 'tab', interval=0.1)
                if random_switch == 2:
                    pyautogui.hotkey('command', 'shift', 'tab', interval=0.1)
                if random_switch == 3 or random_switch == 4:
                    random_number = random.randint(1, 5)
                    pyautogui.hotkey('command', str(random_number), interval=0.1)
            elif "close" in query.lower().split():
                speak("Closing this tab")
                pyautogui.hotkey('command', 'w', interval=0.1)
            elif "new" in query.lower().split():
                speak("Opening a new tab")
                pyautogui.hotkey('command', 't', interval=0.1)
        elif "close window" in query.lower():
            speak("Closing this window")
            pyautogui.hotkey('command', 'shift', 'w', interval=0.1)
    elif value == "OS":
        speak("Application is neither windows nor Mac Sorry sir can't help you with this")
    else:
        speak("Sorry can't help you with it")


def if_program_is_running():
    if platform.system() == "Windows":
        return "RIW"
    elif platform.system() == "Darwin":
        return "RIM"
    else:
        return "OS"


def whatsapp(query):
    query = query.split()
    counter_variable = 0
    for q in query:
        if q.lower() in contacts:
            contact = contacts[q][0]
            counter_variable = 1
            break
    if counter_variable == 0:
        speak("Sir whom to WhatsApp")
        query = takecommand()
        query = query.split()
        for q in query:
            if q.lower() in contacts:
                contact = contacts[q][0]
                counter_variable = 1
                break
        if counter_variable == 0:
            speak("Sir please type the number to whom you want to whatsapp starting with the country code:")
            contact = input("Sir please type the number to whom you want to whatsapp starting with the country code:")
    whatsapp_link = "https://api.whatsapp.com/send/?phone=" + contact
    speak("What do you want to message")
    message = takecommand()
    whatsapp_link += "&text=" + message
    webbrowser.open(whatsapp_link)
    time.sleep(23)
    pyautogui.press('enter')


def jokes():
    file = open("jokes", "r")
    content = file.readlines()
    joke = random.choice(content)
    file.close()
    speak(joke)
    print(joke)


def stories():
    file = open("stories", "r", errors='ignore')
    content = file.readlines()
    story = random.choice(content)
    file.close()
    speak(story)
    print(story)


def email(query):
    query = query.split()
    counter_variable = 0
    for q in query:
        if q.lower() in contacts:
            emails = contacts[q.lower()][1]
            counter_variable = 1
            break
    if counter_variable == 0:
        speak("Sir whom to Mail")
        query = takecommand()
        query = query.split()
        for q in query:
            if q.lower() in contacts:
                emails = contacts[q][1]
                counter_variable = 1
                break
        if counter_variable == 0:
            speak("Sir please type the email to whom you want to send an email: ")
            emails = input("Sir please type the email to whom you want to send an email: ")
    speak("What do you want to message")
    message = takecommand()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    try:
        server.ehlo()
        server.starttls()
        server.login("","")#Enter your email and password over here
        server.sendmail(emails, emails, message)
        server.close()
        speak("email sent")
    except:
        speak("There was some error in mailing so sorry sir")


def check_cpu_usage():
    usage = psutil.cpu_percent(1)
    print(usage)
    if not usage < 75:
        speak("ERROR! CPU is overloaded")
    else:
        speak("Everything is ok. CPU is not overloaded")


def calculator(query):
    k = query.split()
    s = 0
    c = 0
    extra = 0
    for i in k:
        try:
            if i == "x":
                s = s + (int(k[c - 1]) * int(k[c + 1]))
                extra += 1
            if i == "+":
                if extra == 0:
                    s += (int(k[c - 1]) + int(k[c + 1]))
                    extra += 1
                else:
                    s += int(k[c + 1])
            if i == "-":
                if extra == 0:
                    s += (int(k[c - 1]) - int(k[c + 1]))
                    extra += 1
                else:
                    s -= int(k[c + 1])
        except Exception:
            continue
        c += 1
    speak("The answer is " + str(s))


def timer(q=""):
    temp = re.findall(r'\d+', q)
    res = list(map(int, temp))
    q = q.lower().split()
    time_int = 0
    if res:
        if "hour" in q or "hours" in q:
            try:
                time_int += 3600 * int(q[q.index("hour") - 1])
            except:
                try:
                    time_int += 3600 * int(q[q.index("hours") - 1])
                except:
                    pass
        if "minute" in q or "minutes" in q:
            try:
                time_int += 60 * int(q[q.index("minute") - 1])
            except:
                try:
                    time_int += 60 * int(q[q.index("minutes") - 1])
                except:
                    pass
        if "second" in q or "seconds" in q:
            try:
                time_int += int(q[q.index("second") - 1])
            except:
                try:
                    time_int += int(q[q.index("seconds") - 1])
                except:
                    pass
    if time_int == 0:
        speak("For How long do you want to set the timer:")
        q = takecommand()
        q = q.lower().split()
        if "hour" in q or "hours" in q:
            try:
                time_int += 3600 * int(q[q.index("hour") - 1])
            except:
                try:
                    time_int += 3600 * int(q[q.index("hours") - 1])
                except:
                    pass
        if "minute" in q or "minutes" in q:
            try:
                time_int += 60 * int(q[q.index("minute") - 1])
            except:
                try:
                    time_int += 60 * int(q[q.index("minutes") - 1])
                except:
                    pass
        if "second" in q or "seconds" in q:
            try:
                time_int += int(q[q.index("second") - 1])
            except:
                try:
                    time_int += int(q[q.index("seconds") - 1])
                except:
                    pass
    if time_int != 0:
        k = convert(time_int)
        k = k.split(":")
        string_time = ""
        if k[0] != '0':
            if k[0] != '1':
                string_time += str(k[0]) + " hours "
            else:
                string_time += str(k[0]) + " hour "
        if k[1] != '00':
            if k[1] != '1':
                string_time += str(k[1]) + " minutes "
            else:
                string_time += str(k[1]) + " minute "
        if k[2] != '00':
            if k[2] != '1':
                string_time += str(k[2]) + " seconds "
            else:
                string_time += str(k[2]) + " second "
        return string_time, time_int


def convert(seconds):
    minimum, sec = divmod(seconds, 60)
    hour, minimum = divmod(minimum, 60)
    return "%d:%02d:%02d" % (hour, minimum, sec)


def alarm(query):
    date_finder = datefinder.find_dates(query)
    dates = ""
    for i in date_finder:
        dates = str(i.time())
        break
    if dates == "":
        speak(
            "Ok please type when's the alarm and use {} to seperate between hour and minutes and dont "
            "forget seconds".format(
                ":"))
        dates = input("Enter : ")
    set_time = time_to_num(dates)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_times = time_to_num(current_time)
    difference = float(set_time - current_times)
    if difference < 0:
        difference = 86400 + difference
    return difference


def wake_alarm(query):
    date_finder = datefinder.find_dates(query)
    dates = ""
    for i in date_finder:
        dates = str(i.time())
        break
    if dates == "":
        speak(
            "Ok please type when's the alarm and use {} to seperate between hour and minutes and dont "
            "forget seconds".format(
                ":"))
        dates = input("Enter : ")
    set_time = time_to_num(dates)
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_times = time_to_num(current_time)
    difference = float(set_time - current_times)
    if difference < 0:
        difference = 86400 + difference
    return difference


def time_to_num(time_str):
    hh, mm, ss = map(int, time_str.split(':'))
    return ss + 60 * (mm + 60 * hh)


def times():
    playsound.playsound("Alarm-ringtone.mp3")


def wake_up_times():
    playsound.playsound("Alarm-ringtone.mp3")
    speak("Good Morning Sir")
    speak(greeting)


def copy_clipboard():
    if if_program_is_running()=="RIW":
        pyautogui.hotkey('ctrl', 'c')
    # ctrl-c is usually very fast but your program may execute faster
    elif if_program_is_running()=="RIM":
        pyautogui.hotkey('command', 'c')
    time.sleep(2)
    return pyperclip.paste()


def TaskExecution(default=""):
    jarvis_on = 0
    if default == "":
        wish()
    while running:
        if not default == "":
            query = default
            default = ""
        else:
            query = str(takecommand())
        if jarvis_on == 1 or "jarvis" in query.lower():
            query = query.replace("jarvis", "")
            query = query.replace("Jarvis", "")
            query = query.rstrip().lstrip()
            if "say" in query.lower().split() or "speak" in query.lower().split() or "repeat" in query.lower():
                say(query)
            elif "define" in query.split() or "meaning" in query.split() or "mean" in query.split() or "definition" in query.split():
                meaning(query)
            elif "type" in query.lower().split():
                typing(query)
            elif "how to " in query or "how do " in query:
                how_to(query)
            elif "search" in query.lower().split():
                search(query)
            elif "wake up" in query.lower():
                jarvis_on = 1
                speak("Online and ready sir")
            elif "date" in query.lower().split():
                speak(datetime.datetime.now().strftime("%d/%m/%Y"))
            elif "magazine" in query.lower().split() and "read" in query.lower().split():
                read_magazine()
            elif "play" in query.lower().split() or "hit" in query.lower().split():
                print(query)
                music(query)
            elif "pause" in query.lower().split():
                pyautogui.hotkey('playpause')
            elif "tab" in query.lower().split() or "window" in query.lower().split() or "incognito" in query.lower().split():
                chrome_main_automation(query)
            elif "stop" in query.lower().split() or "shut up" in query.lower() or "sleep" in query.lower().split():
                speak("Sure")
                engine.stop()
                jarvis_on = 0
            elif "joke" in query.lower().split():
                jokes()
            elif "story" in query.lower().split() or "stories" in query.lower().split() or "anecdote" in query.lower().split():
                stories()
            elif "whatsapp" in query.lower().split():
                whatsapp(query.lower())
            elif "email" in query.lower().split():
                email(query)
            elif "cpu usage" in query.lower():
                check_cpu_usage()
            elif "+" in query.lower() or "-" in query.lower() or "x" in query.lower():
                calculator(query)
            elif "instagram" in query.lower():
                speak("Checking Instagram")
                instagra = instagram()
                print(instagra)
                speak(instagra)
            elif "facebook" in query.lower():
                speak("Checking Facebook")
                faceb = facebook()
                print(faceb)
                speak(faceb)
                # sets a timer
            elif 'timer' in query.lower().split():
                time_set, time_timer = timer(query)
                timers = Timer(time_timer, times)
                speak("timer set for " + time_set)
                timers.start()
                continue
            # sets an alarm
            elif "alarm" in query.lower().split():
                difference = alarm(query)
                alarms = Timer(difference, times)
                speak("Alarm set")
                alarms.start()
                continue
            elif "get up" in query.lower():
                difference = alarm(query)
                alarms = Timer(difference, wake_up_times())
                speak("Alarm set")
                alarms.start()
                continue
            elif "stopwatch" in query.lower().split():
                from Stopwatch import App
                App()
                continue
            elif "website" in query.lower():
                speak(
                    "Say speak if you want to speak.   Say type if you want to type")
                k = takecommand()
                if k is not None:
                    if "speak" in k.casefold():
                        speak("Please say the name of website")
                        query = takecommand()
                        webbrowser.open("https://" + query)
                    elif "type" in k.casefold():
                        query = input(
                            "Enter the name of the website: ")
                        webbrowser.open(query)
                    else:
                        speak("Next time say speak or type")
            elif "time" in query.lower().split():
                str_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"{master} the time is {str_time}")
                print(f"{master} the time is {str_time}")
            elif "open code" in query:
                if if_program_is_running()=="RIW":
                    os.system("code")
                elif if_program_is_running()=="RIM":
                    subprocess.run(['open', '-a', "Visual Studio Code"])
                speak("Opening Visual Studio Code sir")
            elif "open pycharm" in query:
                if if_program_is_running() == "RIW":
                    os.system("code")
                elif if_program_is_running() == "RIM":
                    subprocess.run(['open', '-a', "Pycharm"])
                speak("Opening Pycharm sir")
            elif "open notepad" in query.lower():
                if if_program_is_running()=="RIW":
                    subprocess.Popen('C:\\Windows\\System32\\notepad.exe')
                elif if_program_is_running()=="RIM":
                    subprocess.run(['open', '-a', "Notes"])
                speak("Opening Notepad sir")
            elif "weather" in query.lower() or 'temperature' in query.lower():
                date_object = datefinder.find_dates(query)
                k = datetime.datetime.now()
                for i in date_object:
                    k = i
                if k.date() != datetime.datetime.now().date():
                    from city_name_extractor import lat_long
                    city, lat, long = lat_long(query)
                    from Weather import weather_forecast
                    date_temp = weather_forecast(lat, long)
                    if k in date_temp['date'] and (lat != 0 or long != 0):
                        m = date_temp['date'].index(k)
                        speak(date_temp['temp'][m] + ' degree Celcius in ' + city + ' on ' + str(k.date()))
                        print(date_temp['temp'][m] + ' degree Celcius in ' + city + ' on ' + str(k.date()))
                    else:
                        if k in date_temp['date']:
                            city, lat, long = lat_long('Kolkata')
                            date_temp = weather_forecast(lat, long)
                            m = date_temp['date'].index(k)
                            speak(date_temp['temp'][m] + ' degree Celcius in Kolkata on ' + str(k.date()))
                        else:
                            speak('Sorry cant help you with that date')
                            continue
                elif 'tomorrow' in query.lower():
                    from city_name_extractor import lat_long
                    city, lat, long = lat_long(query.lower())
                    from Weather import weather_forecast
                    date_temp = weather_forecast(lat, long)
                    if lat != 0 or long != 0:
                        speak("Tomorrow it is " + date_temp['temp'][1] + ' degree Celcius in ' + city)
                    else:
                        city, lat, long = lat_long('Kolkata')
                        date_temp = weather_forecast(lat, long)
                        speak("Tomorrow it is " + date_temp['temp'][1] + ' degree Celcius in Kolkata')
                elif 'day after tomorrow' in query.lower():
                    from city_name_extractor import lat_long
                    city, lat, long = lat_long(query.lower())
                    print(city)
                    from Weather import weather_forecast
                    date_temp = weather_forecast(lat, long)
                    if lat != 0 or long != 0:
                        speak("Tomorrow it is " + date_temp['temp'][2] + ' degree Celcius in ' + city)
                    else:
                        city, lat, long = lat_long('Kolkata')
                        date_temp = weather_forecast(lat, long)
                        speak("Tomorrow it is " + date_temp['temp'][2] + ' degree Celcius in Kolkata')
                else:
                    from city_name_extractor import city
                    city_name = city(query.lower())
                    if city_name:
                        from Weather import main
                        speak(main(city_name))
                        print(main(city_name))
                    else:
                        from Weather import main
                        speak(main("Kolkata"))
                        print(main('Kolkata'))
            elif "news" in query.lower().split():
                try:
                    json_obj = urlopen(
                        'https://newsapi.org/v1/articles?source=the-times-of-india&sortBy=top&apiKey=5deda8ad0a3f44b6ae97b18949ddcc42')
                    data = json.load(json_obj)
                    i = 1
                    news = {}
                    speak('here are some top news from the times of india')
                    print(
                        '''=============== TIMES OF INDIA ============''' + '\n')

                    for item in data['articles']:
                        news[str(i) + '. ' + item['title']] = item['description']
                        i += 1
                    for item in news:
                        print(item + "\n")
                        print(news[item] + "\n")
                    speak(str(news))
                except Exception as e:
                    print(str(e))
            elif "save file" in query.lower():
                time.sleep(1)
                if if_program_is_running()=="RIW":
                    pyautogui.keyDown('ctrl')
                    pyautogui.press('s')
                    pyautogui.keyUp('ctrl')
                elif if_program_is_running()=="RIM":
                    pyautogui.keyDown('command')
                    pyautogui.press('s')
                    pyautogui.keyUp('ctrl')
            elif "where is" in query:
                query = query.replace("where is", "")
                location = query.replace("jarvis", "")
                speak("User asked to Locate")
                speak(location)
                webbrowser.open(
                    "https://www.google.nl/maps/place/" + location + "")
            elif "copy" in query.lower():
                if "line" in query.lower():
                    pyautogui.click(clicks=3, interval = 0.1)
                else:
                    pyautogui.click(clicks = 2, interval = 0.1)
                copy_clipboard()
                speak("copied")
            elif "paste" in query.lower():
                if if_program_is_running()=="RIW":
                    pyautogui.hotkey('ctrl', 'v')
                elif if_program_is_running()=="RIM":
                    pyautogui.hotkey('command', 'v', interval=0.05)
                speak("Pasted")
            elif "pound" in query.lower() or "lbs" in query.lower():
                query.replace("Jarvis", "")
                query.replace("jarvis", "")
                if "pound" in query.lower():
                    index_before_pounds = (query.lower()).index("pound")
                else:
                    index_before_pounds = (query.lower()).index("lbs")
                string_before_pounds = query[:index_before_pounds]
                digit = [int(i)
                         for i in string_before_pounds.split() if i.isdigit()]
                if "to kg" in query.lower() or "to kilogram" in query.lower() or "in kg" in query.lower() or "in kilogram" in query.lower():
                    pound_to_kg = digit[0] / 2.205
                    speak("{:.2f} kilograms".format(pound_to_kg))
                    print(pound_to_kg)
                if "to lbs" in query.lower() or "to pound" in query.lower() or "in lbs" in query.lower() or "in pound" in query.lower():
                    kilogram_to_lbs = digit[0] * 2.2046
                    speak("{:.2f} pounds".format(kilogram_to_lbs))
                    print(kilogram_to_lbs)
            elif "translate" in query.lower():
                speak("What do you want to translate")
                message = takecommand()

                # creating a EngtoHindi() object
                res = EngtoHindi(message)

                # displaying the translation
                print(res.convert)
                speak_hindi(res.convert)
            elif ("corona" in query.lower() or "covid" in query.lower()) and "in" in query.lower():
                from city_name_extractor import country
                country_name, country_code = country(query)
                from Covid_19 import covid_19
                speak(covid_19(country_name, country_code))
                print(covid_19(country_name, country_code))
            elif "volume" in query.lower():
                keyboards = Controller()
                if "up" in query.lower() or "increase" in query.lower():
                    for i in range(4):
                        keyboards.press(Key.media_volume_up)
                if "decrease" in query.lower() or "lower" in query.lower() or "down" in query.lower():
                    for i in range(4):
                        keyboards.press(Key.media_volume_down)
            elif "riddle" in query.lower().split():
                k = {"What has to be broken before you can use it?": "egg",
                     "What is full of holes but still holds water": "sponge",
                     "A man who was outside in the rain without an umbrella or hat didn’t get a single hair on "
                     "his head wet. Why": "bald",
                     "I have branches, but no fruit, trunk or leaves. What am I": "bank",
                     "What can’t talk but will reply when spoken to": "echo"}
                key = random.choice(list(k))
                c = 1
                f = 0
                while c != 4:
                    speak(key)
                    inp = takecommand()
                    if k[key] in inp.lower():
                        f = 1
                        break
                    else:
                        c += 1
                if f == 1:
                    speak("congratulations you did it")
                else:
                    speak("The answer is :" + k[key])
            else:
                answer, answer_code = chatBot(query)
                if answer == "" and jarvis_on != 1:
                    speak("Sorry sir can't help you with that.")
                    answer = ""
                print(answer)
                if answer_code == 0:
                    jarvis_on = 0
                    speak("Sure Bye")
                    engine.stop()
                if answer_code == 1:
                    answer_code = -1
                if answer_code == 5:
                    time.sleep(2)
                    speak("Sir You do realize that you have to get up")


def takecommand():
    fps = 44100
    apikey = ''#Enter Your Watson Api Key
    url = 'https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/3caf4eee-1061-4fcb-a7a2-cb5466f55140'
    authenticator = IAMAuthenticator(apikey)
    stt = SpeechToTextV1(authenticator=authenticator)
    stt.set_service_url(url)
    duration = 6

    print('Listening...')
    recording = sd.rec(duration * fps, samplerate=fps, channels=1)

    sd.wait()
    print("Recognizing...")

    wavio.write('output.wav', recording, fps, sampwidth=2)
    try:
        with open('output.wav', 'rb') as f:
            res = stt.recognize(audio=f, content_type='audio/wav', model='en-US_NarrowbandModel').get_result()
        text = res['results'][0]['alternatives'][0]['transcript']
        confidence = res['results'][0]['alternatives'][0]['confidence']
    except:
        text = ""
    print(text)
    try:
        os.remove("output.wav")
    except:
        pass
    return text


if __name__ == '__main__':
    TaskExecution()
