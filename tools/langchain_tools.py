from langchain.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field

from tools.gmail_tools import GmailFetcher
from tools.audit_logger import AuditLogger
from agent.email_agent import EmailCleanupAgent
from schemas.decision import EmailDecision


class FetchPromotionalEmailsInput(BaseModel):
    query: str = Field(
        default="category:promotions older_than:2d",
        description="Gmail search query"
    )
    max_results: int = Field(default=3)


class FetchPromotionalEmailsTool(BaseTool):
    name = "fetch_promotional_emails"
    description = "Fetch promotional emails from Gmail"
    args_schema: Type[BaseModel] = FetchPromotionalEmailsInput

    def __init__(self, gmail_fetcher: GmailFetcher):
        super().__init__()
        self.gmail = gmail_fetcher

    def _run(self, query: str, max_results: int):
        emails = self.gmail.fetch_emails(query=query, max_results=max_results)
        return emails


class DecideEmailsInput(BaseModel):
    emails: list = Field(description="List of email contexts")


class DecideEmailsTool(BaseTool):
    name = "decide_emails"
    description = "Decide whether each email should be deleted"
    args_schema: Type[BaseModel] = DecideEmailsInput

    def __init__(self, agent: EmailCleanupAgent):
        super().__init__()
        self.agent = agent

    def _run(self, emails: list):
        decisions = []

        for email in emails:
            decision = self.agent.decide(email)
            decisions.append({
                "email": email,
                "decision": decision.model_dump(),
            })

        return decisions

    class DecideEmailsInput(BaseModel):
        emails: list = Field(description="List of email contexts")

    class DecideEmailsTool(BaseTool):
        name = "decide_emails"
        description = "Decide whether each email should be deleted"
        args_schema: Type[BaseModel] = DecideEmailsInput

        def __init__(self, agent: EmailCleanupAgent):
            super().__init__()
            self.agent = agent

        def _run(self, emails: list):
            decisions = []

            for email in emails:
                decision = self.agent.decide(email)
                decisions.append({
                    "email": email,
                    "decision": decision.model_dump(),
                })

            return decisions


class LogDecisionsInput(BaseModel):
    decisions: list = Field(description="Email decisions to log")


class LogDecisionsTool(BaseTool):
    name = "log_decisions"
    description = "Log email cleanup decisions for auditing"
    args_schema: Type[BaseModel] = LogDecisionsInput

    def __init__(self, audit_logger: AuditLogger):
        super().__init__()
        self.logger = audit_logger

    def _run(self, decisions: list):
        for item in decisions:
            email = item["email"]
            decision = EmailDecision(**item["decision"])

            self.logger.log(
                email_id=email["id"],
                sender=email["from"],
                subject=email["subject"],
                decision=decision,
            )

        return f"Logged {len(decisions)} decisions"


