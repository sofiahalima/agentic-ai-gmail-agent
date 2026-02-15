import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()


class ClaudeClient:
    def __init__(self,
                 model: str = "claude-3-haiku-20240307",
                 max_tokens: int = 512,
                 temperature: float = 0.2,
                 ):
        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise RuntimeError("API key not set")

        self.client = Anthropic(api_key=api_key)
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.model = model

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generate a response from the claude
        """
        messages = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_prompt,
                }
            ],
        )
        return self._extract_text(messages)

    @staticmethod
    def _extract_text(message):
        """
       Claude messages contain a list of content blocks.
       We concatenate all text blocks.
       """
        parts = []
        for block in message.content:
            if block.type == "text":
                parts.append(block.text)
        return " ".join(parts).strip()
