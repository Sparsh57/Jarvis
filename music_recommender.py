import difflib
import os
import random
import pyttsx3
import pywhatkit
import pandas as pd
import subprocess


engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)


def speak(text):
    engine.say(text)
    engine.runAndWait()


sheet = pd.read_excel('songs_list.xlsx', sheet_name="songs_list")
songs = sheet['Song Name']
artists = sheet['Artist']
file_name = sheet['File Name']

def edm():
    music_files = ['On My Way.mp3', 'Sing me to sleep.mp3', 'Wake Me Up.mp3', 'Titanium.mp3', '2U.mp3', 'without you.mp3', 'Let me love you.mp3', 'Taki taki.mp3', 'Ignite.mp3', 'lean on.mp3', 'Don_t let me down.mp3']
    playing_file = random.choice(music_files)
    file_path = str(os.path.join(os.getcwd(), "songs", playing_file))
    subprocess.call(['open', file_path])


def happy():
    music_files = ["never close your eyes.mp3","Bad Guy.mp3","Hymn For the weekend.mp3","Galway girl.mp3","Shape of you.mp3","Work from home.mp3","Despacito.mp3","Girls like you.mp3","Memories.mp3","Cheap Thrills.mp3"]
    playing_file = random.choice(music_files)
    file_path = str(os.path.join(os.getcwd(), "songs", "happy", playing_file))
    subprocess.call(['open', file_path])


def hip_hop():
    music_files = ["Mood.mp3","rockstar.mp3","God's Plan.mp3","laugh now cry later.mp3","Godzilla.mp3","Lose Yourself.mp3","Love The  way you lie.mp3","Lemonade.mp3","Blueberry faygo.mp3","old town road.mp3","What you know.mp3","rockstar.mp3"]
    playing_file = random.choice(music_files)
    file_path = str(os.path.join(os.getcwd(), "songs", "hip hop", playing_file))
    subprocess.call(['open', file_path])


def inspiration():
    music_files = ["Believer.mp3","Radioactive.mp3","Whatever it takes.mp3","ok not to be ok.mp3","Counting Stars.mp3","Treat you better.mp3","Unstoppable.mp3","Hall of fame.mp3"]
    playing_file = random.choice(music_files)
    file_path = str(os.path.join(os.getcwd(), "songs", "inspiration", playing_file))
    subprocess.call(['open', file_path])


def pop():
    music_files = ["Faded.mp3","This is what you came for.mp3","One Kiss.mp3","Attention.mp3","Rockabye.mp3","so far away.mp3","Closer.mp3","something just like this.mp3","See you again.mp3","Dusk  till dawn.mp3"]
    playing_file = random.choice(music_files)
    file_path = str(os.path.join(os.getcwd(), "songs", "pop", playing_file))
    subprocess.call(['open', file_path])


def slow():
    music_files = ["do I wanna know.mp3","Pompeii.mp3","My  heart will go on love theme.mp3","A thousand years.mp3","Fix You.mp3","Perfect.mp3","Thinking  out loud.mp3","Say you won't let go.mp3","i dont wanna live forever.mp3"]
    playing_file = random.choice(music_files)
    file_path = str(os.path.join(os.getcwd(), "songs", "slow", playing_file))
    subprocess.call(['open', file_path])


def normal_song(query):
    return_value = 0
    check_if_song = 0
    for count, song in enumerate(songs):
        if difflib.get_close_matches(song.lower(), [query.lower()], cutoff=0.7):
            check_if_song = 1
            speak("PLaying " + song)

            file_path = str(os.path.join(os.getcwd(), 'songs', file_name[count]))
            subprocess.call(['open', file_path])
            return_value = 1
            break
    if check_if_song == 0:
        try:
            query = query[query.index("by") + 2:]
        except:
            try:
                query = query[query.index("bye") + 3:]
            except:
                pass
        query = query.split("and")
        query = "".join(query)
        maximum = [0, "", ""]
        for count, artist in enumerate(artists):
            print(artist)
            artist = artist.split(',')
            count_of_artist = 0
            for musician in artist:
                musician = musician.lower().lstrip().rstrip()
                if difflib.get_close_matches(musician, [query.lower().lstrip().rstrip()], cutoff=0.8):
                    count_of_artist += 1
            if count_of_artist > maximum[0]:
                maximum[0] = count_of_artist
                maximum[1] = file_name[count]
                maximum[2] = artist
        file_path = str(os.path.join(os.getcwd(), "songs", maximum[1]))
        if maximum[1] != "":
            speak("Playing music by " + "and".join(maximum[2]))
            subprocess.call(['open', file_path])
            return_value = 1
        return return_value


def random_music():
    list_variable = []
    for file in os.listdir("songs"):
        if os.path.isfile(os.path.join("songs", file)):
            files = str(os.path.join(os.getcwd(), 'songs', file))
            list_variable.append(files)
    file_path = random.choice(list_variable)
    subprocess.call(['open', file_path])


def main(query):
    if "edm" in query or "electronic" in query or "dance" in query:
        edm()
    elif "happy" in query or "mood" in query or "good" in query:
        happy()
    elif "rap" in query or "hip hop" in query or "fast" in query or "hip-hop" in query:
        hip_hop()
    elif "inspir" in query or "motivat" in query or "focus" in query:
        inspiration()
    elif "pop" in query or "top" in query or "popular" in query:
        pop()
    elif "slow" in query or "romantic" in query or "sad" in query or "sleep" in query:
        slow()
    else:
        return_value = normal_song(query)
        if return_value == 0 and ("song" in query or "music" in query):
            random_music()
        elif return_value == 0:
            speak("Sir playing using Youtube")
            pywhatkit.playonyt(query)