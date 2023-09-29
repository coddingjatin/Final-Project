import datetime
import subprocess
import time
from click import echo
import pyautogui
import speech_recognition as sr
import pyttsx3
import os
import wikipedia
import webbrowser
import psutil
import requests
import random

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 0.9)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"Jatin: {query}")
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand. Can you please repeat?")
        speak("Sorry, I couldn't understand. Can you please repeat?")
        return None
    except sr.RequestError as e:
        print("Speech recognition service is currently unavailable. Please try again later.")
        return None
def run_python_program(program_name):
    try:
        subprocess.Popen(["python", program_name])
        speak(f"Running {program_name}.")
    except Exception as e:
        speak(f"An error occurred while trying to run {program_name}.")

def search_amazon_product(product_name):
    try:
        # Create the Amazon search URL with the product name
        amazon_url = f"https://www.amazon.in//s?k={product_name.replace(' ', '+')}"
        
        # Open the Amazon search results in the default web browser
        webbrowser.open(amazon_url)
        
        speak(f"Here are the Amazon search results for {product_name}.")
    except Exception as e:
        speak("Sorry, something went wrong while trying to search for the product on Amazon.")

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    speak(f"System Information: CPU Usage is {cpu_usage} percent. "
          f"Memory Usage is {memory_info.percent} percent. "
          f"Disk Usage is {disk_info.percent} percent.")

jokes = [
    "Why did the computer keep freezing? Because it left its Windows open!",
    "Why did the programmer go broke? Because he used up all his cache!",
    
]
def tell_joke():
    joke = random.choice(jokes)
    speak(joke)      

def get_weather(location):
    api_key = "38009e346e2993f698efd436bfb80bfa"
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": location,
        "appid": api_key,
        "units": "metric"  # You can use "imperial" for Fahrenheit
    }
    
    response = requests.get(base_url, params=params)
    weather_data = response.json()

    if weather_data.get("main"):
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        speak(f"The weather in {location} is {description}. The temperature is {temperature} degrees Celsius.")
    else:
        speak("I couldn't retrieve weather information for that location.")


def search_wikipedia(query):
    try:
        search_results = wikipedia.search(query)
        if not search_results:
            speak(f"Sorry, I couldn't find information on {query} in Wikipedia.")
            return

        first_result = search_results[0]
        summary = wikipedia.summary(first_result, sentences=2)
        speak(f"Here's what I found on Wikipedia for {first_result}: {summary}")
    except wikipedia.exceptions.DisambiguationError as e:
        speak("There are multiple options for this search. Please choose a specific topic.")
    except wikipedia.exceptions.PageError as e:
        speak(f"Sorry, I couldn't find information on {query} in Wikipedia.")


def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)


def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
        speak(f"Folder {folder_name} created successfully.")
    except FileExistsError:
        speak(f"The folder {folder_name} already exists.")
    except Exception as e:
        speak(f"An error occurred while creating the folder {folder_name}.")


def create_file(file_name):
    try:
        with open(file_name, 'w') as file:
            file.write('')
        speak(f"File {file_name} created successfully.")
    except Exception as e:
        speak(f"An error occurred while creating the file {file_name}.")    

def adjust_volume(volume_level):
    try:
        volume_level = float(volume_level)
        if 0.0 <= volume_level <= 1.0:
            engine.setProperty('volume', volume_level)
            speak(f"Volume adjusted to {volume_level}.")
        else:
            speak("Volume level should be between 0.0 and 1.0.")
    except ValueError:
        speak("Please provide a valid volume level between 0.0 and 1.0.")
def set_timer(minutes):
    try:
        minutes = int(minutes)
        seconds = minutes * 60
        speak(f"Timer set for {minutes} minutes.")
        time.sleep(seconds)
        speak("Timer is up!")
    except ValueError:
        speak("Please provide a valid number of minutes for the timer.")
def search_flipkart_product(product_name):
    try:
        # Create the Flipkart search URL with the product name
        flipkart_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
        
        # Open the Flipkart search results in the default web browser
        webbrowser.open(flipkart_url)
        
        speak(f"Here are the Flipkart search results for {product_name}.")
    except Exception as e:
        speak("Sorry, something went wrong while trying to search for the product on Flipkart.")

def play_youtube_video(query):
    try:
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        speak("Here are the YouTube search results for your query.")
    except Exception as e:
        speak("Sorry, something went wrong while trying to play the YouTube video.")
def open_spotify():
    try:
        subprocess.Popen(["spotify"])
        speak("Opening Spotify.")
    except Exception as e:
        speak("Sorry, I couldn't open Spotify.")

def play_spotify_song(song_name):
    try:
        os.system(f'spotify:search:{song_name}')
        speak(f"Playing {song_name} on Spotify.")
    except Exception as e:
        speak("Sorry, I couldn't play the song on Spotify.")
def take_screenshot():
    try:
        screenshot = pyautogui.screenshot()
        current_directory = os.getcwd()
        timestamp = time.strftime("%Y%m%d%H%M%S")
        screenshot_filename = f"screenshot_{timestamp}.png"
        screenshot.save(os.path.join(current_directory, screenshot_filename))
        speak(f"Screenshot saved as {screenshot_filename} in the program's directory.")
    except Exception as e:
        speak("Sorry, something went wrong while taking the screenshot.")


if __name__ == "__main__":
    speak("Hello, I am Jarvis . How are you Jatin  ,  Pushkar  ,  Pradnya and    Taanaay     and , How can i help you?")

    while True:
        user_input = listen()
        if user_input:
            if "exit" in user_input.lower():
                speak("Goodbye!")
                break
            elif "tech" in user_input.lower():
                program_name = "Gesture_Controller.py" 
                run_python_program(program_name)
            elif "open" in user_input.lower():
                app_name = user_input.lower().replace("open", "").strip()
                try:
                    os.startfile(app_name + ".exe")
                except FileNotFoundError:
                    speak(f"Sorry, I couldn't find the {app_name} application.")
                else:
                    speak(f"Opening {app_name}.")
            elif "wikipedia" in user_input.lower():
                query = user_input.lower().replace("wikipedia", "").strip()
                if query:
                    search_wikipedia(query)
                else:
                    speak("Please specify a search term after 'Wikipedia.'")
            elif "volume" in user_input.lower():
                volume_level = user_input.lower().replace("volume", "").strip()
                if volume_level:
                    adjust_volume(volume_level)
                else:
                    speak("Please specify a volume level between 0.0 and 1.0.")
            elif "create folder" in user_input.lower():
                folder_name = user_input.lower().replace("create folder", "").strip()
                if folder_name:
                    create_folder(folder_name)
                else:
                    speak("Please specify a folder name.")
            elif "create file" in user_input.lower():
                file_name = user_input.lower().replace("create file", "").strip()
                if file_name:
                    create_file(file_name)
                else:
                    speak("Please specify a file name.")    
            elif "system information" in user_input.lower():
                get_system_info()
            elif "tell a joke" in user_input.lower():
                tell_joke()
            elif "weather" in user_input.lower():
                location = user_input.lower().replace("weather", "").strip()
                if location:
                    get_weather(location)
                else:
                    speak("Please specify a location for weather updates.") 
            elif "timer" in user_input.lower():
                minutes = user_input.lower().replace("timer", "").strip()
                if minutes:
                    set_timer(minutes)
                else:
                    speak("Please specify the timer duration in minutes.")         
            elif 'time' in user_input.lower():
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")        
            elif "camera" in user_input.lower() or "take a photo" in user_input.lower():
                echo.capture(0, "robo camera", "img.jpg")    
            elif "Browse Github" in user_input.lower():
                webbrowser.open_new_tab("https://github.com")
                speak("Here is Github")  
            elif 'news' in user_input.lower():
                news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
                speak('Here are some headlines from the Times of India,Happy reading')
                time.sleep(6)  
            elif "alexa" in user_input.lower():
                product_name = user_input.lower().replace("alexa", "").strip()
                if product_name:
                    search_amazon_product(product_name)
                else:
                    speak("Please specify a product name to search for on Amazon.")  
            elif "Browse flipkart" in user_input.lower():
                webbrowser.open_new_tab("https://flipkart.com")
                speak("Here is Flipkart")   
            elif "Browse amazon" in user_input.lower():
                webbrowser.open_new_tab("https://amazon.in")
                speak("Here is Amazon")                        
            elif "flippy" in user_input.lower():
                product_name = user_input.lower().replace("flippy", "").strip()
                if product_name:
                    search_flipkart_product(product_name)
                else:
                    speak("Please specify a product name to search for on Flipkart.")          
            elif "switch off" in user_input.lower() or "shut down" in user_input.lower() or "shutdown" in user_input.lower():
                speak("Ok , your pc will shut down now")
                subprocess.call(["shutdown", '/s', '/t', '0'])
            elif "screenshot" in user_input.lower() or "take a screenshot" in user_input.lower():
                take_screenshot()     
            elif "open spotify" in user_input.lower():
                open_spotify()
            elif "play song" in user_input.lower() or "play music" in user_input.lower():
                speak("Sure, what song would you like to play on Spotify?")
                song_name = listen()
                if song_name:
                    play_spotify_song(song_name)                         
            elif "youtube" in user_input.lower():
                query = user_input.lower().replace("youtube", "").strip()
                if query:
                    play_youtube_video(query)
                else:
                    speak("Please specify a search term after 'YouTube.'")        
            else:
                search_web(user_input)
 