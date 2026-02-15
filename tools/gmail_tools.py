from __future__ import annotations

import os.path
from typing import List, Dict

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# READ-ONLY scope (VERY IMPORTANT)
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GmailFetcher:
    def __init__(self, credentials_path: str = "credentials.json"):
        self.creds = None
        self.credentials_path = credentials_path
        self.service = self._authenticate()

    def _authenticate(self):
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file(
                "token.json", SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        return build("gmail", "v1", credentials=self.creds)

    def fetch_emails(
        self,
        query: str,
        max_results: int = 3,
    ) -> List[Dict]:
        """
        Fetch emails matching Gmail search query.
        Returns simplified email contexts.
        """
        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                q=query,
                maxResults=max_results,
            )
            .execute()
        )

        messages = results.get("messages", [])
        emails = []

        for msg in messages:
            full_msg = (
                self.service.users()
                .messages()
                .get(
                    userId="me",
                    id=msg["id"],
                    format="metadata",
                    metadataHeaders=["From", "Subject", "List-Unsubscribe"],
                )
                .execute()
            )

            emails.append(self._parse_message(full_msg))

        return emails

    def trash_email(self, message_id: str):
        try:
            self.service.users().messages().trash(
                userId="me",
                id=message_id
            ).execute()

            print(f"Moved to trash: {message_id}")

        except Exception as e:
            print(f"Error trashing {message_id}: {e}")

    @staticmethod
    def _parse_message(message: Dict) -> Dict:
        headers = {
            h["name"]: h["value"]
            for h in message["payload"]["headers"]
        }

        return {
            "id": message["id"],
            "from": headers.get("From", ""),
            "subject": headers.get("Subject", ""),
            "snippet": message.get("snippet", ""),
            "headers": list(headers.keys()),
        }
