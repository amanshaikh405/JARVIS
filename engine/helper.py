import os
import re
import threading
import time
import markdown2
from bs4 import BeautifulSoup
import sys
import os
import shutil
import sqlite3
import shutil

def extract_yt_term(command):
    # Define a regular expression pattern to capture the song name
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    # Use re.search to find the match in the command
    match = re.search(pattern, command, re.IGNORECASE)
    # If a match is found, return the extracted song name; otherwise, return None
    return match.group(1) if match else None


def remove_words(input_string, words_to_remove):
    # Split the input string into words
    words = input_string.split()

    # Remove unwanted words
    filtered_words = [word for word in words if word.lower() not in words_to_remove]

    # Join the remaining words back into a string
    result_string = ' '.join(filtered_words)

    return result_string



# key events like receive call, stop call, go back
def keyEvent(key_code):
    command =  f'adb shell input keyevent {key_code}'
    os.system(command)
    time.sleep(1)

# Tap event used to tap anywhere on screen
def tapEvents(x, y):
    command =  f'adb shell input tap {x} {y}'
    os.system(command)
    time.sleep(1)

# Input Event is used to insert text in mobile
def adbInput(message):
    command =  f'adb shell input text "{message}"'
    os.system(command)
    time.sleep(1)

# to go complete back
def goback(key_code):
    for i in range(6):
        keyEvent(key_code)

# To replace space in string with %s for complete message send
def replace_spaces_with_percent_s(input_string):
    return input_string.replace(' ', '%s')

def markdown_to_text(md):
    html = markdown2.markdown(md)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text().strip()

def resource_path(relative_path):
    """
    Get absolute path to resource (PyInstaller compatible)
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

DB_NAME = "jarvis.db"
_lock = threading.Lock()
_connection = None


def get_db_path():
    base_dir = os.path.join(
        os.path.expanduser("~"),
        "Documents",
        "Jarvis"
    )
    os.makedirs(base_dir, exist_ok=True)

    db_path = os.path.join(base_dir, DB_NAME)

    if not os.path.exists(db_path):
        with _lock:   # 🔥 CRITICAL
            if not os.path.exists(db_path):  # double check
                if hasattr(sys, "_MEIPASS"):
                    source = os.path.join(sys._MEIPASS, DB_NAME)
                else:
                    source = os.path.abspath(
                        os.path.join(os.path.dirname(__file__), "..", DB_NAME)
                    )

                if not os.path.exists(source):
                    raise FileNotFoundError(f"Source DB not found: {source}")

                shutil.copy2(source, db_path)

    return db_path

def fix_porcupine_dll_path():
    if hasattr(sys, "_MEIPASS"):
        dll_path = os.path.join(
            sys._MEIPASS,
            "pvporcupine",
            "lib",
            "windows",
            "amd64"
        )
        os.environ["PATH"] += os.pathsep + dll_path
        print("Porcupine DLL path added:", dll_path)
