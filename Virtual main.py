import subprocess
import speech_recognition as sr
import pyttsx3
import os
import wikipedia
import webbrowser

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
def play_youtube_video(query):
    try:
        url = f"https://www.youtube.com/results?search_query={query}"
        webbrowser.open(url)
        speak("Here are the YouTube search results for your query.")
    except Exception as e:
        speak("Sorry, something went wrong while trying to play the YouTube video.")



if __name__ == "__main__":
    speak("Hello, I am Jarvis . How are you Jatin  ,  Pushkar  ,  Pradnya and    Tanay     and , How can i help you?")

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
            elif "youtube" in user_input.lower():
                query = user_input.lower().replace("youtube", "").strip()
                if query:
                    play_youtube_video(query)
                else:
                    speak("Please specify a search term after 'YouTube.'")        
            else:
                search_web(user_input)
 