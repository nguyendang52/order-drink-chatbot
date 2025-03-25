from vertexai.generative_models import (
    Content,
    GenerativeModel,
    Part,
    Tool,
)

chat_history = [
    {
                "role": "user",
                "content": "user_input"
    }, 
    {
                "role": "model",
                "content": "response.text"
            }
]
formatted_history = [
    Content(role=item["role"], parts=[Part.from_text(item["content"])])
    for item in chat_history
]

print('format', formatted_history)