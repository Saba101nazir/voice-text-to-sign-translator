import speech_recognition as sr
import numpy as np
import cv2
from easygui import *
import os
import string
import tkinter as tk

def display_video(video_path, highlight_text):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return

    # Define window size 
    window_width = 640
    window_height = 480

    # Get the screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position for the center of the screen
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Resize frame to fit the window
        frame = cv2.resize(frame, (window_width, window_height))

        # Add text overlay to highlight the spoken word or alphabet
        cv2.putText(frame, f'You Said: {highlight_text}', (10, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)  # White color, smaller font

        cv2.imshow('Video', frame)
        cv2.moveWindow('Video', x, y)  # Move window to the center of the screen
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_speech():
    r = sr.Recognizer()
    dataset_folder = 'assets'
    spoken_text = ""  # Initialize spoken_text at the beginning

    def process_audio(audio):
        nonlocal spoken_text  # Access the outer spoken_text variable
        try:
            spoken_text = r.recognize_google(audio)  # Recognize audio without timeout
            spoken_text = spoken_text.lower()
            print('You Said:', spoken_text)
            
            for c in string.punctuation:
                spoken_text = spoken_text.replace(c, "")

            words = spoken_text.split()

            for word in words:
                # ANSI escape codes for text formatting
                highlight_color = '\033[92m'  # Green color
                end_color = '\033[0m'  # Reset color

                print(f'I am Listening: {highlight_color}{word}{end_color}')

                video_file = f'{word}.mp4'
                video_path = os.path.join(dataset_folder, video_file)
                if os.path.exists(video_path):
                    display_video(video_path, word)
                else:
                    for char in word:
                        if char.isalpha():
                            alpha_video = f'{char.lower()}.mp4'
                            alpha_path = os.path.join(dataset_folder, alpha_video)
                            if os.path.exists(alpha_path):
                                display_video(alpha_path, char)
                            else:
                                print(f"Video file not found for alphabet: {char}")

        except sr.UnknownValueError:
            print("Speech Recognition could not understand audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)  # Shorter duration for faster adjustment

        while True:
            print("I am Listening")
            audio = r.listen(source)  # Listen without timeout
            process_audio(audio)

            if 'goodbye' in spoken_text or 'good bye' in spoken_text or 'bye' in spoken_text:
                print("Oops! Time to say goodbye")
                break

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    msg = "DIALOGIX ASSISTANT"
    choices = ["Live Voice", "All Done!"]

    while True:
        reply = buttonbox(msg, choices=choices)

        if reply == choices[0]:
            recognize_speech()
        elif reply == choices[1]:
            quit()
