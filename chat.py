import ollama

# Убедитесь, что модель Llama 3 запущена (ollama run llama3)
def generate_response(prompt):
    print(f"-> Запрос к Llama 3: {prompt}")
    response = ollama.chat(
        model='llama3',
        messages=[
            {
                'role': 'user',
                'content': prompt
            }
        ]
    )
    return response['message']['content']

print("--- Локальный чат-бот с Llama 3 запущен ---")
while True:
    user_input = input("Ваш вопрос: ")
    if user_input.lower() in ["выход", "exit"]:
        print("Завершение работы.")
        break
    
    # Получаем и печатаем ответ
    ai_response = generate_response(user_input)
    print("Ответ AI: " + ai_response)
    