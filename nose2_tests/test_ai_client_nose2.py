import unittest

from src.ai_client import AIConversationClient
from tests.dummy_api_client import DummyAPIClient


class TestAIClient(unittest.TestCase):
    """Test suite for AIConversationClient class using nose2."""

    def setUp(self) -> None:
        """Set up a test client before each test."""
        api = DummyAPIClient()
        self.client = AIConversationClient(api_client=api)

    def test_send_message(self) -> None:
        """Test sending a message returns expected response."""
        session_id = self.client.start_new_session("test_user")
        response = self.client.send_message(session_id, "Hello")
        self.assertIsInstance(response, dict)
        self.assertIn("content", response)

    def test_get_chat_history(self) -> None:
        """Test retrieving chat history after sending a message."""
        session_id = self.client.start_new_session("test_user")
        self.client.send_message(session_id, "Hello")
        history = self.client.get_chat_history(session_id)
        self.assertIsInstance(history, list)
        self.assertEqual(len(history), 2)  # user + assistant

    def test_set_user_preferences(self) -> None:
        """Test setting user preferences."""
        result = self.client.set_user_preferences("user_1", {"theme": "dark"})
        self.assertTrue(result)

    def test_start_new_session(self) -> None:
        """Test starting a new session."""
        session_id = self.client.start_new_session("user_2")
        self.assertTrue(session_id.startswith("session_"))

    def test_end_session(self) -> None:
        """Test ending a session."""
        session_id = self.client.start_new_session("user_3")
        self.assertTrue(self.client.end_session(session_id))


if __name__ == "__main__":
    unittest.main()
