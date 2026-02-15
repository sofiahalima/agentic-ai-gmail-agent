import csv
import os
from datetime import datetime
from schemas.decision import EmailDecision


class AuditLogger:
    def __init__(self, path: str = "audit_log.csv"):
        self.path = path
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.path):
            with open(self.path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp",
                    "email_id",
                    "sender",
                    "subject",
                    "decision",
                    "confidence",
                    "reason",
                    "signals",
                ])

    def log(self, email_id: str, sender: str, subject: str, decision: EmailDecision):
        with open(self.path, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.utcnow().isoformat(),
                email_id,
                sender,
                subject,
                decision.decision,
                decision.confidence,
                decision.reason,
                ";".join(decision.signals),
            ])
