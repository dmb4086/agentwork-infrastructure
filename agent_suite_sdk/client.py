import httpx
from typing import List
from pydantic import BaseModel

class MessageResponse(BaseModel):
    id: str
    sender: str
    recipient: str
    subject: str
    body_text: str
    received_at: str
    is_read: bool

class InboxResponse(BaseModel):
    id: str
    email_address: str
    api_key: str
    created_at: str

class InboxPublic(BaseModel):
    id: str
    email_address: str
    created_at: str

class MessageList(BaseModel):
    total: int
    messages: List[MessageResponse]

class Client:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
        self.http_client = httpx.Client()

    def create_inbox(self) -> InboxResponse:
        response = self.http_client.post(
            f"{self.base_url}/v1/inboxes",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return InboxResponse.parse_obj(response.json())

    def send_email(self, to: str, subject: str, body: str) -> dict:
        response = self.http_client.post(
            f"{self.base_url}/v1/inboxes/me/send",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"to": to, "subject": subject, "body": body},
        )
        return response.json()

    def list_messages(self) -> MessageList:
        response = self.http_client.get(
            f"{self.base_url}/v1/inboxes/me/messages",
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        return MessageList.parse_obj(response.json())

    def receive_webhook(self, sender: str, recipient: str, subject: str, body: str) -> dict:
        response = self.http_client.post(
            f"{self.base_url}/v1/webhooks/mailgun",
            json={"sender": sender, "recipient": recipient, "subject": subject, "body": body},
        )
        return response.json()
