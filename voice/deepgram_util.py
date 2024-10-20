import os
from dotenv import load_dotenv
from pydub import AudioSegment
from pydub.playback import play

from deepgram import (
    DeepgramClient,
    SpeakOptions,
)

load_dotenv()

SPEAK_OPTIONS = {"text": "What are good places to visit in SF?"}
filename = "output.wav"


def speak(text, gender):
    deepgram = DeepgramClient(api_key=os.getenv("DG_API_KEY"))

    # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
    options = SpeakOptions(
        model='aura-asteria-en' if gender == 'female' else 'aura-orpheus-en',
        encoding='linear16',
        container='wav'
    )

    # STEP 3: Call the save method on the speak property
    response = deepgram.speak.v("1").save(filename, {"text": text}, options)
    audio = AudioSegment.from_wav(filename)
    audio = audio.speedup(playback_speed=1.1)
    play(audio)

def main():
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key=os.getenv("DG_API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        audio = AudioSegment.from_wav(filename)
        play(audio)
        print(response.to_json(indent=4))

    except Exception as e:
        print(f"Exception: {e}")


if __name__ == "__main__":
    main()