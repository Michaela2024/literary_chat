# Literary Chat 📚

An AI-powered web application that lets you have conversations with characters from classic literature. Using Retrieval-Augmented Generation (RAG) and text-to-speech technology, characters respond based on actual passages from their books with realistic voices.

## ✨ Features

- **RAG-Powered Conversations**: Characters respond based on actual book content using semantic search
- **Natural Voice Synthesis**: Google Cloud Text-to-Speech with character-specific British voices
- **Multiple Classic Books**: 
  - Pride and Prejudice by Jane Austen
  - Frankenstein by Mary Shelley
  - A Christmas Carol by Charles Dickens
- **Interactive Characters**: Chat with Elizabeth Bennet, Mr. Darcy, The Creature, Victor Frankenstein, Scrooge, and more
- **Modern UI**: Clean, responsive interface with real-time messaging
- **Character Avatars**: Visual representation of each character
- **Conversation Management**: Start fresh conversations anytime
- **Automated Testing**: Selenium test suite for core functionality

## 🛠️ Tech Stack

**Backend:**
- Python 3.11
- Django 5.2
- LangChain (RAG implementation)
- FAISS (vector database)
- Google Gemini API (language model)
- Google Cloud Text-to-Speech

**Frontend:**
- HTML5/CSS3
- Vanilla JavaScript
- Modern gradient design

**Testing:**
- Selenium WebDriver
- Python unittest

## 📋 Prerequisites

- Python 3.8 or higher
- Google Cloud account with API access
- Git

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/literary-chat.git
cd literary-chat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies include:
- `django`
- `langchain`
- `langchain-google-genai`
- `langchain-community`
- `langchain-text-splitters`
- `faiss-cpu`
- `google-cloud-texttospeech`
- `python-dotenv`
- `selenium` (for testing)

### 3. Set Up Environment Variables

Create a `.env` file in the project root:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

**Important**: Never commit your `.env` file to version control!

### 4. Get Google API Keys

#### For Gemini API (Language Model):
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API key"
4. Copy the key to your `.env` file

#### Enable Text-to-Speech API:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the [Cloud Text-to-Speech API](https://console.cloud.google.com/apis/library/texttospeech.googleapis.com)
3. The same API key works for both services

**Free Tier Limits:**
- Gemini: Generous free tier for development
- Text-to-Speech: 1 million characters/month (standard voices)

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (for Admin Access)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 7. Start the Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to see the app!

## 📚 Adding Books and Characters

### Via Django Admin

1. Go to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials

### Add a Book

1. Click "Books" → "Add Book"
2. Fill in details:
   - Title, Author, Year
   - Description
   - Upload text file (from Project Gutenberg)
3. Click "Save"
4. **Process for RAG**: 
   - Select the book
   - Choose "Process selected books for RAG" from Actions
   - Click "Go"
   - Wait for processing (creates vector embeddings)

### Add Characters

1. Click "Characters" → "Add Character"
2. Fill in:
   - Book (select from dropdown)
   - Name
   - Description
   - Personality traits
   - Voice (select from available Google TTS voices)
   - Avatar (optional image upload)
3. Click "Save"

**Available Voices:**
- `en-GB-Neural2-A` - British Female (Clear & Professional)
- `en-GB-Neural2-C` - British Female (Warm & Friendly)
- `en-GB-Neural2-F` - British Female (Young & Energetic)
- `en-GB-Neural2-B` - British Male (Deep & Mature)
- `en-GB-Neural2-D` - British Male (Authoritative)

## 🎮 Usage

### Starting a Conversation

1. **Home Page**: Browse available books
2. **Book Page**: Select a character
3. **Chat Interface**: 
   - Type your message
   - Press Enter or click Send
   - Hear the character's response (auto-plays)
   - Click 🔊 to replay audio

### Example Questions to Ask

- "What are your deepest fears?"
- "Tell me about your family"
- "What drives your decisions?"
- "How do you feel about [another character]?"
- "What is your greatest regret?"

### Conversation Management

- **New Chat**: Click "🔄 New Chat" to start fresh
- **Back**: Navigate between books and characters
- **History**: All conversations are saved (until you start a new chat)

## 🧪 Testing

### Run Selenium Tests

Make sure the Django server is running in one terminal:

```bash
python manage.py runserver
```

In another terminal, run tests:

```bash
python test_literarychat_ui.py
```

**Tests Include:**
- Home page loads correctly
- Book selection works
- Character chat interface opens
- Message sending and receiving
- Audio button functionality

## 📁 Project Structure

```
literary-chat/
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── .env                          # Environment variables (not in repo)
├── .env.example                  # Template for environment variables
├── .gitignore                    # Git ignore file
├── README.md                     # This file
├── test_literarychat_ui.py       # Selenium tests
├── books/                        # Main Django app
│   ├── models.py                 # Database models
│   ├── views.py                  # View logic
│   ├── urls.py                   # URL routing
│   ├── admin.py                  # Admin configuration
│   ├── rag_processor.py          # RAG processing logic
│   ├── rag_query.py              # RAG query logic
│   ├── templates/                # HTML templates
│   │   └── books/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── book_detail.html
│   │       └── chat.html
│   └── migrations/               # Database migrations
├── literarychat/                 # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── media/                        # User uploads (not in repo)
│   ├── books/                    # Uploaded book files
│   ├── avatars/                  # Character avatars
│   └── tts_cache/               # Cached audio files
└── vector_stores/                # FAISS indexes (not in repo)
```

## 🔧 How It Works

### RAG (Retrieval-Augmented Generation)

1. **Book Processing**: 
   - Text is split into chunks (~1000 characters)
   - Each chunk is converted to a vector embedding
   - Stored in FAISS vector database

2. **Query Processing**:
   - User's question is converted to a vector
   - Similar chunks are retrieved from the book
   - Retrieved passages provide context to the AI

3. **Response Generation**:
   - Gemini receives the question + relevant passages
   - Generates a character-appropriate response
   - Response is grounded in actual book content

### Text-to-Speech Pipeline

1. Character response is generated
2. Text is cleaned (remove special characters)
3. Sent to Google Cloud TTS with character's voice
4. Audio is cached (MD5 hash of text)
5. Returned to frontend and auto-played

## 🚫 What's NOT Included

The following are excluded via `.gitignore`:
- `.env` (API keys)
- `db.sqlite3` (local database)
- `vector_stores/` (FAISS indexes - regenerated on setup)
- `media/` (user uploads)
- `__pycache__/` and `*.pyc` (Python cache)

## 🐛 Troubleshooting

### "API key not valid"
- Verify your API key in `.env`
- Ensure Text-to-Speech API is enabled in Google Cloud Console
- Check the API key isn't restricted to specific APIs

### "No module named 'langchain'"
```bash
pip install -r requirements.txt
```

### TTS not working
- Verify `GOOGLE_API_KEY` is set correctly
- Check Text-to-Speech API is enabled
- Ensure voice name is valid (e.g., `en-GB-Neural2-A`)

### Characters respond incorrectly
- Verify book was processed for RAG (check admin)
- Ensure vector_stores folder was created
- Try reprocessing the book

## 🎯 Future Enhancements

Potential features for future development:
- [ ] User authentication and conversation history
- [ ] More books and characters
- [ ] Conversation export (PDF, text)
- [ ] Character comparison mode
- [ ] Multi-language support
- [ ] Voice speed and pitch controls
- [ ] Mobile app version

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- **Books**: All texts from [Project Gutenberg](https://www.gutenberg.org/)
- **AI Model**: Google Gemini 2.0 Flash
- **Text-to-Speech**: Google Cloud Text-to-Speech
- **RAG Framework**: LangChain
- **Vector Database**: FAISS (Facebook AI Similarity Search)


Built as a hobby portfolio project demonstrating AI, RAG, full-stack development, and modern web design. 🚀
