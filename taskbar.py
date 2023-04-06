# Import necessary modules
from pystray import Icon, Menu, MenuItem
from PIL import Image
import subprocess
import transliterate

# Initialize streamlit_process variable
streamlit_process = None

# Define on_transliterate function to handle transliteration
def on_transliterate(icon, item):
    print("Transliterate clicked")
    # Call transliterate function from transliterate module
    transliterate.transliterate_last_accessed_file(r"C:\Users\Bestfast\AppData\Roaming\foobar2000-v2\lyrics")

# Define on_edit function to handle editing
def on_edit(icon, item):
    print("Edit clicked")
    # Start Streamlit server here
    global streamlit_process
    streamlit_process = subprocess.Popen(["streamlit", "run", "streamlit.py"])

# Define on_quit function to handle quitting the application
def on_quit(icon, item):
    global streamlit_process
    # Terminate Streamlit process if it exists
    if streamlit_process is not None:
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

# Run the icon
icon.run()