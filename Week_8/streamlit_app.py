# streamlit_app.py
# Streamlit chat UI that talks to our FastAPI server
#
# Run with:
#   streamlit run streamlit_app.py
#
# Make sure app.py is running first:
#   uvicorn app:app --host 0.0.0.0 --port 8000

import streamlit as st
import requests
import json

# Config
API_URL = "http://localhost:8000"

# Page setup
st.set_page_config(
    page_title = "Medical Assistant",
    page_icon  = "🏥",
    layout     = "wide"
)

st.title("🏥 Medical Assistant")

# Sidebar: generation controls
with st.sidebar:
    st.header("️Settings")

    system_prompt = st.text_area(
        "System prompt",
        value = "You are a helpful medical assistant. Answer clearly and accurately.",
        height = 100
    )

    temperature = st.slider("Temperature",  min_value=0.0, max_value=1.0, value=0.7, step=0.05)
    top_p       = st.slider("Top-p",        min_value=0.0, max_value=1.0, value=0.95, step=0.05)
    top_k       = st.slider("Top-k",        min_value=1,   max_value=100, value=40,   step=1)
    max_tokens  = st.slider("Max tokens",   min_value=50,  max_value=500, value=200,  step=50)
    stream_mode = st.toggle("Streaming mode", value=True)

    st.divider()

    # check API health
    if st.button("Check API status"):
        try:
            r = requests.get(f"{API_URL}/health", timeout=5)
            if r.status_code == 200:
                st.success("API is running and healthy")
            else:
                st.error("API returned error")
        except Exception as e:
            st.error(f" Cannot reach API: {e}")

    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

#Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# show all previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

#Chat input 
user_input = st.chat_input("Ask a medical question...")

if user_input:
    # show user message
    with st.chat_message("user"):
        st.write(user_input)

    # add to history
    st.session_state.messages.append({
        "role":    "user",
        "content": user_input
    })

    # call API
    with st.chat_message("assistant"):
        try:
            payload = {
                "messages":    st.session_state.messages,
                "system":      system_prompt,
                "temperature": temperature,
                "top_p":       top_p,
                "top_k":       top_k,
                "max_tokens":  max_tokens,
                "stream":      stream_mode
            }

            if stream_mode:
                # streaming — show tokens as they arrive
                response_text = ""
                placeholder   = st.empty()

                with requests.post(
                    f"{API_URL}/chat",
                    json    = payload,
                    stream  = True,
                    timeout = 120
                ) as r:
                    for chunk in r.iter_content(chunk_size=None, decode_unicode=True):
                        if chunk:
                            response_text += chunk
                            placeholder.write(response_text)

            else:
                # normal — wait for full response
                with st.spinner("Thinking..."):
                    r = requests.post(
                        f"{API_URL}/chat",
                        json    = payload,
                        timeout = 120
                    )
                    data          = r.json()
                    response_text = data.get("response", "No response")
                    st.write(response_text)
                    st.caption(f"Tokens: {data.get('tokens', '?')} | Request ID: {data.get('request_id', '?')}")

            # add assistant response to history
            st.session_state.messages.append({
                "role":    "assistant",
                "content": response_text
            })

        except Exception as e:
            st.error(f"Error calling API: {e}")
            st.info("Make sure the FastAPI server is running: uvicorn app:app --port 8000")