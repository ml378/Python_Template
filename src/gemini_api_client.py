from __future__ import annotations

import importlib
import os
import uuid
from typing import TYPE_CHECKING, Any, Protocol

import requests
from dotenv import load_dotenv

from src.ai_interface import IAIConversationClient
from src.conversation import Conversation, Message, MessageRole

# overall concern: why use requests if we can use the SDK's methods directly? future todo. We also keep self sessions but also gemini chat sessions. 

if TYPE_CHECKING:

    class GenerativeModelConstructor(Protocol):
        def __call__(self, model_name: str) -> Any: ...  # noqa: ANN401
        def start_chat(self, history: list[Any]) -> Any: ...  # noqa: ANN401
else:
    GenerativeModelConstructor = Any

# dynamic import
genai = importlib.import_module("google.generativeai")
genai_configure: Any = genai.configure
genai_model_class: GenerativeModelConstructor = genai.GenerativeModel

load_dotenv()


class GeminiAPIClient(IAIConversationClient):
    """GeminiAPIClient is an implementation of IAIConversationClient that interfaces with Google's Gemini 2.0 API to handle AI chat interactions.

    It manages sessions, messages, user preferences, and generates assistant responses.
    """

    def __init__(self) -> None:
        """Initialize the GeminiAPIClient.

        Loads the Gemini API key from the environment, configures the SDK,
        and prepares model and session tracking.
        """
        self._api_key = os.getenv("GEMINI_API_KEY")

        if not self._api_key:
            msg = "Missing GEMINI_API_KEY in .env file"
            raise ValueError(msg)

        genai_configure(api_key=self._api_key)
        self._model: Any = genai_model_class("gemini-2.0-flash")

        self._model_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={self._api_key}"
        )

        self._chat_sessions: dict[str, Any] = {}
        self._sessions: dict[str, Conversation] = {}
        self._user_preferences: dict[str, dict[str, Any]] = {}

    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        """Send a message from the user and return the AI's response.

        Args:
            session_id (str): The unique identifier for the session.
            message (str): The user's message content.

        Returns:
            dict: Contains the assistant's message with ID, role, content, and timestamp.

        Raises:
            ValueError: If the session ID is not found.
            RuntimeError: If the Gemini API call fails.

        """
        if session_id not in self._sessions:
            msg = "Session not found"
            raise ValueError(msg)

        convo = self._sessions[session_id]
        convo.add_message(Message(message, MessageRole.USER))

        history = "\n".join(
            f"{msg.role.value.capitalize()}: {msg.content}" for msg in convo.messages
        )

        payload = {"contents": [{"parts": [{"text": history}]}]}
        headers = {"Content-Type": "application/json"}

        try:
            # add a timeout to prevent indefinite hanging
            response = requests.post(self._model_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            parsed = response.json()
            text = parsed["candidates"][0]["content"]["parts"][0]["text"].strip()
            assistant_msg = Message(text, MessageRole.ASSISTANT)
            convo.add_message(assistant_msg)

            return {
                "message_id": assistant_msg.id,
                "role": assistant_msg.role.value,
                "content": assistant_msg.content,
                "timestamp": assistant_msg.timestamp.isoformat(),
            }
        except Exception as e:
            msg = f"Gemini API error: {e}"
            raise RuntimeError(msg) from e

    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]:
        """Return the full chat history for a given session.

        Args:
            session_id (str): The unique identifier for the session.

        Returns:
            list[dict]: List of message dictionaries with ID, role, content, and timestamp.

        """
        if session_id not in self._sessions:
            return []

        return [
            {
                "message_id": m.id,
                "role": m.role.value,
                "content": m.content,
                "timestamp": m.timestamp.isoformat(),
            }
            for m in self._sessions[session_id].messages
        ]

    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """Store user-specific preferences (e.g., system prompt).

        Args:
            user_id (str): The unique identifier for the user.
            preferences (dict): A dictionary of user preferences.

        Returns:
            bool: Always returns True.

        """
        self._user_preferences[user_id] = preferences
        return True

    def start_new_session(self, user_id: str) -> str:
        """Start a new conversation session for a user.

        Args:
            user_id (str): The user's unique ID.

        Returns:
            str: The generated session ID.

        """
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        prompt = self._user_preferences.get(user_id, {}).get("system_prompt")
        convo = Conversation(conversation_id=session_id, system_prompt=prompt)
        self._sessions[session_id] = convo
        self._chat_sessions[session_id] = self._model.start_chat(history=[])
        return session_id

    def end_session(self, session_id: str) -> bool:
        """End and clean up a session.

        Args:
            session_id (str): The ID of the session to end.

        Returns:
            bool: Always returns True.

        """
        self._sessions.pop(session_id, None)
        self._chat_sessions.pop(session_id, None)
        return True
