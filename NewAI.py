import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import json
import requests
import tkinter as tk
from tkinter import scrolledtext, PhotoImage, Label, Button
from PIL import Image, ImageTk
import threading

print('Loading your AI personal assistant')

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

class VoiceAssistantGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Siri")
        self.root.geometry("600x700")
        self.root.configure(bg="#282828")

        # Set up the logo
        self.logo_img = Image.open("googleImage.png")  # Replace with your logo file
        self.logo_img = self.logo_img.resize((100, 100), Image.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        self.logo_label = Label(self.root, image=self.logo_photo, bg="#282828")
        self.logo_label.pack(pady=20)

        # Set up the text area
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=20, bg="#404040", fg="white", font=("Helvetica", 14))
        self.text_area.pack(pady=10, padx=10)
        #self.text_area.insert(tk.END, "Assistant: Hi I'm siri \n")

        # Set up the listen button
        self.listen_img = Image.open("Google_mic.png")  # Replace with your microphone icon file
        self.listen_img = self.listen_img.resize((50, 50), Image.LANCZOS)
        self.listen_photo = ImageTk.PhotoImage(self.listen_img)
        self.listen_button = Button(self.root, image=self.listen_photo, command=self.start_listening, bg="#282828", borderwidth=0)
        self.listen_button.pack(pady=20)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def speak(self, text):
        self.text_area.insert(tk.END, f"Assistant: {text}\n")
        self.text_area.see(tk.END)
        engine.say(text)
        engine.runAndWait()

    def wishMe(self):
        hour = datetime.datetime.now().hour
        if hour >= 0 and hour < 12:
            self.speak("Hello, Good Morning \nI am siri")
        elif hour >= 12 and hour < 18:
            self.speak("Hello, Good Afternoon \nI am siri")
        else:
            self.speak("Hello, Good Evening \nI am siri")
    
        
    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_area.insert(tk.END, "Listening...\n")
            self.text_area.see(tk.END)
            r.pause_threshold = 1
            audio = r.listen(source)

            try:
                statement = r.recognize_google(audio, language='en-in')
                self.text_area.insert(tk.END, f"Recognizing...\nYou said: {statement}\n")
                self.text_area.see(tk.END)
            except Exception as e:
                self.speak("Hey, please say that again")
                return "None"
            return statement.lower()

    def start_listening(self):
        threading.Thread(target=self.run_assistant).start()

    def run_assistant(self):
        self.wishMe()
        while True:
            self.speak("Tell me how can I help you now?")
            statement = self.takeCommand()
            if statement == 0:
                continue

            if "bye" in statement or "ok bye" in statement or "ok stop here" in statement:
                self.speak('Your personal assistant is shutting down, Goodbye')
                break

            if 'wikipedia' in statement:
                self.speak('Searching Wikipedia...')
                statement = statement.replace("wikipedia", "")
                results = wikipedia.summary(statement, sentences=3)
                self.speak("According to Wikipedia")
                self.speak(results)

            elif 'open youtube' in statement:
                webbrowser.open_new_tab("https://www.youtube.com")
                self.speak("YouTube is open now")
                time.sleep(10)

            elif 'open insta' in statement or 'instagram' in statement:
                webbrowser.open_new_tab("https://www.instagram.com")
                self.speak("Instagram is open now")
                time.sleep(10)

            elif 'open google' in statement:
                webbrowser.open_new_tab("https://www.google.com")
                self.speak("Google Chrome is open now")
                time.sleep(10)

            elif 'open gmail' in statement:
                webbrowser.open_new_tab("gmail.com")
                self.speak("Google Mail is open now")
                time.sleep(10)

            elif "weather" in statement:
                api_key = "8ef61edcf1c576d65d836254e11ea420"
                base_url = "https://api.openweather.map.org/data/2.5/weather?"
                self.speak("What's the city name?")
                city_name = self.takeCommand()
                complete_url = base_url + "appid=" + api_key + "&q=" + city_name
                response = requests.get(complete_url)
                x = response.json()
                if x["cod"] != "404":
                    y = x["main"]
                    current_temperature = y["temp"]
                    current_humidity = y["humidity"]
                    z = x["weather"]
                    weather_description = z[0]["description"]
                    self.speak("Temperature in kelvin unit is " +
                              str(current_temperature) +
                              "\nHumidity in percentage is " +
                              str(current_humidity) +
                              "\nDescription: " +
                              str(weather_description))
                else:
                    self.speak("City Not Found")

            elif 'time' in statement:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                self.speak(f"The time is {strTime}")

            elif 'who are you' in statement or 'what can you do' in statement:
                self.speak('I am G-one version 1.0 your personal assistant. I am programmed to perform minor tasks like '
                          'opening YouTube, Google Chrome, Gmail, and Stack Overflow, predict time, take a photo, search Wikipedia, predict weather '
                          'in different cities, get top headline news from Times of India, and answer computational or geographical questions.')

            elif "who made you" in statement or "who created you" in statement:
                self.speak("I was built by Harshal Daud, Ganesh Tirsule, and Gaurav Ranyeole")

            elif "open stackoverflow" in statement:
                webbrowser.open_new_tab("https://stackoverflow.com/login")
                self.speak("Here is Stack Overflow")

            elif 'news' in statement:
                news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
                self.speak('Here are some headlines from the Times of India, Happy reading')
                time.sleep(10)

            elif 'open newspaper' in statement:
                news = webbrowser.open_new_tab("https://indianexpress.com")
                self.speak('Here are some headlines from the Indian Express, Happy reading')
                time.sleep(10)

            elif "camera" in statement or "take a photo" in statement:
                ec.capture(0, "robo camera", "img.jpg")

            elif 'search' in statement:
                statement = statement.replace("search", "")
                webbrowser.open_new_tab(statement)
                time.sleep(10)

            elif 'ask' in statement or 'give answer' in statement or 'question' in statement:
                self.speak('I can answer computational and geographical questions. What question do you want to ask now?')
                question = self.takeCommand()
                app_id = "R2K75H-7ELALHR35X"
                client = wolframalpha.Client(app_id)
                res = client.query(question)
                answer = next(res.results).text
                self.speak(answer)

            elif "log off" in statement or "sign out" in statement:
                self.speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
                subprocess.call(["shutdown", "/l"])

            elif "play a song" in statement or "song" in statement:
                self.speak("Which song do you want to listen to?")
                song = self.takeCommand()
                webbrowser.open_new_tab(f"https://www.youtube.com/results?search_query={song}")
                self.speak("This is special for you")
                time.sleep(15)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAssistantGUI(root)
    root.mainloop()
