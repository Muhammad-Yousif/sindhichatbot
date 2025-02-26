import os
import sys
import streamlit as st
import openai
import requests

# Force UTF-8 Encoding
os.environ["PYTHONUTF8"] = "1"
sys.stdout.reconfigure(encoding='utf-8')

st.title("🤖 Multi-Model Sindhi Biology Chatbot")
st.write("هي بوٽ حياتيات بابت سوالن جا جواب ڏئي ٿو، ChatGPT ۽ DeepSeek جي مدد سان.")


# Store API selection and key securely
if "api_key" not in st.session_state:
    st.session_state.api_key = None
if "model" not in st.session_state:
    st.session_state.model = None

# Model selection dropdown
model_choice = st.selectbox("🔍 Select Model:", ["ChatGPT (OpenAI)", "DeepSeek"])

# API Key Input
if not st.session_state.api_key:
    api_key = st.text_input("🔑 Enter your API Key:", type="password")
    if api_key:
        st.session_state.api_key = api_key  # Store key securely
        st.session_state.model = model_choice  # Store model choice
        st.rerun()  # Refresh to hide input box
else:
    st.write(f"✅ Using **{st.session_state.model}** API")

    # User input for chatbot
    user_input = st.text_input("✍️ پنهنجو سوال داخل ڪريو:")

    if user_input:
        try:
            if st.session_state.model == "ChatGPT (OpenAI)":
                client = openai.OpenAI(api_key=st.session_state.api_key)

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Change to "gpt-4" if needed
                    messages=[{"role": "user", "content": user_input}]
                )
                reply = response.choices[0].message.content

            elif st.session_state.model == "DeepSeek":
                deepseek_url = "https://api.deepseek.com/v1/chat/completions"
                headers = {"Authorization": f"Bearer {st.session_state.api_key}"}
                data = {
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": user_input}]
                }

                response = requests.post(deepseek_url, json=data, headers=headers)
                reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response")

            else:
                reply = "⚠️ Invalid model selection!"

            st.write("🧠 **جواب:**", reply)

        except Exception as e:
            st.error(f"❌ API Error: {e}")
