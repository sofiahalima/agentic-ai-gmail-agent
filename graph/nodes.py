from graph.state import EmailGraphState
from tools.gmail_tools import GmailFetcher
from tools.audit_logger import AuditLogger
from schemas.decision import EmailDecision
from utils.slack_alert import send_slack_alert


def build_nodes(agent, logger):
    gmail = GmailFetcher()
    audit_logger = AuditLogger()

    def fetch_emails_node(state: EmailGraphState):
        emails = gmail.fetch_emails(
            query="in:inbox older_than:30d",
            max_results=20,
        )

        return {
            **state,
            "emails": emails,
        }

    def decide_node(state: EmailGraphState):
        decisions = []
        print(f"Deciding on {len(state['emails'])} emails")

        for email in state["emails"]:
            decision = agent.decide(email)

            decisions.append({
                "email": email,
                "decision": decision.model_dump(),
            })

        return {
            **state,
            "decisions": decisions,
        }

    def delete_node(state: EmailGraphState):
        deleted_count = 0
        protected_count = 0
        proposed_deletes = 0

        PROTECTED_KEYWORDS = [
            "invoice",
            "receipt",
            "bank",
            "statement",
            "payment",
            "booking",
            "flight",
            "order",
            "confirmation",
            "otp",
            "verification",
        ]

        for item in state["decisions"]:
            action = item["decision"]["decision"]
            confidence = item["decision"]["confidence"]

            if action == "DELETE":
                proposed_deletes += 1

            # subject = item["email"]["subject"].lower()
            # if any(keyword in subject for keyword in PROTECTED_KEYWORDS):
            #     item["decision"]["decision"] = "UNSURE"
            #     protected_count += 1
            #     continue

                if confidence >= 0.80:
                    gmail.trash_email(item["email"]["id"])
                    deleted_count += 1

                else:
                    # Override low-confidence delete
                    item["decision"]["decision"] = "UNSURE"
                    protected_count += 1

        logger.info(f"LLM proposed {proposed_deletes} deletes")
        logger.info(f"Deleted {deleted_count} emails")
        logger.info(f"Protected {protected_count} low-confidence deletes")

        return {
            **state,
            "stats": {
                "proposed": proposed_deletes,
                "deleted": deleted_count,
                "protected": protected_count,
            }
        }

    def log_node(state: EmailGraphState):
        for item in state["decisions"]:
            email = item["email"]
            decision = EmailDecision(**item["decision"])

            audit_logger.log(
                email_id=email["id"],
                sender=email["from"],
                subject=email["subject"],
                decision=decision,
            )

        logger.info(f"Logged {len(state['decisions'])} decisions")

        return state

    def summary_node(state: EmailGraphState):

        keep = 0
        unsure = 0

        for item in state["decisions"]:
            decision = item["decision"]["decision"]

            if decision == "KEEP":
                keep += 1
            elif decision == "UNSURE":
                unsure += 1

        total = len(state["decisions"])
        stats = state.get("stats", {})

        logger.info("===== RUN SUMMARY =====")
        logger.info(f"Total processed: {total}")
        logger.info(f"LLM proposed deletes: {stats.get('proposed', 0)}")
        logger.info(f"Deleted: {stats.get('deleted', 0)}")
        logger.info(f"Protected: {stats.get('protected', 0)}")
        logger.info(f"Keep: {keep}")
        logger.info(f"Unsure: {unsure}")
        logger.info("=======================")
        send_slack_alert(f"==== RUN SUMMARY ===== Total processed: {total} LLM proposed deletes: {stats.get('proposed', 0)}")


        return state

    return fetch_emails_node, decide_node, delete_node, log_node, summary_node
