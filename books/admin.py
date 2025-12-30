from django.contrib import admin
from .models import Book, Character, Conversation, Message

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'is_processed', 'created_at')
    list_filter = ('is_processed', 'author')
    search_fields = ('title', 'author')
    readonly_fields = ('is_processed', 'vector_store_path', 'created_at')
    actions = ['process_books_for_rag']
    
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'publication_year', 'description')
        }),
        ('Files', {
            'fields': ('text_file', 'cover_image')
        }),
        ('Processing Status', {
            'fields': ('is_processed', 'vector_store_path', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    
    def process_books_for_rag(self, request, queryset):
        """Admin action to process selected books for RAG"""
        from .rag_processor import process_book_for_rag
        
        success_count = 0
        errors = []
        
        for book in queryset:
            try:
                if process_book_for_rag(book):
                    success_count += 1
                else:
                    errors.append(f"{book.title}: Processing failed")
            except Exception as e:
                errors.append(f"{book.title}: {str(e)}")
        
        if success_count > 0:
            self.message_user(
                request, 
                f"Successfully processed {success_count} of {queryset.count()} books."
            )
        
        if errors:
            for error in errors:
                self.message_user(request, f"ERROR: {error}", level='ERROR')
    
    process_books_for_rag.short_description = "Process selected books for RAG"

@admin.register(Character)
class CharacterAdmin(admin.ModelAdmin):
    list_display = ('name', 'book', 'voice')  # Changed from voice_name
    list_filter = ('book',)
    search_fields = ('name', 'book__title')
    
    fieldsets = (
        ('Character Information', {
            'fields': ('book', 'name', 'description', 'personality_traits')
        }),
        ('Voice Settings', {
            'fields': ('voice',),  # Changed from voice_name
            'description': 'Google TTS voice options: en-GB-Neural2-A (clear female), en-GB-Neural2-C (warm female), en-GB-Neural2-F (young female), en-GB-Neural2-B (deep male), en-GB-Neural2-D (authoritative male)'
        }),
        ('Avatar', {
            'fields': ('avatar',)
        }),
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('character', 'user_session', 'created_at')
    list_filter = ('character__book', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'role', 'content_preview', 'timestamp')
    list_filter = ('role', 'timestamp')
    readonly_fields = ('timestamp',)
    
    def content_preview(self, obj):
        return obj.content[:100] + "..." if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content'