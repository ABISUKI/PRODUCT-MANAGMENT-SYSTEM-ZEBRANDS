import threading
from typing import List

from google.cloud.firestore_v1.watch import DocumentChange
from api.ports.db_port_interface import DBMainInterface


class Listener:
    def __init__(self,  db: DBMainInterface):
        self.db = db

    @classmethod
    def listening(
        cls,
        changes: List[DocumentChange]
    ) -> None:
        """Logic to update dictionary based on changes in the db

        Args:
            changes (List[DocumentChange]):
        """
        for change in changes:
            if change.type.name == "MODIFIED":
                print(f"Modified!: {change.document.id}")

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
