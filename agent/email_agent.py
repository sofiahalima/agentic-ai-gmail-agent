from agent.base_agent import BaseAgent
from schemas.decision import EmailDecision
import json


class EmailCleanupAgent(BaseAgent):
    SYSTEM_PROMPT = """
        You are an email-cleanup agent.
        
        Your task:
        - Identify unwanted emails.
        - Be conservative: when unsure, choose UNSURE.
        - NEVER delete from following category : receipts, banking, tickets, educational, LinkedIn
        - check for mails with adds and Unsubscribe options but not in above listed category
        - check for mails with no reply options but not in above listed category
        - check for mails with big images in the body
        - emails with special characters in subject
        
        
        Return ONLY valid JSON matching this schema:
        {
          "decision": "DELETE | KEEP | UNSURE",
          "confidence": 0.0-1.0,
          "reason": "short explanation",
          "signals": ["list", "of", "signals"]
        }
    """

    def decide(self, email_context: dict) -> EmailDecision:
        prompt = self._build_prompt(email_context)

        raw_response = self.llm.generate(
            system_prompt=self.SYSTEM_PROMPT,
            user_prompt=prompt
        )

        try:
            data = json.loads(raw_response)
            return EmailDecision(**data)
        except Exception as e:
            # Fail-safe: never delete if parsing fails
            return EmailDecision(
                decision="UNSURE",
                confidence=0.0,
                reason=f"Parsing error: {str(e)}",
                signals=["llm_error"]
            )

    def _build_prompt(self, email_context: dict) -> str:
        return f"""
            Analyze the following email:
            
            Sender: {email_context.get("from")}
            Subject: {email_context.get("subject")}
            Snippet: {email_context.get("snippet")}
            Headers: {email_context.get("headers")}
            
            Decide whether this email should be deleted.
            """
