import time

from pydantic import ValidationError
from firebase_admin import firestore
from google.cloud.firestore import DocumentReference, Transaction, DocumentSnapshot
from api.app.entities.exceptions import ProductModelError, ProductNotUpdated, DataNotFoundError
from api.app.entities.input_models import ProductsUpdateInput, UserCreationInput, ProductsCreationInput, \
    ProductDeleteInput
from api.app.entities.persistence_models import ProductsPersistenceModel
from api.ports.db_port_interface import DBMainInterface


class Products:
    def __init__(self, db: DBMainInterface):
        self.db = db
        self.__products_collection = "products"

    @staticmethod
    def generate_sku(model: str, brand: str, name: str):
        sku = name[:-4] + "-" + brand + "-" + model
        return sku.upper()

    @staticmethod
    def doc_model(
            doc_id: str,
            serial_number: str,
            model: str,
            brand: str,
            price: float,
            name: str,
            sku: str,

    ) -> dict:
        time_ = int(time.time() * 1000)
        return ProductsPersistenceModel(
            id=doc_id,
            serial_number=serial_number,
            name=name,
            model=model,
            brand=brand,
            price=price,
            sku=sku,
            created_at=time_,
            updated_at=time_
        ).dict()

    def add_product(self, product_creation_input: ProductsCreationInput) -> dict:

        document_data = self.doc_model(doc_id=product_creation_input.serial_number,
                                       serial_number=product_creation_input.serial_number,
                                       model=product_creation_input.model,
                                       brand=product_creation_input.brand.upper(),
                                       price=product_creation_input.price,
                                       name=product_creation_input.name.upper(),
                                       sku=self.generate_sku(product_creation_input.model,
                                                             product_creation_input.brand,
                                                             product_creation_input.name))
        try:
            self.db.create(
                collection=self.__products_collection, document_id=product_creation_input.serial_number, document_data=document_data
            )
        except ValidationError as error:
            raise ProductModelError(f"Error creating product model. Please contact to support service. Error: {error}")
        return document_data

    def update_sku_according_to_product_update(self, product_doc: DocumentSnapshot, model: str = None, brand: str = None, name: str = None, **kwargs):
        model_ = product_doc.get("model")
        brand_ = product_doc.get("brand")
        name_ = product_doc.get("name")

        model = model_ if not model else model
        brand = brand_ if not brand else brand
        name = name_ if not name else name
        return self.generate_sku(model, brand, name)

    def update_product(self, product_update_input: ProductsUpdateInput):
        doc_to_update = {}
        document_data = product_update_input.dict()
        document_data.pop("product_id")
        for field in document_data:
            if document_data.get(field):
                doc_to_update.update({field: document_data.get(field)})
            else:
                continue
        time_ = int(time.time() * 1000)
        if not doc_to_update:
            raise ProductNotUpdated("Product not updated, Theres is not fields to updated")

        doc_ref: DocumentReference = self.db.get_doc_reference(self.__products_collection, product_update_input.product_id)

        @firestore.transactional
        def update(transaction: Transaction):
            product_snapshot = doc_ref.get(transaction=transaction)
            product_id = product_snapshot.get("id")
            if not product_id:
                raise DataNotFoundError(f"Product Id: {product_update_input.product_id} not found!")

            sku = self.update_sku_according_to_product_update(product_snapshot, **doc_to_update)

            doc_to_update.update({"updated_at": time_, "sku": sku})
            transaction.update(doc_ref, doc_to_update)
            return {"updated": doc_to_update}

        return update(self.db.db_transaction)

    def delete_product(self, product_delete_input: ProductDeleteInput):
        self.db.delete(collection=self.__products_collection, document_id=product_delete_input.product_id)
        print("Deleted!")
        return {}

    def get_product_by_sku(self, sku: str):
        results = self.db.query(collection=self.__products_collection, filters=[("sku", "==", sku.upper())])
        if not results:
            raise DataNotFoundError(f"Product for   SKU  {sku} not found!")

        return {"products": results}

    def get_all_products(self):
        return {"products": self.db.get_all(self.__products_collection)}

