import streamlit as st
import requests

API_URL = "http://localhost:8000/process"

st.set_page_config(page_title="AI Agent", layout="wide")
st.title("🤖 Agentic Multi-Modal Assistant")

with st.sidebar:
    st.markdown("### supported Formats")
    st.markdown("- **Images**: JPG, PNG (OCR)")
    st.markdown("- **Docs**: PDF")
    st.markdown("- **Audio**: MP3 (Speech to Text)")
    st.markdown("- **Links**: YouTube")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
with st.container():
    col1, col2 = st.columns([1, 4])
    
    with col1:
        uploaded_file = st.file_uploader("Upload", type=['png', 'jpg', 'pdf', 'mp3'], label_visibility="collapsed")
    
    with col2:
        user_input = st.chat_input("Enter your request...")

if user_input or (uploaded_file and user_input):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            st.markdown(f"*{uploaded_file.name} attached*")
    files = None
    if uploaded_file:
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    
    data = {"query": user_input}

    with st.spinner("Agent is thinking..."):
        try:
            response = requests.post(API_URL, data=data, files=files)
            if response.status_code == 200:
                res_json = response.json()
                bot_reply = res_json["response_text"]
                action = res_json["action_taken"]
                final_msg = bot_reply
                if res_json["needs_clarification"]:
                    final_msg = f"❓ **Clarification Needed**: {bot_reply}"
                else:
                    final_msg = f"**{action.upper()}**: \n\n{bot_reply}"

                st.session_state.messages.append({"role": "assistant", "content": final_msg})
                with st.chat_message("assistant"):
                    st.markdown(final_msg)
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Connection failed: {str(e)}")