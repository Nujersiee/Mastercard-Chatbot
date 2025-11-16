import streamlit as st
from google import genai
import os

# --- 🛑 Извлекаем ключ из Streamlit Secrets (Безопасный метод) 🛑 ---
# Ключ теперь будет установлен в панели 'Secrets' на Streamlit Cloud
try:
    # Имя ключа должно совпадать с тем, что вы установите в Streamlit Secrets
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"] 
except KeyError:
    # Эта ошибка показывает, что вы не добавили ключ в Streamlit Secrets
    st.error("⚠ API ключ GEMINI_API_KEY не найден в Streamlit Secrets. Пожалуйста, добавьте его по инструкции ниже!")
    st.stop() # Останавливаем выполнение, пока ключ не будет добавлен

# --- Инициализация Gemini ---
try:
    genai.configure(api_key=GEMINI_API_KEY)
    client = genai.Client()
except Exception as e:
    st.error(f"Ошибка инициализации Gemini. Проверьте ваш API ключ! (Детали: {e})")
    st.stop() # Останавливаем выполнение

# --- Настройки Streamlit (с логотипом) ---
LOGO_FILENAME = "logonpg.png" 

st.set_page_config(
    page_title="Чат-бот Mastercard",
    layout="wide",
    page_icon=LOGO_FILENAME 
)

st.sidebar.image(LOGO_FILENAME, width=100) 
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
    
    # Извлекаем системный промпт
    system_prompt = st.session_state["messages"][0]["content"]
    
    with st.chat_message("assistant"):
        with st.spinner('Gemini думает...'):
            try:
                # Используем чаты для поддержки контекста (истории)
                response = client.chats.create(
                    model='gemini-2.5-flash',
                    messages=history,
                    system_instruction=system_prompt
                )
                ai_response = response.text
                st.markdown(ai_response)
            except Exception as e:
                ai_response = f"Ошибка: Не могу получить ответ от Gemini. Проблема с ключом или лимитом. (Детали: {e})"
                st.markdown(ai_response)

    st.session_state["messages"].append({"role": "assistant", "content": ai_response})