import openai
import speech_recognition as sr
from gtts import gTTS
import os
import time
import execute_tasks as tasks
import pyaudio
import myApi

# OpenAI API key
openai.api_key = myApi.openai_key
user_input, url_to_open = "", ''
messages = []  # List to keep the conversation
recognizer = sr.Recognizer()  # initialize the recognizer
google_url = "https://www.google.pt"
keep_conversation = True
jarvis_name = ['john', 'jon', 'joan']
stop_conversation = ["close conversation", "close this conversation", "stop conversation", "stop this conversation",
                     "end conversation", "end this conversation", "finish conversation", "finish this conversation",
                     "shut down", "stop speaking", "close the software", "shutdown"]
conversation_mode = False
interview_mode = False
safe_mode = True
tkn = 300


def main():
    global keep_conversation, user_input

    def recognize_speech():  # Function to recognize speech
        global user_input
        mic = sr.Microphone()
        with mic as source:  # Open the microphone and start listening
            print("Listening...")
            recognizer.pause_threshold = 1.5
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio).lower()  # Convert speech to text
            print(user_input)
        except sr.UnknownValueError:
            print("Sorry, i could not understand. Please say again.")
            return ''
        except sr.RequestError:
            print("Sorry, there was an error with the speech recognition service. Please try again.")
            return ''
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
            max_tokens=tkn,
            n=1,
            stop=None,
            temperature=0.5,
        )
        message = gpt_response.choices[0].message.content
        messages.append(gpt_response.choices[0].message)
        return message

    def speech_function(say_text):
        if tasks.os_name == "Darwin":
            text_to_speech2(say_text, 180)
        else:
            text_to_speech(say_text)

    tasks.check_os()
    introduction = "Hi Alan, how can i assist you today?"  # Welcome message
    print(introduction)
    speech_function(introduction)

    while keep_conversation:  # Main loop of the AI assistant
        global interview_mode, conversation_mode, safe_mode, tkn
        recognize_speech()
        if user_input != "":
            if user_input.lower().__contains__('go to safe mode'):
                safe_mode = True
                conversation_mode = False
                interview_mode = False
                user_input = ""
                speech_function("I'm on safe mode now, please call me when you need me!")
            elif user_input.lower().__contains__('go to interview mode'):
                safe_mode = False
                conversation_mode = False
                interview_mode = True
                user_input = ""
                speech_function("I'm on interview mode now, please tell me the title of the job offer. ")
            elif user_input.lower().__contains__('go to conversation mode'):
                safe_mode = False
                conversation_mode = True
                interview_mode = False
                user_input = ""
                speech_function("I'm on conversation mode now, what do you want to talk about?")
            else:
                if safe_mode:
                    for name in jarvis_name:  # Recognizes if it's calling jarvis name
                        if user_input.lower().__contains__(name):
                            for frase in stop_conversation:
                                if user_input.lower().__contains__(frase):
                                    speech_function("See you next time. Have a great day!")  # text_to_speech(response)
                                    keep_conversation = False  # Get out of the while loop
                                    print("Conversation has been closed!")
                                    break
                            if (user_input.lower().__contains__("open google") or user_input.lower().__contains__(
                                    "open opera")
                                    or user_input.lower().__contains__("open browser")):
                                speech_function(f"Ok Sir, opening browser")
                                tasks.open_page(google_url)
                                user_input = ""
                            elif user_input.lower().__contains__("open page") or user_input.lower().__contains__(
                                    "open the page"):
                                input_split = user_input.split("page", 1)
                                new_url = input_split[1]
                                speech_function("Will do it, Sir!")
                                tasks.open_page(new_url)
                                user_input = ""
                            elif user_input.lower().__contains__('search for'):
                                input_split = user_input.split('search for', maxsplit=1)
                                text_to_search = input_split[1]
                                speech_function(f"Ok, searching for {text_to_search} on google!")
                                tasks.search_on_google(text_to_search)
                            elif user_input.lower().__contains__('open application'):
                                input_split_application = user_input.split('application', 1)
                                print(input_split_application)
                                if len(input_split_application) < 2:
                                    speech_function("Sorry, i couldn't understand which application you want to open.")
                                else:
                                    app = input_split_application[1]
                                    speech_function(f"Ok, opening {app}")
                                    tasks.open_app(app)
                                    user_input = ""
                            elif user_input.lower().__contains__('open app'):
                                input_split_app = user_input.split('open app ', 1)
                                print(input_split_app)
                                if len(input_split_app) < 2:
                                    speech_function("Sorry, i couldn't understand which application you want to open.")
                                else:
                                    app = input_split_app[1]
                                    speech_function(f"Ok, opening {app}")
                                    tasks.open_app(app)
                                    user_input = ""
                            elif user_input.lower().__contains__('play the song') or user_input.lower().__contains__(
                                    'play the music'):
                                input_split_song = user_input.split('the song', 1)
                                input_split_music = user_input.split('the music', 1)
                                if len(input_split_song) > 1:
                                    music_name = input_split_song[1].strip()
                                elif len(input_split_music) > 1:
                                    music_name = input_split_music[1].strip()
                                else:
                                    speech_function("I couldn't understand which song or music you want to play.")
                                    speech_function(f"Ok, opening spotify!")
                                    tasks.play_song_spotify(music_name)
                                    user_input = ''
                            elif keep_conversation:
                                tkn = 300
                                messages.append(
                                    {"role": "user", "content": "Act like your name is John. " + user_input})
                                response = get_chatgpt_response(messages)  # Get the response from ChatGPT
                                print("J.O.H.N.: ", response)  # Display the response from ChatGPT and play it as speech
                                speech_function(response)  # text_to_speech(response)
                elif interview_mode:
                    for frase in stop_conversation:
                        if user_input.lower().__contains__(frase):
                            speech_function("See you next time. Have a great day!")  # text_to_speech(response)
                            keep_conversation = False  # Get out of the while loop
                            print("Conversation has been closed!")
                            break
                    if not user_input.lower().__contains__(frase):
                        tkn = 200
                        job_title = user_input.lower().strip()
                        messages.append({"role": "user", "content": f"Make another random and short interview "
                                                                    f"question about {job_title} for a job position."})
                        response = get_chatgpt_response(messages)  # Get the response from ChatGPT
                        print("J.O.H.N.: ", response)  # Display the response from ChatGPT and play it as speech
                        speech_function(response)  # text_to_speech(response)
                elif conversation_mode:
                    for frase in stop_conversation:
                        if user_input.lower().__contains__(frase):
                            speech_function("See you next time. Have a great day!")  # text_to_speech(response)
                            keep_conversation = False  # Get out of the while loop
                            print("Conversation has been closed!")
                            break
                    else:
                        tkn = 150
                        messages.append({"role": "user",
                                         "content": user_input + "Lets have a short talk like you are my friend?"})
                        response = get_chatgpt_response(messages)  # Get the response from ChatGPT
                        print("J.O.H.N.: ", response)  # Display the response from ChatGPT and play it as speech
                        speech_function(response)  # text_to_speech(response)
    print("See you next time. Have a great day!")


if __name__ == "__main__":
    main()
