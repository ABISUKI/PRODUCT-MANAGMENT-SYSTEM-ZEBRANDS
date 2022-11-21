from unittest.mock import Mock, patch

from google.cloud.firestore_v1 import DocumentSnapshot
from pydantic import ValidationError

from api.app.entities.exceptions import UserAlreadyExistError, UserNotUpdated, SkuGenerationError, ProductModelError
from api.app.entities.input_models import UserCreationInput, UserUpdateInput, ProductsCreationInput, ProductsUpdateInput
from api.app.products import Products


def test_product_doc_mode_success_model():
    doc_model = Products.doc_model(
        doc_id="doc_id_example",
        serial_number="serial_number_example",
        model="model_example",
        brand="brand_example",
        price=45.5,
        name="name_example",
        sku="sku_example"
    )
    assert doc_model


def test_product_doc_mode_wrong_model():
    try:
        _ = Products.doc_model(
                        doc_id="doc_id_example",
                        serial_number="serial_number_example",
                        model="model_example",
                        brand="brand_example",
                        price="",
                        name="name_example",
                        sku="sku_example"
        )
        assert False
    except Exception as error:
        assert type(error) == ValidationError


def test_generate_sku_success():
    sku = Products.generate_sku(model="90A", brand="hp", name="laptop")
    assert sku == "LAPTO-HP-90A"


def test_generate_sku_failed():
    try:
        _ = Products.generate_sku(model="90A", brand=None, name="laptop")
        assert False
    except Exception as error:
        assert type(error) == SkuGenerationError


def test_add_product_success_update():
    db = Mock()
    db.create.return_value = None

    product_creation_input = ProductsCreationInput(serial_number="sjndibc",
                                                 model="AB91",
                                                 brand="hp",
                                                 price=102.99,
                                                 name="keyboard")
    products = Products(db)
    product = products.add_product(product_creation_input)
    assert product
    assert product.get("id") == product_creation_input.serial_number
    assert product.get("sku") == "KEYBOAR-HP-AB91"


def test_add_product_failed_product_model():
    db = Mock()
    db.create.return_value = None

    product_creation_input = ProductsCreationInput(serial_number="sjndibc",
                                                   model="AB91",
                                                   brand="hp",
                                                   price=10.50,
                                                   name="keyboard")
    products = Products(db)
    try:
        product_creation_input.price = None
        _ = products.add_product(product_creation_input)
        assert False
    except Exception as error:
        assert type(error) == ProductModelError


def test_update_sku_according_to_product_update_success():
    db = Mock()
    products = Products(db)
    product_doc: DocumentSnapshot = {"model": "A90", "brand": "hp", "name": "keyboard"}
    sku = products.update_sku_according_to_product_update(product_doc=product_doc, model="A67")
    assert sku == "KEYBOAR-HP-A67"


def test_update_sku_according_to_product_update_failed_not_snap():
    db = Mock()
    products = Products(db)
    product_doc: DocumentSnapshot = {}
    try:
        _ = products.update_sku_according_to_product_update(product_doc=product_doc, model="A67")
        assert False
    except Exception as error:
        assert type(error) == SkuGenerationError
