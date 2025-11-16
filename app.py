import streamlit as st
from google import genai

# --- 🛑 ВАШ GEMINI API КЛЮЧ 🛑 ---
# Ключ, который вы только что предоставили
GEMINI_API_KEY = "AIzaSyDsytyHtW_xPl6MPxsa6WzkQsZCrw7mtr4" 
# ------------------------------------------------------------

# Инициализация Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
    client = genai.Client()
except Exception as e:
    st.error("Ошибка инициализации Gemini. Проверьте ваш API ключ!")

# --- Настройки Streamlit (с логотипом) ---
LOGO_FILENAME = "logonpg.png" 

st.set_page_config(
    page_title="Чат-бот Mastercard",
    layout="wide",
    page_icon=LOGO_FILENAME 
)

st.image(LOGO_FILENAME, width=100) 
st.title("Чат-бот Mastercard на Gemini")

# Инициализация истории чата
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "Ты - высококвалифицированный финансовый консультант и эксперт по платежным системам Mastercard. Твоя основная задача — давать точные, полезные и вежливые ответы на вопросы о продуктах и услугах компании Mastercard. Анализируй язык каждого входящего запроса. Ответ должен быть строго на том языке, на котором задан вопрос. Отвечай только по теме финансов и платежей, связанных с Mastercard. ВСЕГДА будь дружелюбным и гостеприимным."},
        {"role": "assistant", "content": "👋 Привет! Я ваш персональный финансовый помощник от Mastercard. Спрашивайте о картах, платежах и услугах – я здесь, чтобы помочь!"}
    ]

# Отображение предыдущих сообщений
for message in st.session_state["messages"]:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Логика обработки запроса ---
if prompt := st.chat_input("Ваш вопрос:"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # Формируем историю для Gemini
    history = [
        {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
        for m in st.session_state["messages"] if m["role"] != "system"
    ]
    
    # Добавляем системный промпт как первый элемент истории
    system_prompt = st.session_state["messages"][0]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner('Gemini думает...'):
            try:
                response = client.chats.create(
                    model='gemini-2.5-flash',
                    messages=history,
                    system_instruction=system_prompt
                )
                ai_response = response.text
                st.markdown(ai_response)
            except Exception as e:
                ai_response = f"Ошибка: Не могу получить ответ от Gemini. Возможно, ключ неверный, или лимит исчерпан."
                st.markdown(ai_response)

    st.session_state["messages"].append({"role": "assistant", "content": ai_response})