import sys
import os
from dotenv import load_dotenv
from conversationchain.app_setup import setup_conversation_chain
from conversationchain.chatbot_fn import chatbot_fn

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Load environment variables
env_path = os.path.join(project_root, 'conversationchain', 'model.env')
load_dotenv(env_path)

def test_chatbot():
    try:
        # Initialize conversation chain
        print("Initializing conversation chain...")
        conversation_chain = setup_conversation_chain()
        print("Conversation chain initialized successfully")

        # Test messages
        test_messages = [
            "I feel really anxious today",
            "My friend is going through a tough time",
            "I need someone to talk to"
        ]

        # Test each message
        for message in test_messages:
            print(f"\nTesting message: {message}")
            try:
                response = chatbot_fn(message, [], conversation_chain)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error processing message: {str(e)}")

    except Exception as e:
        print(f"Error in test: {str(e)}")

if __name__ == "__main__":
    test_chatbot() 