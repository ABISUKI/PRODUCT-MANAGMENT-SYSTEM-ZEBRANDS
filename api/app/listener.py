import os
import threading
from typing import List

import requests
from google.cloud.firestore_v1.watch import DocumentChange
from api.ports.db_port_interface import DBMainInterface


class Listener:
    def __init__(self,  db: DBMainInterface):
        self.db = db

    def notify_product_changes(self, email: str, user_name: str, product_id: str):
        email_template = self.db.get(collection="email-templates", document_id="product_change")
        template = {
            "sender": {
                "name": "   Neftali Tapia",
                "email": "senderalex@example.com"
            },
            "to": [
                {
                    "email": email,
                    "name": user_name
                }
            ],
            "subject": f"Product Change! ID: {product_id}",
            "htmlContent": email_template.get("template", "<html><head></head><body><p>Hello, </p>Some product has been changed!.</p></body></html>")
        }
        try:
            response = requests.post("https://api.sendinblue.com/v3/smtp/email",
                              headers={"Content-Type": "application/json",
                                       "api-key": os.getenv("SENDIBLUE_API_KEY")},
                              json=template)
            print("Notifier status: ", response.status_code)
        except Exception as error:
            print(f"Error trying to notify product changes to the users: {error}")

    def listening(
        self,
        changes: List[DocumentChange]
    ) -> None:
        """Logic to update dictionary based on changes in the db

        Args:
            changes (List[DocumentChange]):
        """
        for change in changes:
            if change.type.name == "MODIFIED":
                print(f"Modified!: {change.document.id}")
                all_user_documents = self.db.get_all("users")
                destination = [(doc.get("email"), doc.get("names")) for doc in all_user_documents if doc]
                for x in destination:
                    self.notify_product_changes(email=x[0], user_name=x[1], product_id=change.document.id)
                
    def get_real_time_data(self) -> None:
        """Listen change in real time to update dictionary."""
        client = self.db.get_db_client()
        _ = threading.Event()

        def on_snapshot(col_snapshot, changes, read_time):
            print("Callback received query snapshot.")
            print(f"Current data: {read_time}")
            self.listening(changes)

        query = client.collection("products")
        _ = query.on_snapshot(on_snapshot)
