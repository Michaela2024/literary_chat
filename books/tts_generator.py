from google.cloud import texttospeech
from django.conf import settings
import os
import hashlib
from pathlib import Path

CHARACTER_VOICE_SETTINGS = {
    # A Christmas Carol
    "ebenezer scrooge": {"name": "en-GB-Neural2-D", "gender": "MALE", "pitch": -4.0, "speaking_rate": 0.85},
    "bob cratchit": {"name": "en-GB-Neural2-B", "gender": "MALE", "pitch": 0.0, "speaking_rate": 1.0},
    "ghost of christmas past": {"name": "en-GB-Neural2-A", "gender": "FEMALE", "pitch": 2.0, "speaking_rate": 0.9},
    "ghost of christmas present": {"name": "en-GB-Neural2-D", "gender": "MALE", "pitch": -2.0, "speaking_rate": 1.05},
    
    # Pride and Prejudice
    "elizabeth bennet": {"name": "en-GB-Neural2-A", "gender": "FEMALE", "pitch": 1.0, "speaking_rate": 1.0},
    "mr darcy": {"name": "en-GB-Neural2-D", "gender": "MALE", "pitch": -2.0, "speaking_rate": 0.9},
    "mrs bennet": {"name": "en-GB-Neural2-C", "gender": "FEMALE", "pitch": 2.0, "speaking_rate": 1.15},
    
    # Frankenstein
    "victor frankenstein": {"name": "en-GB-Neural2-B", "gender": "MALE", "pitch": -1.0, "speaking_rate": 0.95},
    "the creature": {"name": "en-GB-Neural2-D", "gender": "MALE", "pitch": -6.0, "speaking_rate": 0.8},
}

# Default voices
DEFAULT_FEMALE = {"name": "en-GB-Neural2-A", "gender": "FEMALE", "pitch": 0.0, "speaking_rate": 1.0}
DEFAULT_MALE = {"name": "en-GB-Neural2-B", "gender": "MALE", "pitch": 0.0, "speaking_rate": 1.0}

def generate_speech_audio(text, character_name, conversation_id):
    try:
        # Handle list response from new Gemini model
        if isinstance(text, list):
            text = ' '.join(item.get('text', '') for item in text if isinstance(item, dict) and item.get('type') == 'text')
        
        cleaned_text = text.replace('*', '')
        
        # Create cache directory
        cache_dir = Path(settings.MEDIA_ROOT) / 'tts_cache'
        cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Create unique filename based on text hash
        text_hash = hashlib.md5(cleaned_text.encode()).hexdigest()
        audio_filename = f"{text_hash}.mp3"
        audio_path = cache_dir / audio_filename
        
        # Return cached file if it exists
        if audio_path.exists():
            return f"media/tts_cache/{audio_filename}"
        
        # Initialize TTS client
        client = texttospeech.TextToSpeechClient(
            client_options={"api_key": settings.GOOGLE_API_KEY}
        )
        
        # Look up character voice settings
        char_key = character_name.lower().strip()
        if char_key in CHARACTER_VOICE_SETTINGS:
            char_voice = CHARACTER_VOICE_SETTINGS[char_key]
        else:
            is_female = any(name in char_key for name in ['elizabeth', 'jane', 'lydia', 'mary', 'kitty', 'mrs'])
            char_voice = DEFAULT_FEMALE if is_female else DEFAULT_MALE
        
        gender_enum = (texttospeech.SsmlVoiceGender.FEMALE 
                      if char_voice["gender"] == "FEMALE" 
                      else texttospeech.SsmlVoiceGender.MALE)
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB",
            name=char_voice["name"],
            ssml_gender=gender_enum
        )
        
        # Set the text input
        synthesis_input = texttospeech.SynthesisInput(text=cleaned_text)
        
        # Audio config with character-specific pitch and rate
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=char_voice["speaking_rate"],
            pitch=char_voice["pitch"]
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
        
        print(f"🎙️ Using voice: {char_voice['name']} (pitch: {char_voice['pitch']}, rate: {char_voice['speaking_rate']}) for {character_name}")
        
        return f"media/tts_cache/{audio_filename}"
        
    except Exception as e:
        print(f"TTS Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return None