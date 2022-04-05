from tkinter import *
import wolframalpha
import pyjokes
import subprocess
import time
import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import sys
sys.path.append('/usr/local/lib/python3.7/dist-packages/')

root = Tk()
w = Label(root, text='Welcome back User!')
w.pack()

root.title('Assistancy - your favourite personal assistant')
ourMessage = 'Tool and Techniques Lab, Group - 3'
messageVar = Message(root, text=ourMessage, width=300)
messageVar.config(bg='lightgreen')
messageVar.pack()

# ScrollBar
scrollbar = Scrollbar(root)
scrollbar.pack(side=RIGHT, fill=Y)

# ListBox
mylist = Listbox(root, height=20, width=40, yscrollcommand=scrollbar.set)

mylist.pack(fill=BOTH)
scrollbar.config(command=mylist.yview)
root.geometry('700x500')
root.minsize(700, 500)


# -----------------------------------------Main code begins------------------------------------
engine = pyttsx3.init()  # Microsoft Speech API

engine.setProperty('rate', 160)    # Speed percent (can go over 100)
engine.setProperty('volume', 0.9)  # Volume 0-1
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine.setProperty('voice', en_voice_id)

wolframe_appId = 'TR9UJW-AA3RR4ATQT'
wolframe_client = wolframalpha.Client(wolframe_appId)

# Mailids as key and value pairs
mailIds = {
    "Aryan": "1905815@kiit.ac.in",
    "Anirban": "1905816@kiit.ac.in",
    "Udit": "1905817@kiit.ac.in",
    "Prateek": "1905814@kiit.ac.in"
}

def speak(audio):
    mylist.insert(END, "Assistancy" + " : " + audio)
    root.update()
    print("Assistancy" + " : " + audio)
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour < 17:
        speak("Good Afternoon")
    else:
        speak("Good Evening")

    speak("I am your assistancy. How can i help you?")


def takeCommand():
    while(True):

        r = sr.Recognizer()

        with sr.Microphone() as source:

            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source, phrase_time_limit=5)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            mylist.insert(END, "User said : " + query)
            root.update()
            print(f"User said: {query}\n")
            return query

        except Exception as e:
            print(e)
            print("Unable to Recognize your voice. Please say again.")


def date():
    now = datetime.datetime.now()
    my_date = datetime.datetime.today()

    month_name = now.month
    day_name = now.day
    month_names = ['January', 'February', 'March', 'April', 'May', 'June',
                   'July', 'August', 'September', 'October', 'November', 'December']
    ordinalnames = ['1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th', '14th', '15th',
                    '16th', '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24rd', '25th', '26th', '27th', '28th', '29th', '30th', '31st']

    speak("Today is " + month_names[month_name-1] +
          " " + ordinalnames[day_name-1] + '.')


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(text)

    subprocess.Popen(["notepad.exe", file_name])


def main_function():
    query = takeCommand().lower()

    # Logic for executing task
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace('wikipedia', "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(results)

    elif 'open youtube' in query:
        speak("Opening Youtube...")
        webbrowser.open('http://www.youtube.com')

    elif 'open google' in query:
        speak("Opening google...")
        webbrowser.open('http://www.google.com')

    elif 'open gmail' in query:
        speak("Opening Gmail...")
        webbrowser.open('https://mail.google.com/mail/u/0/?tab=rm&ogbl#inbox')

    elif 'open amazon' in query:
        speak("Opening amazon...")
        webbrowser.open('http://www.amazon.in')

    elif 'joke' in query:
        speak(pyjokes.get_joke())

    elif 'open flipkart' in query:
        speak("Opening flipkart...")
        webbrowser.open('http://www.flipkart.com')

    elif 'open prime video' in query:
        speak("Opening Prime Video...")
        webbrowser.open('http://www.primevideo.com')

    elif 'open netflix' in query:
        speak("Opening Netflix")
        webbrowser.open_new_tab("http://www.netflix.com/browse")

    elif 'play music' in query or 'play some song' in query:
        print("Playing trending songs YouTube...")
        webbrowser.open(
            'https://www.youtube.com/watch?v=2qzcHLyv3N0&list=PLw-VjHDlEOgvWPpRBs9FRGgJcKpDimTqf&index=2')

    elif 'bye bye' in query or 'goodbye' in query  or 'exit' in query:
        speak(f"Goodbye. Have a nice day!")
        quit()

    elif 'the time' in query:
        strTime = datetime.datetime.now().strftime('%H:%M:%S')
        speak(f"The time is {strTime}")

    elif "today's date" in query:
        date()

    elif 'news' in query:
        news = webbrowser.open_new_tab(
            "https://timesofindia.indiatimes.com/city/mangalore")
        speak('Here are some headlines from the Times of India, Happy reading')
        time.sleep(6)

    elif 'cricket' in query:
        news = webbrowser.open_new_tab("https://www.cricbuzz.com")
        speak('This is live news from cricbuzz')
        time.sleep(6)

    elif 'corona' in query:
        news = webbrowser.open_new_tab(
            "https://www.worldometers.info/coronavirus/")
        speak('Here are the latest covid-19 numbers')
        time.sleep(6)

    elif 'make a note' in query:
        speak("What to keep note?")
        text = takeCommand()
        note(text)

    elif 'open code' in query:
        speak("Opening Visual studio code...")
        codePath = "C:\\Users\\UDIT\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)

    elif 'open chrome' in query:
        speak("Opening chrome...")
        codePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(codePath)

    elif 'open zoom' in query:
        speak("Opening Zoom...")
        codePath = "C:\\Users\\UDIT\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"
        os.startfile(codePath)

    elif 'open office' in query or 'open word' in query or 'open powerpoint' in query or 'open excel' in query:
        speak("Opening Office")
        codePath = "C:\\Users\\UDIT\\AppData\\Local\\Kingsoft\\WPS Office\\ksolaunch.exe"
        os.startfile(codePath)

    elif 'open telegram' in query:
        speak("Opening Telegram...")
        codePath = "C:\\Users\\UDIT\\AppData\\Roaming\\Telegram Desktop\\Telegram.exe"
        os.startfile(codePath)

    elif 'send email' in query:
        try:
            speak("to Whom you want to send email?")
            to = takeCommand()
            speak("What should be the content?")
            content = takeCommand()

            server = smtplib.SMTP('smtp.gmail.com', 587)
            # server.connect("smtp.example.com",465)
            server.ehlo()
            server.starttls()
            server.login('<user-name>', '<pass-word>')

            server.sendmail('<user-name>', mailIds[to], content)

            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry, I was unable to send the email at the moment. Please try again")

    else:
        res = wolframe_client.query(query)
        answer = next(res.results).text
        speak(answer)

wishMe()

frame = Frame(root)
frame.pack()
greenbutton = Button(frame, text='SPEAK', fg='green', command=main_function)
greenbutton.pack(side=LEFT)
redbutton = Button(frame, text='STOP', fg='red', command=root.destroy)
redbutton.pack(side=LEFT)

root.mainloop()