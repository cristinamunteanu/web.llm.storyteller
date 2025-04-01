# Web LLM Storyteller

Web LLM Storyteller is a web application that generates short stories in Romanian, converts them to audio using Text-to-Speech (TTS), and creates child-friendly cartoon-style illustrations based on the story. Users can also replay or stop the audio playback.

---

## Features

- **Story Generation**: Generates short stories in Romanian using OpenAI's GPT-3.5-turbo model.
- **Text-to-Speech (TTS)**: Converts the generated story into audio using the `edge_tts` library with the `ro-RO-AlinaNeural` voice.
- **Image Generation**: Creates cartoon-style, child-friendly illustrations based on the story using OpenAI's image generation API.
- **Audio Playback Controls**: Includes buttons to play, stop, and replay the audio.
- **Child-Friendly Design**: Focuses on creating content suitable for small children.

---

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript
- **APIs**:
  - OpenAI GPT-3.5-turbo for story generation
  - OpenAI Image API for illustration generation
- **Text-to-Speech**: `edge_tts` library
- **Audio Playback**: `mpg123` (Linux), `afplay` (macOS), or `playsound` (Windows)

---

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (set as an environment variable: `OPENAI_API_KEY`)
- `mpg123` installed (for Linux audio playback):
  ```bash
  sudo apt update
  sudo apt install mpg123

---

### Clone the Repository

```bash
git clone https://github.com/your-repo/web-llm-storyteller.git
cd web-llm-storyteller
```

### Install Dependencies

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your_openai_api_key"
```

### Run the Application

Start the Flask server:

```bash
python app.py
```

The application will be available at `http://127.0.0.1:5000`.

---

## Usage

### Generate a Story

1. Enter a prompt in the input field in Romanian (e.g., "O padure magica").
2. Click the "Generate Story" button.
3. The app will generate a short story in Romanian.

### Listen to the Story

- The story will be converted to audio and played automatically.
- Use the "Stop Playing" button to stop the audio.
- Use the "Replay Audio" button to replay the audio.

### View the Illustration

- A cartoon-style, child-friendly illustration based on the story will be displayed below the text.

---

## Project Structure

```
web-llm-storyteller/
├── static/
│   └── output.mp3          # Generated audio file
├── templates/
│   └── index.html          # Main HTML template
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Key Functions

### Story Generation

- **Function**: `generate_story(prompt)`
- **Description**: Generates a short story in Romanian using OpenAI's GPT-3.5-turbo model.

### Image Generation

- **Function**: `generate_image(prompt)`
- **Description**: Creates a cartoon-style, child-friendly illustration based on the story.

### Text-to-Speech

- **Function**: `generate_tts(story)`
- **Description**: Converts the generated story into audio using the `edge_tts` library.

### Audio Playback

- **Functions**:
  - `play_audio()`: Plays the generated audio file.
  - `stop_audio()`: Stops the audio playback.
  - `speak_story(story)`: Combines TTS and audio playback.

---

## Known Issues

- **Audio Playback**: Ensure `mpg123` is installed on Linux systems for audio playback.
- **Image Quality**: The generated images depend on the OpenAI model's capabilities and may vary in quality.

---

## Future Improvements

- Add support for more languages in story generation and TTS.
- Enhance the cartoon-style illustration prompts for better results.
- Implement a progress bar for audio playback.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Acknowledgments

- [OpenAI](https://openai.com/) for GPT-3.5-turbo and image generation APIs.
- [edge_tts](https://github.com/rany2/edge-tts) for Text-to-Speech functionality.
```

---