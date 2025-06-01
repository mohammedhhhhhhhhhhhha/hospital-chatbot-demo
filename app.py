# app.py
import streamlit as st
import requests

st.title("🏥 Hospital Chatbot Demo")

# Session state
if "session" not in st.session_state:
    st.session_state["session"] = {}

user_input = st.text_input("You:", key="input")

if st.button("Send"):
    response = requests.post("http://localhost:8000/chat", json={"user_input": user_input, "session": st.session_state["session"]})
    data = response.json()
    st.session_state["session"] = data["session"]
    st.write("🤖:", data["bot_response"])
