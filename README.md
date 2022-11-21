# PRODUCT-MANAGMENT-SYSTEM-ZEBRANDS
 Basic catalog system to manage products. A product should have basic info such as sku, name, price and brand.

### Installation and Usage ⚙️ 🔧
clone repo and pip install 
```commandline
pip install -r requirements.py
```
run app
```commandline
uvicorn main:app
```


### Unit Test 🔬
* Unit testing execution example. 
```commandline
python -m pytest
```
### Endpoints ↘️
| API                                 | Version | Method | Description                       |
|-------------------------------------| ------- |--------|-----------------------------------|
| v1.0/zebrands-system/login          | V1      | POST   | Get credentials.                  |
| v1.0/zebrands-system/users          | V1      | POST   | Create a new user.                |
| v1.0/zebrands-system/users          | V1      | PUT    | Update an user .                  |
| v1.0/zebrands-system/users          | V1      | GET    | Gets all user unformation .       |
| v1.0/zebrands-system/{user_id}      | V1      | GET    | Gets User information .           |
| v1.0/zebrands-system/users          | V1      | DELETE | Delete user .                     |
| v1.0/ zebrands-system/products      | V1      | POST   | Add new product to catalog .      |
| v1.0/zebrands-system/products       | V1      | PUT    | Update product .                  |
| v1.0/zebrands-system/products       | V1      | GET    | Get all products .                |
| v1.0/zebrands-system/products/{sku} | V1      | GET    | Get product by sku                |
| v1.0/zebrands-system/products       | V1      | DEL    | Remove products  .                |



### Technology involved 👾
* FastAPi
* Python
* FireBase
