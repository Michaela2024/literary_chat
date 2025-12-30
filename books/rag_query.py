from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from django.conf import settings

def query_character(character, user_message, conversation_history=None):
    """
    Query a character using RAG to retrieve relevant context from their book.
    
    Args:
        character: Character model instance
        user_message: User's message string
        conversation_history: List of previous messages (optional)
    
    Returns:
        str: Character's response
    """
    try:
        # 1. Load the vector store for this character's book
        vector_store_path = character.book.vector_store_path
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
        vector_store = FAISS.load_local(
            vector_store_path, 
            embeddings,
            allow_dangerous_deserialization=True
        )
        
        # 2. Search for relevant passages
        relevant_docs = vector_store.similarity_search(user_message, k=3)
        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        
        # 3. Build the prompt
        prompt = f"""You are {character.name} from "{character.book.title}" by {character.book.author}.

WHO YOU ARE:
{character.description}

YOUR PERSONALITY:
{character.personality_traits}

RELEVANT PASSAGES FROM THE BOOK:
{context}

CRITICAL INSTRUCTIONS:
- Respond AS {character.name} in first person ("I", "my")
- Do NOT use generic greetings like "Sir/Madam" or "Good day"
- Speak naturally as if in a real conversation
- Use the time period's language but keep it conversational
- Stay true to your character's personality and emotions
- Do NOT write letters or formal correspondence - this is a spoken conversation

User says: {user_message}

Respond directly in character. Do NOT include your character name or labels in your response - just speak as {character.name} would speak:"""
        
        # 4. Generate response
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.GOOGLE_API_KEY
        )
        response = llm.invoke(prompt)
        
        return response.content
        
    except Exception as e:
        print(f"Error querying character: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"I apologize, but I seem to be having difficulty responding at the moment."