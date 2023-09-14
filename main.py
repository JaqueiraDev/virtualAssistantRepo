import openai
import speech_recognition as sr
from gtts import gTTS
import os
import time
import execute_tasks as tasks

# OpenAI API key
openai.api_key = "OpenAI API key"  # ATTENTION REMOVE THIS API KEY BEFORE COMMIT
user_input, url_to_open = "", ''
messages = []  # List to keep the conversation
recognizer = sr.Recognizer()  # initialize the recognizer
google_url = "https://www.google.pt"
keep_conversation = True
jarvis_name = ["jarvis", "jars", "jobs", "jar"]
stop_conversation = ["close conversation", "close this conversation", "stop conversation", "stop this conversation",
                     "end conversation", "end this conversation", "finish conversation", "finish this conversation",
                     "shut down", "stop speaking", "close the software", "shutdown"]


def recognize_speech():  # Function to recognize speech
    global user_input
    with sr.Microphone() as source:  # Open the microphone and start listening
        print("Listening...")
        recognizer.pause_threshold = 1
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio).lower()  # Convert speech to text
        print(user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, i could not understand. Please say again.")
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service. Please try again.")
    return ""


def text_to_speech(text):  # Function for TTS Windows or Linux System
    global user_input
    tts = gTTS(text=text, lang='en-uk')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Install mpg321: sudo apt-get install mpg321
    time.sleep(1)  # Wait for the audio to finish playing
    user_input = ""  # Stop repeating previous answer.


def text_to_speech2(text, rate_voice_speed):  # Function for TTS macOS system
    global user_input
    voice_name = "Jamie"
    os.system(f'say -v {voice_name} -r {rate_voice_speed} "{text}"')
    user_input = ""


def get_chatgpt_response(question, model="gpt-3.5-turbo"):  # Function to get the response from ChatGPT
    gpt_response = openai.ChatCompletion.create(
        model=model,  # Use the GPT-3.5 turbo engine
        messages=question,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = gpt_response.choices[0].message.content
    messages.append(gpt_response.choices[0].message)
    return message


def speech_function(say_text):
    if tasks.os_name == "Darwin":
        text_to_speech2(say_text, 160)
    else:
        text_to_speech(say_text)


tasks.check_os()
introduction = "Hi Sir, how can i assist you today?"  # Welcome message
print(introduction)
speech_function(introduction)


while keep_conversation:  # Main loop of the AI assistant
    recognize_speech()
    if user_input != "":
        for name in jarvis_name:  # Recognizes if it's calling jarvis name
            if user_input.lower().__contains__(name):
                for frase in stop_conversation:
                    if user_input.lower().__contains__(frase):
                        speech_function("See you next time. Have a great day!")  # text_to_speech(response)
                        keep_conversation = False  # Get out of the while loop
                        print("Conversation has been closed!")
                        break
                if (user_input.lower().__contains__("open google") or user_input.lower().__contains__("open opera")
                        or user_input.lower().__contains__("open browser")):
                    speech_function("Will do it, Sir!")
                    tasks.open_page(google_url)
                    user_input = ""
                elif user_input.lower().__contains__("open page") or user_input.lower().__contains__("open the page"):
                    input_split = user_input.split("page", 1)
                    new_url = input_split[1]
                    speech_function("Will do it, Sir!")
                    tasks.open_page(new_url)
                    user_input = ""
                elif user_input.lower().__contains__('open app') or user_input.lower().__contains__('open application'):
                    input_split = user_input.split('open app' or 'open application', 1)
                    app = input_split[1].strip().capitalize()
                    speech_function("Will do it, Sir!")
                    tasks.open_app(app)
                    user_input = ""
                elif keep_conversation:
                    messages.append({"role": "user", "content": "Act like your name is JARVIS. " + user_input})
                    response = get_chatgpt_response(messages)  # Get the response from ChatGPT
                    print("J.A.R.V.I.S: ", response)  # Display the response from ChatGPT and play it as speech
                    speech_function(response)  # text_to_speech(response)

print("See you next time. Have a great day!")
