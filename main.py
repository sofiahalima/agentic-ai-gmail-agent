from llm.claude_client import ClaudeClient
from llm.open_llm_client import OpenLLMClient
from llm.llm_router import LLMRouter
from agent.email_agent import EmailCleanupAgent
from tools.audit_logger import AuditLogger
from tools.gmail_tools import GmailFetcher

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

SYSTEM_PROMPT = """
You are an autonomous email cleanup agent.

Your task:
1. Fetch promotional emails from Gmail
2. Decide whether each email should be deleted
3. Log all decisions for auditing

Rules:
- Be conservative: when unsure, choose UNSURE
- NEVER delete receipts, banking, travel, or work emails
- You must process emails in batches
- You must always log your decisions

You run autonomously without user input.
"""


if __name__ == "__main__":

    claude = ClaudeClient(
        model="claude-3-haiku-20240307"
    )

    open_llm = OpenLLMClient(
        model="mistral"
    )

    llm = LLMRouter(
        primary_llm=claude,
        fallback_llm=open_llm
    )

    #Agent
    agent = EmailCleanupAgent(llm)

    # Tools
    gmail = GmailFetcher()
    logger = AuditLogger()

    # Fetch emails (SAFE QUERY)
    emails = gmail.fetch_emails(
        query="category:promotions older_than:30d",
        max_results=10,
    )

    for email in emails:
        decision = agent.decide(email)
        print("\n---")
        print(f"From: {email['from']}")
        print(f"Subject: {email['subject']}")
        print(f"Decision: {decision.decision} ({decision.confidence})")
        print(f"Reason: {decision.reason}")

        logger.log(
            email_id=email["id"],
            sender=email["from"],
            subject=email["subject"],
            decision=decision,
        )
