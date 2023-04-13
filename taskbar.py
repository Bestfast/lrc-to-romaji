# Import necessary modules
from pystray import Icon, Menu, MenuItem
from PIL import Image
import subprocess
import transliterate
import logging

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
fh = logging.FileHandler('taskbar.log', encoding='utf-8')
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

# Initialize streamlit_process variable
streamlit_process = None

# Define on_transliterate function to handle transliteration


def on_transliterate(icon, item):
    logger.info("Transliterate button clicked")
    # Call transliterate function from transliterate module
    transliterate.transliterate_last_accessed_file(
        r"C:\Users\Bestfast\AppData\Roaming\foobar2000-v2\lyrics")

# Define on_edit function to handle editing


def on_edit(icon, item):
    logger.info("Edit clicked")
    # Start Streamlit server here
    global streamlit_process
    if streamlit_process is not None:
        logger.info("Streamlit server already running, terminating")
        streamlit_process.terminate()
    streamlit_process = subprocess.Popen(["streamlit", "run", "streamlit.py"])

# Define on_quit function to handle quitting the application


def on_quit(icon, item):
    global streamlit_process
    # Terminate Streamlit process if it exists
    if streamlit_process is not None:
        logger.info("Terminating running Streamlit server")
        streamlit_process.terminate()
    # Stop the icon
    icon.stop()


# Load icon image
image = Image.open("icon.ico")

# Create menu with Transliterate, Edit and Quit options
menu = Menu(
    MenuItem("Transliterate", on_transliterate),
    MenuItem("Edit", on_edit),
    MenuItem("Quit", on_quit)
)

# Create icon with Test title, image and menu
icon = Icon("Test", image, "Test App", menu)

logger.info("Starting tray icon")

# Run the icon
icon.run()
