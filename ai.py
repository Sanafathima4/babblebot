import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import save
load_dotenv()
def text_to_speech_elevenlabs(text: str, voice_id: str, output_filename: str):
    """
    Converts text to speech using the ElevenLabs API and saves it to a file.

    Args:
        text (str): The text to be converted to speech.
        voice_id (str): The ID of the voice to use for the speech.
        output_filename (str): The name of the file to save the audio to (e.g., "output.mp3").
    """
    # Initialize the ElevenLabs client.
    # The API key is automatically loaded from the ELEVENLABS_API_KEY environment variable.
    # If the environment variable is not set, you can pass it directly:
    # client = ElevenLabs(api_key="YOUR_API_KEY")
    client = ElevenLabs(api_key=os.getenv('ELEVENLABS_API_KEY'))

    try:
        # Generate the audio from the text
        audio = client.text_to_speech.convert(
            text=text,
            voice_id='uq8azAkk0wBebQXhvpc8', # You can choose a different model
        model_id= "eleven_turbo_v2_5"  # Specify the model to use
        )

        # Save the audio to the specified file
        save(audio, output_filename)
        print(f"Audio saved to {output_filename}")
        

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    # You can find a list of available voice IDs in your ElevenLabs dashboard
    # or by using the client.voices.get_all() method.
    example_text = "Ooh! [giggle] Hi there! I'm Lala! Woah, sorry about that! I'm just a little bit clumsy, hehe! [giggles some more]."
    example_voice_id = "JBFqnCBsd6RMkjVDRZzb"  # Replace with a valid voice ID
    example_output_file = "elevenlabs_output.mp3"

    text_to_speech_elevenlabs(example_text, example_voice_id, example_output_file)