"""
Author: #Smart_Coder
Date: 24th June 2023
Time: Final code version was available at 3:40 PM
Purpose: Creating a Jarvis AI
"""

# Importing Important Modules
import os
import openai
import webbrowser
import random
from imp_files.config import jarvis_api
import json
import tkinter as tk
import tkinter.messagebox as tmsg
feedback_given = False

def remove_invalid_characters(filename):
    """
    This function removes invalid characters from a filename
    :param filename: file name
    :return: correct file name
    """
    valid_chars = "-_.() %s%s" % (os.sep, os.sep)
    clean_filename = ''.join(c for c in filename if c.isalnum() or c in valid_chars).rstrip()

    return clean_filename

def load_settings():
    """
    This function loads the settings from the settings.json file
    :return: Returns the settings dictionary
    """
    with open("imp_files/settings.json", "r") as file:
        settings = json.load(file)
    allow_speaking = settings.get("allow_speaking")
    save_questions = settings.get("save_questions")
    input_method = settings.get("input_method")

    return allow_speaking, save_questions, input_method


settings = load_settings()
allow_speaking, save_questions, input_method = settings

def open_settings():
    """
    This function opens the settings window
    :return:
    """
    say("Opening settings.")
    # Importing Important libraries and modules
    # Create the Tkinter window
    root = tk.Tk()
    root.title("JARVIS A.I. Settings")
    root.geometry("400x450")
    root.iconbitmap("settings.ico")
    root.resizable(False, False)

    # Function to save settings to a JSON file
    def save_settings():
        with open(r"imp_files\settings.json", "w") as file:
            settings = {
                "allow_speaking": allowspeaking.get(),
                "save_questions": savequestions.get(),
                "input_method": inputmethod.get()
            }
            # Write the settings to the file as a JSON object, with indenting to make it easier to read.
            json.dump(settings, file)
        tmsg.showinfo("JARVIS A.I. Settings", "Settings saved successfully.")

    # Function to load settings from a JSON file
    # Example usage

    # Create a heading label
    heading_label = tk.Label(root, text="JARVIS A.I. Settings", font=("Bahnschrift Light", 16, "bold", "underline"))
    heading_label.pack(pady=20)

    check_l = tk.Label(root, text="CheckBox Settings :-", font=("Arial Black", 12))
    check_l.pack(pady=10, padx=20, anchor="w")

    # Create a Checkbutton for the first setting
    allowspeaking = tk.IntVar()
    allowspeaking.set(allow_speaking)  # Set default selection
    cbox = tk.Checkbutton(root, text="Allow Jarvis to Speak.", variable=allowspeaking)
    cbox.configure(font=("Arial", 12))
    cbox.pack(pady=10, padx=20, anchor="w")

    # Create a Checkbutton for the second setting
    savequestions = tk.IntVar()
    savequestions.set(save_questions)  # Set default selection
    cbox2 = tk.Checkbutton(root, text="Save the questions answered by the Jarvis.", variable=savequestions)
    cbox2.configure(font=("Arial", 12))
    cbox2.pack(pady=10, padx=20, anchor="w")

    # Create a set of Radiobuttons for the third setting
    inputmethod = tk.IntVar()
    inputmethod.set(input_method)  # Set default selection

    input_l = tk.Label(root, text="I will give my input using :-", font=("Arial Black", 12))
    input_l.pack(pady=10, padx=20, anchor="w")

    radio1 = tk.Radiobutton(root, text="Microphone", variable=inputmethod, value=0)
    radio1.configure(font=("Arial", 12))
    radio1.pack(pady=10, padx=20, anchor="w")

    radio2 = tk.Radiobutton(root, text="Keyboard", variable=inputmethod, value=1)
    radio2.configure(font=("Arial", 12))
    radio2.pack(pady=10, padx=20, anchor="w")

    # Create a Save button
    save_button = tk.Button(root, text="Save", command=save_settings, bg="green", fg="white",
                            activebackground="darkgreen", activeforeground="white", font=("", 16))
    save_button.pack(side="left", padx=10, pady=10)

    # Create an Exit button
    exit_button = tk.Button(root, text="Exit", command=root.destroy, bg="red", fg="white", activebackground="darkred",
                            activeforeground="white", font=("", 16))
    exit_button.pack(side="right", padx=10, pady=10)

    save_button.config(width=15)
    exit_button.config(width=20)
    root.mainloop()

def take_feedback():
    """
    This function takes the Feedback from the user and if needed save the feedback to the feedback.txt
    """
    say("Taking feedback. Please open the Feedback Window.")
    def submit_feedback():
        rating = rating_scale.get()
        feedback = feedback_entry.get("1.0", "end").strip()
        if not feedback:
            tmsg.showerror("Error", "Please provide feedback.")
        else:
            with open("imp_files/feedback.txt", "a") as f:
                f.write(f"{name} rated us: {rating}\nFeedback: {feedback}\n\n")
            feedback_given = True
            tmsg.showinfo("Thank You", "Thank you for your feedback!")
            window.destroy()
    # Create a new Tkinter window
    window = tk.Tk()
    # Set the title of the window
    window.title("Jarvis Feedback")
    # Set the width and height of the window
    window.geometry("350x300")
    # Set the Window icon
    window.iconbitmap("feedback.ico")
    # Rating Scale
    rating_label = tk.Label(window, text="Rate Jarvis (0-5):", font=("Arial", 14))
    rating_label.pack(pady=10)
    rating_scale = tk.Scale(window, from_=1, to=5, orient=tk.HORIZONTAL, font=("Arial", 12), length=200, tickinterval=1,
                            showvalue=False)
    rating_scale.set(3)  # Set initial value to 3
    rating_scale.configure(troughcolor='#D9D9D9', activebackground='#6CAEE0', sliderrelief='raised', sliderlength=15,
                           highlightthickness=0)
    rating_scale.pack(pady=5)
    # Feedback Entry
    feedback_label = tk.Label(window, text="Feedback:", font=("Arial", 14))
    feedback_label.pack()

    feedback_entry = tk.Text(window, height=5, font=("Arial", 12))
    feedback_entry.pack(pady=(0, 10), padx=10)
    # Submit Button
    submit_button = tk.Button(window, text="Submit", command=submit_feedback, font=("Arial", 14), bg="#4CAF50",
                              fg="white", relief=tk.RAISED, padx=10, pady=5)
    submit_button.pack(pady=10)
    # Run the Tkinter event loop
    window.mainloop()

def ai(prompt):
    """
    This function answers the users question and save it into a file
    :param prompt: User's Question
    :return: Jarvis' answer
    """
    # Sending user's question and getting response.
    prompt = prompt.replace("answer ", "")
    ans = jarvis(prompt)
    ans.removeprefix("\n\n")

    if save_questions == 1:
        say("Saving Question")
        # Saving it inside the prompts folder
        if not os.path.exists("prompts"):
            os.makedirs("prompts")

        text = f"Open AI response for: {prompt} \n"
        text += f"{'*' * len(text)}\n\n"
        text += ans
        prompt = remove_invalid_characters(prompt)
        with open(f"prompts/{prompt.replace(' ', '_')}.txt", "w") as f:
            f.write(text)
    say(ans)

# A variable which will store or chats
chatStr = ""

def jarvis(prompt):
    """
    This function answers the prompt using openai
    :param prompt: Question to be answered
    :return: Jarvis' answer
    """
    # Sending user's question and getting response.
    openai.api_key = jarvis_api
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1.02,
        max_tokens=500,
    )
    return response["choices"][0]["text"]

def chat(mess):
    """
    This function helps us to chat with A.I. Jarvis
    :param mess: It's the user's message.
    :return: It returns the Whole Chat + Jarvis reply
    """
    global name
    global chatStr
    if mess == True:
        say("Saving Chat")
        if chatStr != "":
            title = jarvis(f"Chat:\n{chatStr}\nTitle:")
            text = f"Title of the Chat: {title} \n"
            title = remove_invalid_characters(title)
            # Saving it inside the chats folder
            if not os.path.exists("chats"):
                os.makedirs("chats")

            with open(f"chats\{title.replace(' ', '_')[1:]}.txt", "w") as f:
                f.write(f"{text}\n{'*' * len(text+title)}\n\n{chatStr}")
            say("Chat Saved")
            chatStr = ""
        else:
            say("No Chat to Save")
    else:
        chatStr += f"\n{name}: {mess}\nJarvis: "
        ans = jarvis(chatStr)
        chatStr += ans.removeprefix("\n")
        print(chatStr)
        Speak(ans)

if allow_speaking == 0:
    Speak = lambda x: None
    say = lambda text: print(f"\nJarvis Said: {text}")
else:
    import win32com.client

    speaker = win32com.client.Dispatch("SAPI.SpVoice")


    def Speak(text):
        """
        This function helps Jarvis to speak the text
        :param text: to be spoken
        """
        speaker.Speak(text)


    def say(text):
        """
        This function helps Jarvis to speak the text
        :param text: To be spoken
        :return: None
        """
        print(f"\nJarvis Said: {text}")
        Speak(text)

if input_method == 0:
    import speech_recognition as sr

def takeCommand():
    """
    This function uses the microphone to get the user's input
    :return: Returns the text spoken by the user.
    """
    if input_method == 0:
        print("\nListening...")
        # Using Microphone and returning text.
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1.0
            audio = r.listen(source, 0, 10)
            try:
                print("Recognizing...")
                user_command = r.recognize_google(audio, language="en-in")
                print(f"{name} said: {user_command}")
                return user_command
            except Exception:
                say("Sorry Sir, I couldn't listen to you. Please repeat again.")
                return takeCommand()
    else:
        return input("\nEnter your command => ")

if __name__ == '__main__':
    # Intro and asking for name
    say("Introducing Jarvis A.I. 1.0")
    Speak("Sir, May I have  your name")
    name = input("\nEnter your name: ")
    say(f"Welcome {name} !!!")
    while True:
        # Taking User Command
        query = takeCommand()

        # Processes the query
        query = query.lower()

        # Making able to open sites
        sites = {"youtube": "https://www.youtube.com", "wikipedia": "https://www.wikipedia.org",
                 "anvil": "https://anvil.works/", "amazon ": "https://www.amazon.in/", "netflix": "https://www.netflix.com", "facebook": "https://www.facebook.com", "instagram": "https://www.instagram.com", "twitter": "https://twitter.com", "linkedin": "https://www.linkedin.com/", "github": "https://github.com", "stackoverflow": "https://stackoverflow.com/",
                 "google": "https://google.com"}

        site_matched = False
        for site in sites.keys():
            if f"open {site}" in query:
                say(f"Opening {site} Sir..")
                webbrowser.open(sites[site])
                site_matched = True
                break

        if site_matched:
            continue

        # Making able for playing music
        elif "open music" in query:
            say(f"Opening Music Sir..")
            music_dir = r"D:\#Indian_Railways _Announcement_Software\Announcements"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[random.randint(0, len(songs) - 1)]))
        elif "take feedback" in query:
            take_feedback()
        # Answering any question
        elif "answer" in query:
            ai(query)
        # Resetting the Chat
        elif "reset chat" in query:
            chat(True)
            chatStr = ""
            say("Chat has been reset")
        # Saving the Chat
        elif "save our conversation" in query:
            chat(True)
        # For opening settings
        elif "open settings" in query or "open setting" in query:
            open_settings()
            say("Sir If you changed settings, Make sure to restart by exiting and restarting the app.")
        # Exiting the app
        elif "exit" in query.lower():
            if not feedback_given:
                say("Sir please give us your feedback")
                take_feedback()
            say("Exiting...")
            say("Thanks for using Jarvis !!!")
            exit()
        # Chatting
        else:
            chat(query)
