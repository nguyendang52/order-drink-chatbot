import requests
from vertexai.generative_models import (
    Content,
    GenerativeModel,
    Part,
    Tool,
)

from function_declaration import get_drinks_menu_func, place_order_func

import vertexai
import pydash


url = "https://ots.space/apps/data-hub/v2-dev/items/drink_item?filter={}&limit=-1&fields=id&fields=slug&fields=name_en&fields=name_vi&fields=description_en&fields=description_vi&fields=volume&fields=thumbnail&fields=photos&fields=tags&fields=category&fields=category.id&fields=category.slug&fields=category.name_en&fields=category.name_vi&fields=enabled_quantity_input&fields=default_quantity"
api_get_drinks_menu_response = requests.get(url)

chat_history = []


def init_model():
    system_instruction = """You are bartender barista support for placing order from request of customer.
    When a customer visits your shop, you need to welcome he/she and provide the menu.
    If the customer want to you to suggest a drink, you can select based on preference of the customer.
    If the customer want to order a drink, please place this order from drink information that customer choose.
    """

    vertexai.init(project="one-global-epayment-dev", location="us-central1")
    model = GenerativeModel(
        "gemini-2.0-flash", system_instruction=system_instruction)

    return model


def prepare_chat_history_content(chat_history):

    formatted_history = [
        Content(role=item["role"], parts=[Part.from_text(item["message"])])
        for item in chat_history
    ]

    return formatted_history


def place_order(params):
    default_payload = {
        "order_user": "edbdbbc5-47c1-40b2-92f1-366e14d41849",
        "tags": None,
        "drink": 146,
        "remark": None,
        "quantity": 1,
        "delivery_floor": None,
        **params,
    }

    print('default_payload', default_payload)

    try:
        response = requests.post(
            "https://ots.space/apps/data-hub/v2-dev/items/drink-order", headers={"Authorization": "Bearer Lshs-BrRKbm04VH4spd5C2VHe6TITMsx"}, json=default_payload)

        response.raise_for_status()

        # Log response
        print(f"Request successful: {response.status_code}")
        print(f"Response Body: {response.text}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response Body: {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"Request error occurred: {err}")


def generate_content(model, user_input):
    chat_history.append({
        "role": "user",
        "message": user_input
    })

    chat_history_content = prepare_chat_history_content(chat_history)

    response = model.generate_content(
        chat_history_content +
        [
            Content(role="function", parts=[
                Part.from_dict({
                    "function_call": {
                        "name": "place_order_func",
                    }
                })
            ]),
            Content(role="function", parts=[
                Part.from_dict({
                    "function_call": {
                        "name": "get_drinks_menu_func",
                    }
                })
            ]),
            Content(role="function", parts=[
                Part.from_function_response(
                    name="get_drinks_menu_func",
                    response={
                        "content": api_get_drinks_menu_response.text,
                    }
                )
            ])
        ],
        tools=[Tool(function_declarations=[
                    get_drinks_menu_func, place_order_func])],
    )

    if not pydash.is_empty(pydash.get(response, 'text')):
        chat_history.append(
            {
                "role": "model",
                "message": response.text
            }
        )

        return response.text
    else:
        params = {}
        for key, value in response.candidates[0].content.parts[0].function_call.args.items():
            params[key] = str(int(value))

        place_order(params=params)


def chat_with_gemini():
    model = init_model()

    print("Gemini CLI Chat - Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat.")
            break
        response = generate_content(model, user_input)
        print("Gemini:", response)


chat_with_gemini()
