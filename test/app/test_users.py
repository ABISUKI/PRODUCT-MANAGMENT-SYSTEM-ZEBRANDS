from unittest.mock import Mock, patch

from pydantic import ValidationError

from api.app.entities.exceptions import UserAlreadyExistError, UserNotUpdated
from api.app.entities.input_models import UserCreationInput, UserUpdateInput
from api.app.users import Users


def test_user_doc_mode_success_model():
    doc_model = Users.user_doc_model(
        doc_id="doc_id_example",
        user_name="user_name_example",
        group_id="group_id_example",
        role_ids=["rol_id_example"],
        email="email_example",
        password="pwd_example",
    )
    assert doc_model


def test_user_doc_mode_wrong_model():
    try:
        _ = Users.user_doc_model(
            doc_id="doc_id_example",
            user_name="user_name_example",
            group_id="group_id_example",
            role_ids=["rol_id_example"],
            email=None,
            password="pwd_example",
        )
        assert False
    except Exception as error:
        assert type(error) == ValidationError


def test_create_user_success_creation():
    db = Mock()
    db.query.return_value = []
    db.create.return_value = None
    users = Users(db)
    user_creation_input = UserCreationInput(
        user_name="neftali",
        password="pwd",
        group_id="1092u4",
        role_ids=["1234cdfv"],
        email="173y74@gmail.com",
    )
    user = users.create_user(user_creation_input)

    assert user.get("id")
    assert user.get("user_name") == user_creation_input.user_name
    assert user.get("password") != user_creation_input.password


def test_create_user_wrong_creation_user_already_exist():
    db = Mock()
    db.query.return_value = [
        {
            "password": "$2b$12$WYCDExjqIIxCbT19to8.LOO694OEXaAh2ZVl9AHZXQC7xlEObR21u",
            "created_at": 1668796828663.0,
            "id": "58ce025a-9467-48a9-8aa8-5dda0fdd9955",
            "group_id": "123456",
            "update_at": 1668796828663.0,
            "user_name": "Neftali",
            "modified_by": None,
            "role_ids": ["GDPK8oZ49T67oDxfV4Rb", "FJrLP3utcyeXLzRFPhYS"],
            "email": "15310443abi@gmail.com",
        }
    ]
    db.create.return_value = None
    users = Users(db)
    user_creation_input = UserCreationInput(
        user_name="neftali",
        password="pwd",
        group_id="1092u4",
        role_ids=["1234cdfv"],
        email="173y74@gmail.com",
    )
    try:
        _ = users.create_user(user_creation_input)
        assert False
    except Exception as error:
        assert type(error) == UserAlreadyExistError


def test_update_user_success():
    db = Mock()
    db.update.return_value = None
    users = Users(db)
    user_update_input = UserUpdateInput(user_id="hola",
                                        user_name="updated",
                                        role_ids=["187283y738rh"])
    user = users.update_user(user_update_input)

    assert user.get("updated", {}).get("user_name") == user_update_input.user_name
    assert user.get("updated", {}).get("role_ids") == user_update_input.role_ids


def test_update_user_failed_not_field_to_update():
    db = Mock()
    db.update.return_value = None
    users = Users(db)
    user_update_input = UserUpdateInput(user_id="hola")

    try:
        _ = users.update_user(user_update_input)
        assert False
    except Exception as error:
        assert type(error) == UserNotUpdated
