from google.cloud import texttospeech
from django.conf import settings
import os
import hashlib
from pathlib import Path

def generate_speech_audio(text, character_name, conversation_id):
    """
    Generate speech audio using Google Cloud TTS.
    
    Args:
        text: Text to convert to speech
        character_name: Name of character (for voice selection)
        conversation_id: ID for caching
    
    Returns:
        str: Path to generated audio file
    """
    try:
        # Create cache directory
        cache_dir = Path(settings.MEDIA_ROOT) / 'tts_cache'
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique filename based on text hash
        text_hash = hashlib.md5(text.encode()).hexdigest()
        audio_filename = f"{text_hash}.mp3"
        audio_path = cache_dir / audio_filename
        
        # Return cached file if it exists
        if audio_path.exists():
            return f"media/tts_cache/{audio_filename}"
        
        # Initialize TTS client
        client = texttospeech.TextToSpeechClient(
            client_options={"api_key": settings.GOOGLE_API_KEY}
        )
        
        # Select voice based on character
        is_female = any(name in character_name.lower() 
                       for name in ['elizabeth', 'bennet', 'jane', 'lydia', 'mary', 'kitty'])
        
        if is_female:
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-GB",
                name="en-GB-Neural2-A",  # Female British voice
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
        else:
            voice = texttospeech.VoiceSelectionParams(
                language_code="en-GB",
                name="en-GB-Neural2-B",  # Male British voice
                ssml_gender=texttospeech.SsmlVoiceGender.MALE
            )
        
        # Set the text input
        synthesis_input = texttospeech.SynthesisInput(text=text)
        
        # Select audio format
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.95,  # Slightly slower for elegance
            pitch=0.0
        )
        
        # Generate speech
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        # Save audio file
        with open(audio_path, 'wb') as out:
            out.write(response.audio_content)
        
        return f"media/tts_cache/{audio_filename}"
        
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None