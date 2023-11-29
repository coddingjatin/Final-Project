import pyttsx3
import datetime
import speech_recognition as sr
import os
import re
import wikipedia
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import smtplib
import psutil
import pyjokes
import requests
import time
from click import echo
import webbrowser
import subprocess
import pyautogui

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)
engine.setProperty('rate', 180)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")
        print("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   
        print("Good Afternoon!")   

    else:
        speak("Good Evening!")  
        print("Good Evening!")  

    speak("Sir... I am Magnus...How may I help you?")       

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.energy_threshold = 4000
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        print("Say that again please...")  
        return "None"
    return query

def extract_numbers(text):
    # Regular expression to find integers and floats in the text
    pattern = r"[-+]?\d*\.\d+|\d+"
    numbers = re.findall(pattern, text)
    return numbers

def set_volume(number):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Adjust the volume (0.0 to 1.0)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    if number >1.0:
        set_vol = 1.0
    elif number<0.0:
         set_vol = 0.0 
    volume.SetMasterVolumeLevelScalar(set_vol, None)

def inc_volume(number):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Adjust the volume (0.0 to 1.0)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    set_vol = current_volume + number
    if set_vol >1.0:
        set_vol = 1.0
    volume.SetMasterVolumeLevelScalar(set_vol, None)

def inc_volume_def():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Adjust the volume (0.0 to 1.0)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    
    volume.SetMasterVolumeLevelScalar(current_volume + 0.1, None)

def dec_volume(number):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Adjust the volume (0.0 to 1.0)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    set_vol = current_volume - number  
    if set_vol <0.0:
        set_vol = 0.0
    volume.SetMasterVolumeLevelScalar(set_vol, None)

def dec_volume_def():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

# Adjust the volume (0.0 to 1.0)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    current_volume = volume.GetMasterVolumeLevelScalar()
    set_vol = current_volume - 0.1
    if set_vol <0:
        set_vol = 0.0    
    volume.SetMasterVolumeLevelScalar(set_vol, None)

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
        
def run_python_program(program_name):
    try:
        subprocess.Popen(["python", program_name])
        speak(f"Running {program_name}.")
    except Exception as e:
        speak(f"An error occurred while trying to run {program_name}.")

def get_system_info():
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage('/')

    speak(f"System Information: CPU Usage is {cpu_usage} percent. "
          f"Memory Usage is {memory_info.percent} percent. "
          f"Disk Usage is {disk_info.percent} percent.")

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

def set_timer(minutes):
    try:
        minutes = int(minutes)
        seconds = minutes * 60
        speak(f"Timer set for {minutes} minutes.")
        time.sleep(seconds)
        speak("Timer is up!")
    except ValueError:
        speak("Please provide a valid number of minutes for the timer.")

def search_amazon_product(product_name):
    try:
        # Create the Amazon search URL with the product name
        amazon_url = f"https://www.amazon.in//s?k={product_name.replace(' ', '+')}"
        
        # Open the Amazon search results in the default web browser
        webbrowser.open(amazon_url)
        
        speak(f"Here are the Amazon search results for {product_name}.")
    except Exception as e:
        speak("Sorry, something went wrong while trying to search for the product on Amazon.")

def search_flipkart_product(product_name):
    try:
        # Create the Flipkart search URL with the product name
        flipkart_url = f"https://www.flipkart.com/search?q={product_name.replace(' ', '+')}"
        
        # Open the Flipkart search results in the default web browser
        webbrowser.open(flipkart_url)
        
        speak(f"Here are the Flipkart search results for {product_name}.")
    except Exception as e:
        speak("Sorry, something went wrong while trying to search for the product on Flipkart.")

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

def play_spotify_song(song_name):
    try:
        os.system(f'spotify:search:{song_name}')
        speak(f"Playing {song_name} on Spotify.")
    except Exception as e:
        speak("Sorry, I couldn't play the song on Spotify.")      

def play_youtube_video(query):
    try:
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        speak("Here are the YouTube search results for your query.")
    except Exception as e:
        speak("Sorry, something went wrong while trying to play the YouTube video.")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()
        if query=='none':
            continue
    
        elif "open" in query:
                app_name = query.replace("open", "").strip()
                try:
                    os.startfile(app_name + ".exe")
                except FileNotFoundError:
                    speak(f"Sorry, I couldn't find the {app_name} application.")
                else:
                    speak(f"Opening {app_name}.")

        elif "close" in query:
                    app_name = query.replace("close", "").strip()
                    try:
                        process_name = app_name + ".exe"
                        os.system(f"taskkill /f /im {process_name}")
                    except FileNotFoundError:
                        speak(f"Sorry, I couldn't find the {app_name} application running...")

        elif 'wikipedia' in query:  
            speak('Searching Wikipedia...')
            try:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2) 
                speak("According to Wikipedia...")
                print(results)
                speak(results) 
            except Exception as e:
                speak("There is no information in wikipedia about your query...")
                print("There is no information in wikipedia about your query...")   

        elif 'volume' and 'zero' in query:
            set_volume(0.0)    

        elif ('decrease volume by') in query:
            num = extract_numbers(query)
            float_num = float(num[0])
            float_num = float_num/100
            dec_volume(float_num)
        
        elif ('increase volume by') in query:
            num = extract_numbers(query)
            float_num = float(num[0])
            float_num = float_num/100
            inc_volume(float_num)

        elif 'increase volume' in query:
             inc_volume_def()   

        elif 'decrease volume' in query:
             dec_volume_def() 
        
        elif 'set volume' in query:
            num = extract_numbers(query)
            float_num = float(num[0])
            float_num = float_num/100
            set_volume(float_num)
        
        elif "create folder" in query:
                folder_name = query.replace("create folder", "").strip()
                if folder_name:
                    create_folder(folder_name)
                else:
                    speak("Please specify a folder name.")

        elif "create file" in query:
            file_name = query.replace("create file", "").strip()
            if file_name:
                create_file(file_name)
            else:
                speak("Please specify a file name.") 
      
        elif "gesture" in query:
                program_name = "Gesture_Controller.py" 
                run_python_program(program_name)        

        elif "system information" in query:
            get_system_info()

        elif "joke" in query:
            joke = pyjokes.get_joke(language='en', category='programming')
            speak(joke)
            print(joke)       

        elif "weather" in query:
            location = query.replace("weather", "").strip()
            if location:
                get_weather(location)
            else:
                speak("Please specify a location for weather updates.") 

        elif 'time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"the time is {strTime}")

        elif "timer" in query:
            minutes = query.replace("timer", "").strip()
            if minutes:
                set_timer(minutes)
            else:
                speak("Please specify the timer duration in minutes.") 

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"the time is {strTime}")
            speak(f"the time is {strTime}")        

        elif "camera" in query or "take a photo" in query:
            echo.capture(0, "robo camera", "img.jpg") 
            print("Photo Clicked Successfully!")    
            speak("Photo Clicked Successfully!")    

        elif 'news' in query:
            news = webbrowser.open_new_tab("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India,Happy reading')
            time.sleep(6)  

        elif "search on amazon for" in query:
            product_name = query.replace("search on amazon for", "").strip()
            if product_name:
                search_amazon_product(product_name)
            else:
                speak("Please specify a product name to search for on Amazon.")  

        elif "Browse flipkart" in query or "browse flipkart" in query:
            webbrowser.open_new_tab("https://flipkart.com")
            speak("Here is Flipkart")

        elif "Browse Github" in query or "browse github" in query:
            webbrowser.open_new_tab("https://github.com/coddingjatin")
            speak("Here is Github")   

        elif "Browse Geeksforgeeks" in query or "browse geeksforgekks" in query:
            webbrowser.open_new_tab("https://www.geeksforgeeks.org/")
            speak("Here is Geeksforgeeks") 

        elif "Browse Javatpoint" in query or "browse javatpoint" in query:
            webbrowser.open_new_tab("https://www.javatpoint.com/")
            speak("Here is Geeksforgeeks")                         

        elif "browse amazon" in query or "browse amazon" in query:
            webbrowser.open_new_tab("https://amazon.in")
            speak("Here is Amazon")               

        elif "search on flipkart for" in query:
            product_name = query.replace("search on flipkart for", "").strip()
            if product_name:
                search_flipkart_product(product_name)
            else:
                speak("Please specify a product name to search for on Flipkart.")     

        elif "switch off" in query or "shut down" in query or "shutdown" in query:
            speak("Ok , your pc will shut down now")
            subprocess.call(["shutdown", '/s', '/t', '0'])

        elif "screenshot" in query or "take a screenshot" in query:
            take_screenshot()     

        elif "play song" in query or "play music" in query:
            speak("Sure, what song would you like to play on Spotify?")
            song_name = takeCommand()
            if song_name:
                play_spotify_song(song_name)       

        elif "youtube" in query:
            query = query.replace("youtube", "").strip()
            if query:
                play_youtube_video(query)
            else:
                speak("Please specify a search term after 'YouTube.'")

        elif "stop" in query:
            print("Logging out! ")
            speak("Logging out! ")
            break
        
        else:
            search_web(query)