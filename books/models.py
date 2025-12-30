from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    text_file = models.FileField(upload_to='books/')
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    vector_store_path = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"

class Character(models.Model):
    VOICE_CHOICES = [
        ('en-GB-Neural2-A', 'British Female - Clear & Professional'),
        ('en-GB-Neural2-C', 'British Female - Warm & Friendly'),
        ('en-GB-Neural2-F', 'British Female - Young & Energetic'),
        ('en-GB-Neural2-B', 'British Male - Deep & Mature'),
        ('en-GB-Neural2-D', 'British Male - Authoritative'),
        ('en-US-Neural2-A', 'American Female - Clear'),
        ('en-US-Neural2-C', 'American Female - Warm'),
        ('en-US-Neural2-D', 'American Male - Deep'),
        ('en-US-Neural2-J', 'American Male - Casual'),
    ]
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='characters')
    name = models.CharField(max_length=200)
    description = models.TextField()
    personality_traits = models.TextField()
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    voice = models.CharField(
        max_length=50,
        choices=VOICE_CHOICES,
        
        help_text='Google TTS voice for this character'
    )
    
    def __str__(self):
        return f"{self.name} from {self.book.title}"

class Conversation(models.Model):
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    user_session = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat with {self.character.name}"

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20)  # 'user' or 'character'
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.role}: {self.content[:50]}"