from abc import ABC, abstractmethod
from schemas.decision import EmailDecision


class BaseAgent(ABC):
    def __init__(self, llm_client):
        self.llm = llm_client

    @abstractmethod
    def decide(self, email_context: dict) -> EmailDecision:
        pass
