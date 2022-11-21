from dependency_injector import containers, providers

from api.ports.firestore.db_main import DBMainFirestore


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["api.adapters.rest.users", "api.adapters.rest.products"])
    db_firestore = providers.Factory(DBMainFirestore)
