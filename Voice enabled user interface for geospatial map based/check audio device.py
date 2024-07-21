import os
import pyaudio
import queue
from google.cloud import speech
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label

# Set up environment variable for authentication
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:/Users/Tanay/Desktop/Bharatiya-Antariksh-Hackathon-2024/Voice enabled user interface for geospatial map based/hybrid-sunbeam-429814-a0-7aae21dccd0b.json"

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

class MicrophoneStream:
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk, device_index=None):
        self._rate = rate
        self._chunk = chunk
        self._device_index = device_index

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
            input_device_index=self._device_index
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

def listen_print_loop(responses):
    """Iterates through server responses and prints them."""
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        print(f'Transcript: {transcript}')

def main(device_index):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    with MicrophoneStream(RATE, CHUNK, device_index) as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content)
                    for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        listen_print_loop(responses)

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        dropdown = DropDown()
        p = pyaudio.PyAudio()
        self.device_index = None

        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            btn = Button(text=info['name'], size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: dropdown.select(btn.text))
            dropdown.add_widget(btn)

        mainbutton = Button(text='Select Input Device', size_hint=(None, None), height=44)
        mainbutton.bind(on_release=dropdown.open)
        dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))

        start_button = Button(text='Start Transcription', size_hint=(None, None), height=44)
        start_button.bind(on_release=self.start_transcription)

        layout.add_widget(Label(text='Choose your microphone device'))
        layout.add_widget(mainbutton)
        layout.add_widget(start_button)

        return layout

    def start_transcription(self, instance):
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            if info['name'] == instance.text:
                self.device_index = i
                break

        main(self.device_index)

if __name__ == '__main__':
    MyApp().run()
