import os
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from django.conf import settings

def process_book_for_rag(book):
    """
    Process a book to create RAG vector store.
    
    Args:
        book: Book model instance
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # 1. Read the book text
        file_path = book.text_file.path
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        print(f"📚 Processing: {book.title}")
        print(f"📄 Text length: {len(text)} characters")
        
        # 2. Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)
        print(f"✂️ Created {len(chunks)} chunks")
        
        # 3. Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/embedding-001",
            google_api_key=settings.GOOGLE_API_KEY
        )
        
        # 4. Create vector store
        print("🔢 Creating vector store...")
        vector_store = FAISS.from_texts(chunks, embeddings)
        
        # 5. Save vector store
        vector_store_dir = Path(settings.BASE_DIR) / "vector_stores"
        vector_store_dir.mkdir(exist_ok=True)
        
        vector_store_path = vector_store_dir / f"book_{book.id}"
        vector_store.save_local(str(vector_store_path))
        
        # 6. Update book record
        book.vector_store_path = str(vector_store_path)
        book.is_processed = True
        book.save()
        
        print(f"✅ Successfully processed {book.title}")
        print(f"💾 Vector store saved to: {vector_store_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error processing book: {str(e)}")
        import traceback
        print(f"❌ Error processing book: {str(e)}")
        print("Full traceback:")
        traceback.print_exc()
        return False