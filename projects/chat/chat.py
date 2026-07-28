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
    system = "Você é uma programadora especialista na linguagem pyhton. Responda o que for perguntado de forma direta, sem exemplos ou comentários. Seja sucinto e simples. Busque sempre a resposta mais eficiente e rápida. Não explique o que você está fazendo, apenas faça."

    #while True: # Criar um loop para continuar a conversa
        #user_input = input("User: ") #Definir a entrada do usuário - digitando
    user_input = "Escreva uma função python que verifique caracteres duplicados em uma string."
    add_user_message(messages, user_input)

    answer = chat(messages, system)
    add_assistant_message(messages, answer)

    print("Assistant: " + answer)