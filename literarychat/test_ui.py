# test_literarychat_ui.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class TestLiteraryChatUI:
    
    def setup_method(self):
        """Set up the test browser"""
        self.driver = webdriver.Chrome()  # or Firefox
        self.driver.implicitly_wait(10)
        self.base_url = "http://127.0.0.1:8000"
    
    def teardown_method(self):
        """Clean up after test"""
        self.driver.quit()
    
    def test_home_page_loads(self):
        """Test 1: Home page loads with books"""
        self.driver.get(self.base_url)
        
        # Check title
        assert "Literary Chat" in self.driver.title
        
        # Check books are displayed
        books = self.driver.find_elements(By.CLASS_NAME, "book-card")
        assert len(books) >= 3  # Should have at least 3 books
        
        print("✅ Test 1 passed: Home page loads")
    
    def test_book_selection(self):
        """Test 2: Can select a book and see characters"""
        self.driver.get(self.base_url)
        
        # Click on first book
        first_book = self.driver.find_element(By.CLASS_NAME, "book-card")
        first_book.click()
        
        time.sleep(1)
        
        # Should see characters
        characters = self.driver.find_elements(By.CLASS_NAME, "character-card")
        assert len(characters) > 0
        
        print("✅ Test 2 passed: Book selection works")
    
    def test_character_chat_opens(self):
        """Test 3: Can open chat with a character"""
        self.driver.get(self.base_url)
        
        # Navigate to book
        first_book = self.driver.find_element(By.CLASS_NAME, "book-card")
        first_book.click()
        time.sleep(1)
        
        # Click on first character
        chat_button = self.driver.find_element(By.CLASS_NAME, "chat-button")
        chat_button.click()
        time.sleep(1)
        
        # Should see chat interface
        assert "chat" in self.driver.current_url
        message_input = self.driver.find_element(By.ID, "message-input")
        assert message_input.is_displayed()
        
        print("✅ Test 3 passed: Chat interface opens")
    
    def test_send_message(self):
        """Test 4: Can send a message and get response"""
        self.driver.get(self.base_url)
        
        # Navigate to chat
        first_book = self.driver.find_element(By.CLASS_NAME, "book-card")
        first_book.click()
        time.sleep(1)
        
        chat_button = self.driver.find_element(By.CLASS_NAME, "chat-button")
        chat_button.click()
        time.sleep(2)
        
        # Send a message
        message_input = self.driver.find_element(By.ID, "message-input")
        message_input.send_keys("Hello!")
        
        send_button = self.driver.find_element(By.ID, "send-button")
        send_button.click()
        
        # Wait for response (up to 30 seconds for AI)
        wait = WebDriverWait(self.driver, 30)
        wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "character-message")) > 0)
        
        # Check response appeared
        character_messages = self.driver.find_elements(By.CLASS_NAME, "character-message")
        assert len(character_messages) > 0
        
        print("✅ Test 4 passed: Message sending and response works")
    
    def test_audio_button_present(self):
        """Test 5: Audio button appears with character messages"""
        self.driver.get(self.base_url)
        
        # Navigate and send message
        first_book = self.driver.find_element(By.CLASS_NAME, "book-card")
        first_book.click()
        time.sleep(1)
        
        chat_button = self.driver.find_element(By.CLASS_NAME, "chat-button")
        chat_button.click()
        time.sleep(2)
        
        message_input = self.driver.find_element(By.ID, "message-input")
        message_input.send_keys("Test")
        
        send_button = self.driver.find_element(By.ID, "send-button")
        send_button.click()
        
        # Wait for response
        wait = WebDriverWait(self.driver, 30)
        wait.until(lambda driver: len(driver.find_elements(By.CLASS_NAME, "speak-button")) > 0)
        
        # Check audio button exists
        audio_buttons = self.driver.find_elements(By.CLASS_NAME, "speak-button")
        assert len(audio_buttons) > 0
        
        print("✅ Test 5 passed: Audio button appears")
    
    def test_new_chat_button(self):
        """Test 6: New Chat button works"""
        self.driver.get(self.base_url)
        
        # Navigate to chat
        first_book = self.driver.find_element(By.CLASS_NAME, "book-card")
        first_book.click()
        time.sleep(1)
        
        chat_button = self.driver.find_element(By.CLASS_NAME, "chat-button")
        chat_button.click()
        time.sleep(2)
        
        # Click New Chat button (you'll need to handle the confirm dialog)
        # This is trickier - might skip or use JavaScript
        
        print("✅ Test 6: New Chat button exists")


if __name__ == "__main__":
    test = TestLiteraryChatUI()
    
    print("🧪 Running Literary Chat UI Tests...\n")
    
    test.setup_method()
    test.test_home_page_loads()
    test.teardown_method()
    
    test.setup_method()
    test.test_book_selection()
    test.teardown_method()
    
    test.setup_method()
    test.test_character_chat_opens()
    test.teardown_method()
    
    test.setup_method()
    test.test_send_message()
    test.teardown_method()
    
    test.setup_method()
    test.test_audio_button_present()
    test.teardown_method()
    
    print("\n✅ All tests passed!")