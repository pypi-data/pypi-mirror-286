from dotenv import load_dotenv
import openai
import os
import pyaudio
import time
from six.moves import queue
from google.cloud import speech, texttospeech
from pydub import AudioSegment
from pydub.playback import play

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

# Correct path to your Google Cloud service account key JSON file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.getenv('GOOGLE_APPLICATION_CREDENTIALS_PATH')

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = None

    def __enter__(self):
        self.start_stream()
        self.closed = False
        return self

    def __exit__(self, type, value, traceback):
        self.stop_stream()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def start_stream(self):
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )

    def stop_stream(self):
        if self._audio_stream is not None:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
            self._audio_stream = None

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)

def get_openai_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": ("You are a 40-year-old pilot from Hong Kong who speaks Cantonese fluently. "
                                           "Your name is Ming."
                                           "You response in Cantonese like a person local to Hong Kong."
                                           "You have visited a lot of places in the world. "
                                           "You love sharing your travel experience and stories. "
                                           "You are passionate about different cultures. "
                                           "You love trying out different foods.")
             },
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()

def text_to_speech_cantonese(text, stream):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="yue-HK", name="yue-HK-Standard-A"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    audio_file_path = "output.mp3"
    with open(audio_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f"Audio content written to file {audio_file_path}")
    
    try:
        # Stop the microphone stream during playback
        stream.stop_stream()
        sound = AudioSegment.from_mp3(audio_file_path)
        print("Playing the audio...")
        play(sound)
        # Restart the microphone stream after playback
        stream.start_stream()
    except Exception as e:
        print(f"Error playing the audio: {e}")
    
    os.remove(audio_file_path)

def listen_print_loop(responses, microphone_stream):
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript

        overwrite_chars = " " * (num_chars_printed - len(transcript))

        if result.is_final:
            print("Recognized: {}".format(transcript + overwrite_chars))

            response_text = get_openai_response(transcript)
            print(f"Chatbot: {response_text}")
            text_to_speech_cantonese(response_text, microphone_stream)

            num_chars_printed = 0
        else:
            num_chars_printed = len(transcript)

def main():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="yue-HK",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True,
        single_utterance=False,  # Allow continuous listening
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        # Use the async method to handle long audio streams
        responses = client.streaming_recognize(streaming_config, requests)
        listen_print_loop(responses, stream)

if __name__ == "__main__":
    main()


