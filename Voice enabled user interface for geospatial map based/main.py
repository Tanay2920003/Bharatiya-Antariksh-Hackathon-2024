from google.cloud import speech_v1p1beta1 as speech

def transcribe_audio(audio_file_path):
    with open(audio_file_path, 'rb') as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',  # Change to your desired language
    )
    client = speech.SpeechClient.from_service_account_json('C:/Users/Tanay/Desktop/Bharatiya-Antariksh-Hackathon-2024/Voice enabled user interface for geospatial map based/hybrid-sunbeam-429814-a0-7aae21dccd0b.json')
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

# Example usage:

transcribe_audio('C:/Users/Tanay/Downloads/audio.mp3')

