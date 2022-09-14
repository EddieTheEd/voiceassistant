
from ast import Break
from cProfile import label
from cgitb import text
import atexit
from fileinput import close
import subprocess
import wolframalpha
import pyttsx3
import sys
import tkinter as tk
from tkinter import PhotoImage, ttk
import json
import random
import operator
import speech_recognition as sr
from datetime import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
import openai
from clint.textui import progress
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
from PIL import ImageTk, Image


# Startup

global closebyvoice
closebyvoice = False


# clearing the terminal
clear = lambda: os.system('cls')
clear()

# getting the tts set up
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

#finding all account (data to be implemented)
accountdata = []
accountdatatemp = []
accounts = open("accountdata.txt", "r+")
for line in accounts:
    if "\n" in line:
        accountdatatemp.append(line[:-1])
    else:
        accountdatatemp.append(line)

for i in accountdatatemp:
    if "USER:" in i:
        temp = i.split()
        temp.remove(temp[0])
        username = ' '.join(temp)
        accountdata.append(username)
# accountdata is a list containing all usernames, soon to be made into dictionary

#this opens the logging text file
userdata = open('userdata.txt', 'a')

#function to both add lines to log file, and print
def log(message):
    date = str(datetime.now())
    userdata.write(date + "\n" + message + "\n\n")
    print(date + "\n" + message + "\n")

#small function for tts
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def takeCommand():
    mic = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        boxstatus("Listening...")
        mic.pause_threshold = 1
        audio = mic.listen(source)
  
    try:
        boxstatus('Program recognizing')
        query = mic.recognize_google(audio, language ='en-in')
        boxstatus(f"User said: {query}\n")
  
    except Exception as e: 
        boxstatus('Program failed to understand voice')
        return "None"
     
    return query

def boxstatus(input):
    window.label.destroy()
    window.imageLabel.destroy()
    
    img = tk.PhotoImage(file="./assets/voiceassistlogo.png")
    window.imageLabel = tk.Label(image = img)
    
    window.imageLabel.pack()

    window.label = ttk.Label(text = input)
    window.label.pack()
    window.update()
    log(input)

def confirmmanualusername():
    print(window.entry.get())
    if window.entry.get() == '':
        speak("Please try again.")
        manualtextbox()
    else:
        name = window.entry.get()
        window.imageLabel.destroy()
        window.entry.destroy()
        window.yesbutton.destroy()
        window.imageLabel = tk.Label(window, image = img)
        
        window.imageLabel.pack()

        window.label = ttk.Label(text = input)
        window.label.pack()

        boxstatus(f'Hello {name}!')
        speak("hello" + name + ", how are you today! i hope you are well")
        accounts.write("USER: " + name + "\n")
        a = True
        while a:
            main()

def manualtextbox():
    global window
    window.label.destroy()
    window.imageLabel.destroy()

    window.imageLabel = tk.Label(window, image = img)
    
    window.imageLabel.pack()

    window.iconbitmap('./assets/voiceassistlogo.ico')
    window.title("Ed's Voice Assistant!")
    window.geometry('320x130+5+5')

    window.entry = tk.Entry()
    window.entry.pack()
    window.yesbutton = ttk.Button(window, text="Confirm Username", command=confirmmanualusername)
    window.yesbutton.pack()
    window.attributes('-topmost', 1)
    window.update()


def intro():
    speak("what is your name")
    boxstatus('Voice Assistant Status: Listening')
    namecount = 0

    while namecount != 3:
        name = str(takeCommand())
        if name != 'None':
            namecount = 2
            boxstatus(f'Hello {name}!')
            speak("hello" + name + ", how are you today! i hope you are well")
            accounts.write("USER: " + name + "\n")
            a = True
            while a:
                main()
        else:
            boxstatus('Did not understand.')
            if namecount == 0:
                speak("well, i wasn't able to catch your name, could you repeat that?")
            elif namecount == 1:
                speak("weird, i didn't catch that again. please repeat what you said.")
            elif namecount == 2:
                namecount = 3
                log("User failed to register name using voice. Proceeding to text input.")
                speak("Your name must be quite special. Please type it in the box provided.")
                manualtextbox()
                break
               
            namecount += 1

    
            

def finduser(username):
    newdow.destroy()
    global name
    name = username
    maingui()
    boxstatus(f'Hello {name}!')
    speak("hello" + name + ", welcome back.")
    a = True
    while a:
        main()

def accountselection():
    window.destroy()
    global newdow
    newdow = tk.Tk()
    height = int(round(len(accountdata) * (150/6)))
    newdow.geometry(f'320x{height}+470+50')
    newdow.title("Available accounts: ")
    newdow.iconbitmap('./assets/voiceassistlogo.ico')
    for i in accountdata:
        newdow.button = ttk.Button(text = str(i))
        newdow.button['command'] = lambda i=i: finduser(i)
        newdow.button.pack()

def startup():
    boxstatus('Voice Assistant Status: Configuration')
    speak('processing, starting up')
    if not accountdata:
        speak('no previous users detected')
        log('no previous users detected')
        intro()
    elif len(accountdata) == 1:
        global name
        name = accountdata[0]
        log(f'username {name} detected')
        boxstatus(f"Hello {name}!")
        speak("hello" + name + ", welcome back.")
        a = True
        while a:
            main()
    else:
        speak('multiple users detected. please choose your account.')
        accountselection()
        

def main():
    speak("what would you like to do?")
    programUnderstood = False

    query = str(takeCommand()).split()
    if query != None:
        boxstatus(f"Analysing input: '{' '.join(query)}'")

    # base functions
    if 'obsidian' in query:
        speak("Understood, opening Obsidian")
        os.startfile("C:\\Users\\edwar\\AppData\\Local\\Obsidian\\Obsidian.exe")
        boxstatus("Success!")
        programUnderstood = True
    elif 'restart' in query:
        speak("restarting")
        os.execv(sys.executable, ['python'] + sys.argv)
        boxstatus("Success!")
        programUnderstood = True
    elif 'Firefox' in query:
        speak("Understood, opening firefox.")
        os.startfile("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
        boxstatus("Success!")
        programUnderstood = True
    elif 'close program' in ' '.join(query):
        speak("Understood, see you again soon.")
        log('Program terminated via voice command')
        global closebyvoice
        closebyvoice = True
        exit()
    elif 'create new account' in ' '.join(query):
        speak("all right. I'll forget your current account, and create a new one")
        log("Creating new account")
        intro()

    elif str(' '.join(query)) != "None":
    # putting it through openai
        speak("Well I couldn't understand that, let me put it through open a i.")
        openai.api_key = "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"

        response = openai.Completion.create(
        model="text-davinci-002",
        prompt=' '.join(query),
        temperature=0.3,
        max_tokens=150,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        echo = True
        )
        print(response)
        answer = response['choices'][0]['text']
        print(str(answer))
        speak(str(answer))
        if str(answer) != "None":
            programUnderstood = True


    if programUnderstood == False:
        boxstatus("Failed to understand command.")
        speak("Sorry. i didn't catch that.")

def maingui():
    global window
    window = tk.Tk()

    img = tk.PhotoImage(file="./assets/voiceassistlogo.png")
    window.imageLabel = tk.Label(image = img)
    
    window.imageLabel.pack()

    window.iconbitmap('./assets/voiceassistlogo.ico')
    window.title("Ed's Voice Assistant!")
    window.geometry('320x130+5+5')

    window.label = ttk.Label(window, text='processing...')
    window.label.pack()

    window.attributes('-topmost', 1)

    window.update()

def exitlog():
    global closebyvoice
    if closebyvoice == False:
        log('Program terminated via script ending.')
    userdata.close()



#initial_window creation, i.e maingui with intialization button
log('Program Initialised')
atexit.register(exitlog)

global window
window = tk.Tk()

#visual stuff
global img
img = tk.PhotoImage(file="./assets/voiceassistlogo.png")

window.imageLabel = tk.Label(window, image = img)
window.imageLabel.pack()

window.iconbitmap('./assets/voiceassistlogo.ico')

#core window code

window.title("Ed's Voice Assistant!")
window.text = tk.StringVar()
window.text.set("Press to start program!")
window.geometry('320x130+5+5')

window.label = ttk.Button(window, textvariable = window.text, command = startup)

window.label.pack()
window.attributes('-topmost', 1)
window.mainloop()

