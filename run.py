import sys
import os

if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")

if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")


def startJarvis():
    """Main UI + Eel process (MUST be main process)"""
    print("Jarvis UI starting...")
    from main import start
    start()


def listenHotword():
    """Background hotword listener"""
    print("Hotword listener starting...")
    from engine.features import hotword
    hotword()


if __name__ == "__main__":
    import multiprocessing

    multiprocessing.freeze_support()

    # Start hotword in background process
    hotword_process = multiprocessing.Process(
        target=listenHotword,
        daemon=True
    )
    hotword_process.start()

    # Run Eel / UI in main process
    startJarvis()

    # Cleanup
    if hotword_process.is_alive():
        hotword_process.terminate()
        hotword_process.join()

    print("System stopped")
