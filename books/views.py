from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.conf import settings
from .models import Book, Character, Conversation, Message
from .rag_query import query_character
from google.cloud import texttospeech
from pathlib import Path
import hashlib
import uuid

def home(request):
    """Display all available books"""
    books = Book.objects.filter(is_processed=True)
    return render(request, 'books/home.html', {'books': books})

def book_detail(request, book_id):
    """Display characters from a specific book"""
    book = get_object_or_404(Book, id=book_id, is_processed=True)
    characters = book.characters.all()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'characters': characters
    })

def chat(request, character_id):
    """Chat interface with a character"""
    character = get_object_or_404(Character, id=character_id)
    
    # Get or create session ID
    session_id = request.session.get('session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['session_id'] = session_id
    
    # Get or create conversation
    conversation, created = Conversation.objects.get_or_create(
        character=character,
        user_session=session_id
    )
    
    # Get message history
    messages = conversation.messages.all().order_by('timestamp')
    
    return render(request, 'books/chat.html', {
        'character': character,
        'conversation': conversation,
        'messages': messages
    })

def generate_speech_audio(text, character, conversation_id):
    """
    Generate speech audio using Google Cloud TTS.
    """
    try:
        # Clean the text before generating speech
        cleaned_text = text.replace('*', '')  # Remove asterisks
        cleaned_text = cleaned_text.replace('_', '')  # Remove underscores
        cleaned_text = cleaned_text.replace('"', '')  # Remove quotes
        cleaned_text = cleaned_text.replace("'", '')  # Remove apostrophes in quotes
        cleaned_text = ' '.join(cleaned_text.split())  # Normalize whitespace
        
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
        
        # Use character's voice from database, with fallback
        voice_name = character.voice if hasattr(character, 'voice') and character.voice else "en-GB-Neural2-A"
        
        # Determine gender from voice name
        is_female_voice = any(letter in voice_name for letter in ['A', 'C', 'F'])
        gender = texttospeech.SsmlVoiceGender.FEMALE if is_female_voice else texttospeech.SsmlVoiceGender.MALE
        
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-GB",
            name=voice_name,
            ssml_gender=gender
        )
        
        print(f"🎙️ Using voice: {voice_name} for {character.name}")
        
        # Set the text input with cleaned text
        synthesis_input = texttospeech.SynthesisInput(text=cleaned_text)
        
        # Select audio format
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3,
            speaking_rate=0.95,
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
        
        print(f"✅ Generated TTS audio for {character.name}")
        
        return f"media/tts_cache/{audio_filename}"
        
    except Exception as e:
        print(f"❌ TTS Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return Nonepty

def send_message(request, conversation_id):
    """Handle sending a message and getting response"""
    if request.method == 'POST':
        conversation = get_object_or_404(Conversation, id=conversation_id)
        user_message = request.POST.get('message', '').strip()
        
        if not user_message:
            return JsonResponse({'error': 'Message cannot be empty'}, status=400)
        
        # Save user message
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message
        )
        
        # 
        # Get character response
        character_response = query_character(
            conversation.character,
            user_message
        )
        
        # Save character response
        Message.objects.create(
            conversation=conversation,
            role='character',
            content=character_response
        )
        
        # Generate TTS audio
        audio_url = generate_speech_audio(
            character_response,
            conversation.character,
            conversation_id
        )
        
        avatar_url = conversation.character.avatar.url if conversation.character.avatar else None

        return JsonResponse({
            'user_message': user_message,
            'character_response': character_response,
            'audio_url': audio_url,
            'avatar_url': avatar_url
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def delete_conversation(request, conversation_id):
    """Delete a conversation and start fresh"""
    if request.method == 'POST':
        try:
            conversation = get_object_or_404(Conversation, id=conversation_id)
            character_id = conversation.character.id
            
            # Delete the conversation (messages are deleted automatically via CASCADE)
            conversation.delete()
            
            # Clear the session
            if 'session_id' in request.session:
                del request.session['session_id']
            
            return JsonResponse({
                'success': True,
                'redirect_url': f'/chat/{character_id}/'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)