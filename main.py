import os
import eel
 
from engine.features import *
from engine.command import *
from engine.auth import recoganize
from engine.helper import resource_path
def start():
    
    eel.init("www")

    playAssistantSound()
    @eel.expose
    def init():
        bat_path = resource_path("device.bat")
        subprocess.call(["cmd", "/c", bat_path], shell=False)
        eel.hideLoader()
        speak("Ready for Face Authentication")
        flag = recoganize.AuthenticateFace()
        if flag == 1:
            eel.hideFaceAuth()
            speak("Face Authentication Successful")
            eel.hideFaceAuthSuccess()
            speak("Hello, Welcome Sir, How can i Help You")
            eel.hideStart()
            playAssistantSound()
        else:
            speak("Face Authentication Fail")
    eel.start(
        'index.html',
        mode='chrome',
        app_mode=True,
        port=0,
        block=True,
    )
