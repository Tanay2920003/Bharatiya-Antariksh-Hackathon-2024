

import os
import pyaudio
import queue
import threading
from google.cloud import speech
from geopy.geocoders import Nominatim
import spacy

# Set up environment variable for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "hybrid-sunbeam-429814-a0-7aae21dccd0b.json"

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
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

def extract_cities(text):
        nlp = spacy.load("en_core_web_sm")
        try:
            doc = nlp(text)
            geolocator = Nominatim(user_agent="geoapiExercises")

            cities = []
            for ent in doc.ents:
                if ent.label_ == "GPE":
                    location = geolocator.geocode(ent.text)
                    if location:
                        cities.append(ent.text)
            return cities
        except PermissionError as e:
            print(f"Permission error: {e}")
def listen_print_loop(responses, language_code):
    """Iterates through server responses and prints them."""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        cities = extract_cities(transcript)
        print("Cities found:", cities)


def main():
    client = speech.SpeechClient()

    # Create configurations for both languages

    config_in = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-IN"
    )

    streaming_config_in = speech.StreamingRecognitionConfig(
        config=config_in,
        interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()

        # Create requests for both configurations
        requests_in = (speech.StreamingRecognizeRequest(audio_content=content)
                       for content in audio_generator)

        # Create threads for both language configurations
        response_thread_in = threading.Thread(
            target=listen_print_loop,
            args=(client.streaming_recognize(streaming_config_in, requests_in), "en-IN")
        )
        response_thread_in.start()

        try:
            response_thread_in.join()
        except KeyboardInterrupt:
            print("Interrupted by user")

    # Confirm installation and functionality
    print("Finished")


if __name__ == "__main__":
    main()
