import anthropic

client = anthropic.Anthropic()


def add_user_message(messages, user_input):
    messages.append({"role": "user", "content": user_input})
    return messages

def add_assistant_message(messages, assistant_response):
    messages.append({"role": "assistant", "content": assistant_response})
    return messages

def chat(messages, system=None, temperature=0.0):
    params = {
        "model": "claude-sonnet-4-6",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": temperature,
    }

    # Add system message -if provided-
    if system:
        params["system"] = system

    response = client.messages.create(**params)
    return response.content[0].text


if __name__ == "__main__":
    messages = []
    user_input = "Quantos dias para conhecer o México?"

    messages.append({"role": "user", "content": user_input})

    #Stream is a optional parameter that allows you to receive the response in chunks, instead of waiting for the entire response to be generated. This can be useful for long responses or for real-time applications.
    with client.messages.stream(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            print(text, end="")