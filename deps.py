import os
import firebase_admin
from firebase_admin import credentials, firestore
from dependency_injector import containers, providers

from api.ports.firestore.db_users import DBMainFirestore


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.adapters.rest.products"])
    db_firestore = providers.Factory(DBMainFirestore)
