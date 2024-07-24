# Serializer Module for Flask Application

This module provides a set of serializers for your Flask application, allowing you to easily validate and serialize data. The serializers are built with flexibility and extendability in mind, providing features such as nested serialization and integration with Pydantic models.

## Table of Contents
1. [Installation](#installation)
2. [Basic Usage](#usage)
3. [Creating Custom Serializers](#custom-serializers)
4. [Validators & Other Utilities](#validators--other-utilities)
5. [Support My Work](#support-my-work)

## Installation

To use the serializers in your project, simply include the necessary files in your application directory.

```bash
pip install sqlalchemy-serializer-meta
```

## Usage

Can be used to Serialize SQLAlchemy Model or Flask-SQLAlchemy model.

### Basic Usage

Here's an example of how to use the `UserRegisterSerializer` to validate and create a new user:

```python
from your_application.serializers import UserRegisterSerializer
from your_application.models import User

data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "password": "securepassword123"
}

serializer = UserRegisterSerializer(data=data)
if serializer.is_valid():
    user = serializer.save()
    print("User created:", user)
else:
    print("Errors:", serializer.errors)
```

In this example your custom serializer module/package

```py
from sqlalchemy_serializer_meta import Serializer, ModelSerializer, SerializerError
from your_application.models import User

class UserRegisterSerializer(Serializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_first_name(self, value) -> str:
        # Your Code
        return value

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]

class UserLoginSerializer(Serializer):
    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, email: str) -> str:
        # Your Code
        # Code pass
        self.instance = object # User Object
        return email

    def validate_password(self, password: str) -> str:
        # Your Code
        return password

    # Override serializer
    def to_representation(self, instance: object) -> dict:
        # Your Code
        return UserSerializer(instance=instance).data
```

### Nested Serialization

To handle nested relationships, you can define nested serializers and use them in your main serializer. 

#### Single Nested Object

When dealing with a single nested object, you do not need to specify `many=True`. Here's an example:

```python
from your_application.serializers import UserSerializer, ShippingAddressSerializer

class UserDetailSerializer(UserSerializer):
    shipping_address = ShippingAddressSerializer()

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'shipping_address']

# Usage
user = User.query.get(1)
serializer = UserDetailSerializer(instance=user)
print(serializer.data)
```

This will serialize the `shipping_address` field as a dictionary:

```json
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "shipping_address": {
        "street": "123 Main St",
        "city": "Anytown",
        "zipcode": "12345"
    }
}
```

#### Multiple Nested Objects

When dealing with multiple nested objects, use `many=True` to return a list of dictionaries. Here's an example:

```python
from your_application.serializers import UserSerializer, ShippingAddressSerializer

class UserDetailSerializer(UserSerializer):
    shipping_addresses = ShippingAddressSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'shipping_addresses']

# Usage
user = User.query.get(1)
serializer = UserDetailSerializer(instance=user)
print(serializer.data)
```

This will serialize the `shipping_addresses` field as a list of dictionaries:

```json
{
    "id": 1,
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "shipping_addresses": [
        {
            "street": "123 Main St",
            "city": "Anytown",
            "zipcode": "12345"
        },
        {
            "street": "456 Elm St",
            "city": "Othertown",
            "zipcode": "67890"
        }
    ]
}
```

### Integration with Pydantic Models

You can also integrate Pydantic models for additional validation. Here's an example:

```python
from your_application.serializers import UserSerializer, SerializerError
from pydantic import BaseModel, EmailStr, ValidationError

class UserPydanticModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr

class UserPydanticSerializer(UserSerializer):
    pydantic_model = UserPydanticModel

    def validate_pydantic(self, data):
        try:
            pydantic_instance = self.pydantic_model(**data)
            return pydantic_instance.model_dump()  # Dump the validated model to dictionary
        except ValidationError as e:
            raise SerializerError(e, "Invalid data")

# Usage
data = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
}

serializer = UserPydanticSerializer(data=data)
if serializer.is_valid():
    print("Valid data:", serializer.validated_data)
else:
    print("Errors:", serializer.errors)
```

### Updating Existing Instances

The `.save()` method is designed to update an instance if it already exists, rather than creating a new one. If the `instance` attribute is set, `.save()` will call the `.update()` method. If `instance` is `None`, it will call `.create()`.

Here's an example:

```python
from your_application.serializers import UserSerializer
from your_application.models import User

# Update an existing user
user_instance = User.query.get(1)
data = {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@example.com"
}

serializer = UserSerializer(instance=user_instance, data=data)
if serializer.is_valid():
    user = serializer.save()
    print("User updated:", user)
else:
    print("Errors:", serializer.errors)
```

## Custom Serializers

You can create custom serializers by inheriting from `Serializer` or `ModelSerializer`. Here's an example:

```python
from sqlalchemy_serializer_meta import ModelSerializer
from your_application.models import CustomModel

class CustomModelSerializer(ModelSerializer):
    class Meta:
        model = CustomModel
        fields = ['id', 'name', 'description']

# Usage
instance = CustomModel.query.get(1)
serializer = CustomModelSerializer(instance=instance)
print(serializer.data)
```

## Serializer Validated Fields

You can customize your field validation by adding `validate_<field_name>` methods in your `Serializer class`.

Can be used in SQLAlchemy and Flask API

```py
from sqlalchemy_serializer_meta import Serializer
from your_application.models import CustomModel
from your_application.validators import CustomValidator
from typing import Union

class CustomPydantic(BaseModel):
    id: str
    name: str
    description: EmailStr

class CustomModelSerializer(Serializer):
    # If not specified the validate_pydantic method won't be called hence no errors will occure
    pydantic_model: BaseModel = CustomPydantic

    class Meta:
        model = CustomModel
        fields = ['id', 'name', 'description']

    # Custom Validation for name
    def validate_name(self, value):
        # This will trigger Custome made Validator or pass
        CustomValidator(SerializerError).validate(value)
        return value


def serialize(data: dict) -> Union[dict, list[dict]]:
    # To trigger validators you have to initiate .is_valid() method
    serializer = CustomModelSerializer(data=data)

    try:
        # Trigger validation
        if serializer.is_valid():
            serializer.save()
            return serializer.data
        # If validation did not pass custom validation Grab Errors
        return serializer.errors
        # if validation did not pass Pydantic Validation
    except ValidationError as e: # If pydanic model not defined this error will not occure because validate_pydantic wont be called.
        return e.errors()
        # other unexpected or unhandled errors.
    except Exception as e:
        return e

serialize({'name': 'test', 'description': 'test@test.com',"id":1})
```

### Reusable Serializer Design with SQLAlchemy and Flask-SQLAlchemy

The design of the `CustomModelSerializer` class in our Flask application leverages the flexibility and robustness of SQLAlchemy and Flask-SQLAlchemy, allowing it to be highly reusable across different projects. This approach ensures that the main views or functions in your API can remain focused on returning data or handling errors, rather than getting bogged down in validation logic.

#### Key Features of the Design:

1. **Modular Validation:**
    - By using Pydantic for model validation, we ensure that data is consistently validated before it is processed or saved.
    - Custom validation methods like `validate_name` allow for specific field-level validation rules, making the serializer adaptable to different models and requirements.

2. **Separation of Concerns:**
    - The serializer handles data validation, deserialization, and serialization, keeping these concerns separate from the view logic.
    - This separation allows the view functions to focus on API response generation, improving readability and maintainability.

3. **Custom Error Handling:**
    - The design includes robust error handling, catching validation errors from Pydantic and custom validators, and other exceptions.
    - This ensures that the API can provide meaningful error messages to the client, improving the user experience and making debugging easier.

4. **Ease of Integration:**
    - The `CustomModelSerializer` can be easily integrated with Flask routes, as demonstrated in the example.
    - This flexibility makes it simple to reuse the serializer across different endpoints or even different projects, as long as they use SQLAlchemy and Flask-SQLAlchemy.

#### Example Usage in Flask API:

```py
from flask import Flask, request, jsonify
from sqlalchemy_serializer_meta import Serializer
from your_application.models import CustomModel
from your_application.validators import CustomValidator
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Union

class CustomPydantic(BaseModel):
    id: str
    name: str
    description: EmailStr

class CustomModelSerializer(Serializer):
    pydantic_model: BaseModel = CustomPydantic

    class Meta:
        model = CustomModel
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        CustomValidator(SerializerError).validate(value)
        return value

app = Flask(__name__)

@app.route('/serialize', methods=['POST'])
def serialize_data():
    data = request.json
    serializer = CustomModelSerializer(data=data)

    try:
        if serializer.is_valid():
            serializer.save()
            return jsonify(serializer.data), 201
        return jsonify(serializer.errors), 400
    except ValidationError as e:
        return jsonify(e.errors()), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

#### Benefits for Different Projects:

- **Consistency:** Ensures consistent data validation across various projects, reducing the likelihood of errors and inconsistencies.
- **Reusability:** The modular design means the same serializer class can be used across different models and endpoints, minimizing duplicate code.
- **Focus on Business Logic:** By handling validation and serialization within the serializer, the main view functions can focus on business logic and API response handling, making the codebase cleaner and more maintainable.

By adopting this design, you can create scalable, maintainable, and robust APIs that leverage the power of SQLAlchemy and Flask-SQLAlchemy, ensuring that your application remains flexible and adaptable to changing requirements.


## Validators & Other Utilities

You can add a `read_only` to class meta to specify fields that can only be retrieved but not be updated.

Also you can add a `write_only` to a class to specify fields that can be put as inputs but never retrieved

By default field `password` is passively added as a `write_only` field.


In your application `validators.py`:

```py
from sqlalchemy_serializer_meta.validator import BaseValidator

class CustomValidator(BaseValidator):
    def validate(self, value):
        if not value:
            raise self.raise_exception(ValueError, 'Value cannot be empty')

```

In your application `serializers.py`:

```py
from sqlalchemy_serializer_meta import Serializer
from your_application.models import CustomModel
from your_application.validators import CustomValidator
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Union

class CustomPydantic(BaseModel):
    id: str
    name: str
    description: EmailStr

class CustomModelSerializer(Serializer):
    pydantic_model: BaseModel = CustomPydantic

    class Meta:
        model = CustomModel
        fields = ['id', 'name', 'description']
        read_only = ['id']
        write_only = ['name']

    def validate_name(self, value):
        CustomValidator(SerializerError).validate(value)
        return value
```

## Support My Work

If you find my free content and projects helpful, consider supporting me to enable more learning resources for the community. Your contributions will go towards creating new content and maintaining existing projects.

### How to Contribute

You can contribute by making a donation through PayPal:

[![Donate](https://img.shields.io/badge/Donate-PayPal-blue.svg)](https://paypal.me/Waheedkhaled?country.x=EG&locale.x=en_US)

You can contribute by making donation through Buy me coffee:

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/waheedKh)

Your generosity is greatly appreciated!

### Why Contribute?

By supporting this project, you help ensure the continued availability of free educational content and the development of new projects. Your contribution makes a meaningful impact on the community of learners.

Thank you for your support!