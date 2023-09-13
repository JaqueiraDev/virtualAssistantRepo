import openai
import speech_recognition as sr
from gtts import gTTS
import os
import time
import execute_tasks as tasks

# Configure your OpenAI API key
openai.api_key = "MY_API_KEY"
user_input = ""
messages = []
recognizer = sr.Recognizer()  # initialize the recognizer
url_to_open = ''
google_url = "https://www.google.pt"
stop_conversation = ["close conversation", "close this conversation", "stop conversation", "stop this conversation",
                     "end conversation", "end this conversation", "finish conversation", "finish this conversation"
                     "shut down", "stop speaking", "close the software", "shutdown"]
keep_conversation = True


# Function to recognize speech
def recognize_speech():
    global user_input
    # Open the microphone and start listening
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 2
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio).lower()  # Convert speech to text
        print(user_input)
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand your speech. Please try again.")
    except sr.RequestError:
        print("Sorry, there was an error with the speech recognition service. Please try again.")
    return ""


# Function for Text-to-Speech (TTS) conversion (Option 1)
def text_to_speech(text):
    tts = gTTS(text=text, lang='en-uk')
    tts.save("output.mp3")
    os.system("mpg321 output.mp3")  # Install mpg321: sudo apt-get install mpg321
    time.sleep(1)  # Wait for the audio to finish playing
    global user_input
    user_input = ""  # Stop repeating previous answer.


# Function for Text-to-Speech (TTS) conversion (Option 2)
def text_to_speech2(text, rate_voice_speed):
    voice_name = "Jamie"
    os.system(f'say -v {voice_name} -r {rate_voice_speed} "{text}"')
    global user_input
    user_input = ""


# Function to get the response from ChatGPT
def get_chatgpt_response(question, model="gpt-3.5-turbo"):
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


# Welcome message
tasks.check_os()
introduction = "Hi Sir, how can i assist you today?"
print(introduction)
if tasks.os_name == "Darwin":
    text_to_speech2(introduction, 160)
else:
    text_to_speech(introduction)

# Main loop of the AI assistant
while keep_conversation:
    recognize_speech()
    if user_input != "":
        if user_input.lower().__contains__("jarvis") or user_input.lower().__contains__(
                "jars") or user_input.lower().__contains__("jarvi") or user_input.lower().__contains__("jar"):
            for frase in stop_conversation:
                if user_input.lower().__contains__(frase):
                    messages.append({"role": "user", "content": user_input})
                    response = get_chatgpt_response(messages)  # Get the response from ChatGPT
                    print("J.A.R.V.I.S: ", response)  # Display the response from ChatGPT and play it as speech
                    if tasks.os_name == "Darwin":
                        text_to_speech2(response, 160)  # text_to_speech(response)
                    else:
                        text_to_speech(response)  # text_to_speech(response)
                    keep_conversation = False  # Get out of the while loop
                    # print("Should close conversation right now!")
                    break
            if (user_input.lower().__contains__("open google") or user_input.lower().__contains__("open opera")
                    or user_input.lower().__contains__("open browser")):
                tasks.open_page(google_url)
                user_input = ""
            elif user_input.lower().__contains__("open page") or user_input.lower().__contains__("open the page"):
                input_split = user_input.split("page", 1)
                new_url = input_split[1]
                tasks.open_page(new_url)
                user_input = ""
            elif user_input.lower().__contains__('open app') or user_input.lower().__contains__('open application'):
                input_split = user_input.split('open app' or 'open application', 1)
                app = input_split[1].strip().capitalize()
                tasks.open_app(app)
                user_input = ""
            elif keep_conversation:
                messages.append(
                    {"role": "user", "content": "Act like your name is JARVIS. "
                                                + user_input})
                response = get_chatgpt_response(messages)  # Get the response from ChatGPT
                print("J.A.R.V.I.S: ", response)  # Display the response from ChatGPT and play it as speech
                if tasks.os_name == "Darwin":
                    text_to_speech2(response, 160)  # text_to_speech(response)
                else:
                    text_to_speech(response)  # text_to_speech(response)

print("Goodbye! Have a great day.")
