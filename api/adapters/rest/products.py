from fastapi import APIRouter, Request, Depends, Response

from api.adapters.rest.users import bearer_auth
from api.app.entities.input_models import ProductsCreationInput, ProductsUpdateInput, ProductDeleteInput
from api.app.entities.outputs_models import OutputBase, GetAllProductsOutputBase, ProductsCreationOutputBase
from api.app.products import Products
from api.ports.auth.auth import Auth
from api.ports.firestore.db_main import DBMainFirestore
from api.utils.service_exception_handler import ControllerExceptionHandler

router = APIRouter()


@router.post("", status_code=201, include_in_schema=False)
@router.post("/", status_code=201, tags=["products"], response_model=ProductsCreationOutputBase)
@ControllerExceptionHandler.products
@Auth.check_access_api
async def add_product(response_root: Response,
                      request: Request,
                      product_creation_input: ProductsCreationInput,
                      token: str = Depends(bearer_auth),
                      db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    products = Products(db=db_firestore)
    return products.add_product(product_creation_input)


@router.get("", status_code=200, tags=["products"], response_model=GetAllProductsOutputBase)
@ControllerExceptionHandler.products
async def get_all_products(response_root: Response,
                           request: Request,
                           db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    print(f"Get all products:")
    products = Products(db=db_firestore)
    return products.get_all_products()


@router.get("/{sku}", status_code=200, tags=["products"], response_model=GetAllProductsOutputBase)
@ControllerExceptionHandler.products
async def get_product_by_sku(response_root: Response,
                             request: Request,
                             sku: str,
                             db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    print(f"Get product by sku: {sku}")
    products = Products(db=db_firestore)
    return products.get_product_by_sku(sku)


@router.put("", status_code=200, include_in_schema=False)
@router.put("/", status_code=200, tags=["products"], response_model=OutputBase)
@ControllerExceptionHandler.products
@Auth.check_access_api
async def update_product(response_root: Response,
                         request: Request,
                         products_input: ProductsUpdateInput,
                         token: str = Depends(bearer_auth),
                         db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    products = Products(db=db_firestore)
    return products.update_product(products_input)


@router.delete("", status_code=200, include_in_schema=False)
@router.delete("/", status_code=200, tags=["products"], response_model=OutputBase)
@ControllerExceptionHandler.products
@Auth.check_access_api
async def remove_product(response_root: Response,
                         request: Request,
                         product_delete_input: ProductDeleteInput,
                         token: str = Depends(bearer_auth),
                         db_firestore: DBMainFirestore = Depends(DBMainFirestore)):
    products = Products(db=db_firestore)
    return products.delete_product(product_delete_input)
