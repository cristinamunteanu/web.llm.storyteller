import threading
import time
from flask import Flask, render_template, request, url_for
from openai import OpenAI
import edge_tts
import asyncio
from gtts import gTTS
import subprocess
import platform
from playsound import playsound
import os
import shutil
import base64

app = Flask(__name__)

# Save the audio file to the static folder
audio_file = os.path.join("static", "output.mp3")

# Ensure the static folder exists
if not os.path.exists("static"):
    os.makedirs("static")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

DEBUG = False  # Set this to True to enable debug logs, False to disable

def log_debug(message):
    if DEBUG:
        print(message)

def generate_story(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a storyteller writing a short story in Romanian language. The story must have a clear beginning, middle, and ending. The ending should resolve the story and leave the reader satisfied."},
                {"role": "user", "content": "Scrie o poveste scurtă despre: " + prompt},
            ],
            max_tokens=750,
            temperature=0.5
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Eroare la generarea poveștii: {str(e)}"

def generate_image(prompt):
    try:
        # Modify the prompt to make it more child-friendly and cartoon-like
        cartoon_prompt = f"A cartoon-style, child-friendly illustration of: {prompt}"
        log_debug(f"Generating image for prompt: {cartoon_prompt}")  # Debug log
        response = client.images.generate(
            prompt=cartoon_prompt,
            n=1,  # Number of images to generate
            size="512x512"  # Image size
        )
        # Access the URL from the response correctly
        image_url = response.data[0].url
        log_debug(f"Generated image URL: {image_url}")  # Debug log
        return image_url
    except Exception as e:
        log_debug(f"Error generating image: {e}")
        return None

# The below code uses the edge_tts module to generate a Romanian TTS audio file using the AlinaNeural voice.
async def generate_tts(story):
    try:
        tts = edge_tts.Communicate(text=story, voice="ro-RO-AlinaNeural")
        await tts.save(audio_file)
        log_debug(f"TTS audio saved to {audio_file}")
    except Exception as e:
        log_debug(f"Error generating TTS: {e}")

# Global variable to track the audio playback process
audio_process = None

def play_audio():
    global audio_process
    try:
        # Check if mpg123 is installed
        if shutil.which("mpg123") is None:
            raise FileNotFoundError("mpg123 is not installed. Please install it to play audio.")

        # Use subprocess to play the audio file
        if platform.system() == "Windows":
            audio_process = subprocess.Popen(["start", audio_file], shell=True)
        elif platform.system() == "Darwin":  # macOS
            audio_process = subprocess.Popen(["afplay", audio_file])
        else:  # Linux
            audio_process = subprocess.Popen(["mpg123", audio_file])
        audio_process.wait()
    except Exception as e:
        log_debug(f"Error playing audio: {e}")
    finally:
        #cleanup()
        pass

def stop_audio():
    global audio_process
    if audio_process and audio_process.poll() is None:  # Check if the process is running
        log_debug("Terminating audio process")  # Debug log
        audio_process.terminate()  # Terminate the audio playback process
        audio_process = None
    else:
        log_debug("No audio process to terminate")  # Debug log

def speak_story(story):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(generate_tts(story))
    loop.close()
    play_audio()

def cleanup():
    if os.path.exists(audio_file):
        os.remove(audio_file)


@app.route('/', methods=['GET', 'POST'])
def home():
    story = ''
    image_url = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        story = generate_story(prompt)
        # Generate an image based on the story
        image_prompt = f"An artistic representation of the following story: {story[:200]}"
        image_url = generate_image(image_prompt)
        # Start speaking thread
        speak_thread = threading.Thread(target=speak_story, args=(story,))
        speak_thread.start()
    return render_template('index.html', story=story, image_url=image_url, audio_url=url_for('static', filename='output.mp3'))

@app.route('/stop_audio', methods=['POST'])
def stop_audio_route():
    log_debug("Stop audio route called")  # Debug log
    stop_audio()
    return '', 204  # Return a 204 No Content response

@app.route('/replay_audio', methods=['POST'])
def replay_audio_route():
    try:
        play_audio()  # Replay the audio
        return '', 204  # Return a 204 No Content response
    except Exception as e:
        log_debug(f"Error replaying audio: {e}")
        return '', 500  # Return a 500 Internal Server Error response

if __name__ == "__main__":
    app.run(debug=True)
