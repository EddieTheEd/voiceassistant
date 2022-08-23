
import subprocess
import wolframalpha
import pyttsx3
import sys
import tkinter as tk
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


# Startup

clear = lambda: os.system('cls')
clear()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

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

def intro():
    boxstatus("Voice Assistant Status: Configuration")
    speak('hello')
    speak("what is your name")
    name = str(takeCommand())
    speak("hello" + name + ", how are you today!")
    a = True
    while a:
        main()
        time.sleep(3)

def startup():
    boxstatus('Processing...')
    speak('processing, starting up')
    intro()

def main():
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
    elif 'close' in query:
        speak("Understood, see you again soon.")
        exit()
    else:
        speak("Sorry. i don't understand.")
        boxstatus("Failed to understand command.")



window = tk.Tk()
window.title("Ed's Voice Assistant!")
window.text = tk.StringVar()
window.text.set("Press to start program!")
window.label = tk.Button(window, textvariable = window.text, command = startup)
window.label.pack()
window.mainloop()

