
from cProfile import label
import subprocess
import wolframalpha
import pyttsx3
import sys
import tkinter as tk
from tkinter import ttk
import json
import random
import operator
import speech_recognition as sr
import datetime
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
from clint.textui import progress
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen
from PIL import ImageTk, Image


# Startup

clear = lambda: os.system('cls')
clear()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


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



def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
     
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
  
    try:
        print("Recognizing...")   
        query = r.recognize_google(audio, language ='en-in')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("Unable to Recognize your voice.") 
        return "None"
     
    return query

def boxstatus(input):
    window.label.destroy()
    window.label = tk.Label(text = input)
    window.label.pack()
    window.update()
    print(f"Textbox was changed to {input}")

def finduser(username):
    print(username)

def intro():
    speak("what is your name")
    boxstatus('Voice Assistant Status: Listening')
    name = str(takeCommand())
    if name != 'None':
        boxstatus(f'Hello {name}!')
        speak("hello" + name + ", how are you today! i hope you are well")
        accounts.write("USER: " + name + "\n")
        a = True
        while a:
            main()
            time.sleep(3)
    else:
        boxstatus('Did not understand.')
        speak("well, i wasn't able to catch your name, so i'll ask again.")
        time.sleep(0.5)
        intro()

def accountselection():
    newdow = tk.Tk()
    newdow.geometry('320x130+5+5')
    for i in accountdata:
        window.label = ttk.Button(window, textvariable = window.text, command = findUser(i))



def startup():
    boxstatus('Voice Assistant Status: Configuration')
    speak('processing, starting up')
    if not accountdata:
        speak('no previous user interaction detected')
        intro()
    elif len(accountdata) == 1:
        name = accountdata[0]
        boxstatus(f'Hello {name}!')
        speak("hello" + name + ", welcome back.")
        a = True
        while a:
            main()
            time.sleep(3)
    else:
        speak('multiple users detected')
        accountselection()
        

def main():
    boxstatus('Voice Assistant Status: Listening')
    speak("what would you like to do?")

    query = str(takeCommand()).split()
    boxstatus(f"Analysing input: '{' '.join(query)}'")
    if 'obsidian' in query:
        speak("Understood, opening Obsidian")
        os.startfile("C:\\Users\\edwar\\AppData\\Local\\Obsidian\\Obsidian.exe")
        boxstatus("Success!")
    elif 'restart' in query:
        speak("restarting")
        os.execv(sys.executable, ['python'] + sys.argv)
        boxstatus("Success!")
    elif 'Firefox' in query:
        speak("Understood, opening firefox.")
        os.startfile("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
        boxstatus("Success!")
    elif 'close program' in ' '.join(query):
        speak("Understood, see you again soon.")
        exit()
    else:
        boxstatus("Failed to understand command.")
        speak("Sorry. i don't understand. Please be more specific.")


window = tk.Tk()

#image stuff
img = Image.open("C:\\Users\\edwar\\Documents\\obsidianmindgarden\\assets\\avatar.png")
resized = img.resize((75,75) , resample=3)
img = ImageTk.PhotoImage(resized)
label = tk.Label(window, image = img)
label.pack()


window.iconbitmap('C:\\Users\\edwar\\Documents\\obsidianmindgarden\\assets\\favicon.ico')

window.title("Ed's Voice Assistant!")
window.text = tk.StringVar()
window.text.set("Press to start program!")
window.geometry('320x130+5+5')

window.label = ttk.Button(window, textvariable = window.text, command = startup)

window.label.pack()
window.attributes('-topmost', 1)
window.mainloop()

