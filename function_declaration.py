from vertexai.generative_models import (
    FunctionDeclaration,
)

get_drinks_menu_func = FunctionDeclaration(
    name="get_drinks_menu_func",
    description="Get the drinks menu from the API",
    parameters={
    "type": "object",
    "properties": {}
    },
)
place_order_func = FunctionDeclaration(
    name="place_order_func",
    description="Make order based on drink information the customer choose",
    parameters= {
    "type": "object",
    "properties": {
        "order_user": {
            "type": "string",
            "description": "The ID of the user placing the order",
            "default": "edbdbbc5-47c1-40b2-92f1-366e14d41849"
        },
        "tags": {
            "type": "array",
            "description": "The tags for the drink"
        },
        "drink": {
            "type": "integer",
            "description": "The ID of the drink to order",
        },
        "remark": {
            "type": "string",
            "description": "A remark for the order"
        },
        "quantity": {
            "type": "integer",
            "description": "The quantity of the drink to order. By default will be 1",
            "default": 1
        },
        "delivery_floor": {
            "type": "string",
            "description": "The delivery floor. The value should be formatted like: '1' or '8', etc",
            "default": "1"
        }
    },
    "required": [
        "drink",
    ]
  }
)
