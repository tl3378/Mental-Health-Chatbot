#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""
# app.py

import streamlit as st
import os
import sys
from dotenv import load_dotenv
from conversationchain.chatbot_fn import chatbot_fn
from conversationchain.app_setup import setup_conversation_chain
import logging
import spacy

# Download spaCy model if not present
try:
    spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    spacy.load("en_core_web_sm")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Load environment variables
env_path = os.path.join(project_root, 'conversationchain', 'model.env')
load_dotenv(env_path)

# Verify API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    st.error("OpenAI API key not found. Please check your model.env file.")
    st.stop()

# Page config
st.set_page_config(
    page_title="Mental Health Support Chatbot",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_chain" not in st.session_state:
    try:
        logger.info("Initializing conversation chain...")
        st.session_state.conversation_chain = setup_conversation_chain()
        logger.info("Conversation chain initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize conversation chain: {str(e)}", exc_info=True)
        st.error(f"Failed to initialize conversation chain: {str(e)}")
        st.stop()

if "input_key" not in st.session_state:
    st.session_state.input_key = 0

# Custom CSS with optimized animations
st.markdown("""
<style>
:root {
    --primary-color: #6B8CFF;
    --secondary-color: #FFB6C1;
    --background-color: #F5F7FA;
    --text-color: #2C3E50;
    --border-radius: 20px;
    --transition-speed: 0.3s;
}

.chat-container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: white;
    border-radius: var(--border-radius);
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.welcome-bubble {
    height: 20%;
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    display: flex;
    justify-content: center;
    align-items: center;
    color: white;
    font-size: 1.5em;
    text-align: center;
    padding: 20px;
    border-radius: var(--border-radius);
    margin-bottom: 20px;
    transition: all var(--transition-speed);
}

.message {
    padding: 1rem;
    border-radius: var(--border-radius);
    margin: 1rem 0;
    max-width: 70%;
    opacity: 0;
    transform: translateY(10px);
    animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.user-message {
    background: var(--primary-color);
    color: white;
    margin-left: auto;
    border-bottom-right-radius: 5px;
}

.bot-message {
    background: #F0F2F5;
    color: var(--text-color);
    margin-right: auto;
    border-bottom-left-radius: 5px;
}

.input-area {
    display: flex;
    gap: 10px;
    margin: 20px 0;
    padding: 10px;
    background: white;
    border-radius: var(--border-radius);
    position: sticky;
    bottom: 0;
    z-index: 100;
}

.input-area .stTextInput {
    flex-grow: 1;
}

.disclaimer {
    color: #666666;
    font-size: 0.8rem;
    text-align: center;
    margin-top: 20px;
    padding: 10px;
    background: #F8F9FA;
    border-radius: var(--border-radius);
}

.emergency-button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: #FF6B6B;
    padding: 15px 25px;
    border-radius: var(--border-radius);
    color: white;
    text-decoration: none;
    box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
    transition: all var(--transition-speed);
}

.emergency-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(255, 107, 107, 0.4);
}
</style>
""", unsafe_allow_html=True)

# Chat interface
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

# Welcome bubble
st.markdown("""
    <div class="welcome-bubble">
        Welcome to a safe space for conversation
    </div>
""", unsafe_allow_html=True)

# 消息显示（在上方）
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f'''<div class="message user-message">{message["content"]}</div>''', unsafe_allow_html=True)
    else:
        st.markdown(f'''<div class="message bot-message">{message["content"]}</div>''', unsafe_allow_html=True)

# 输入区（form在下方）
st.markdown('<div class="input-area">', unsafe_allow_html=True)
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input(
        "Type your message...",
        label_visibility="collapsed"
    )
    submitted = st.form_submit_button("Send")
    if submitted and user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.spinner("Thinking..."):
            try:
                response = chatbot_fn(user_input, st.session_state.messages, st.session_state.conversation_chain)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                logger.error(f"Error getting bot response: {str(e)}", exc_info=True)
                st.error(f"Internal error: {str(e)}")
                st.write(str(e))
                st.error("Sorry, there was an error processing your message. Please try again.")
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# Emergency button
st.markdown("""
    <a href="https://www.crisistextline.org/" target="_blank" class="emergency-button">
        Need Immediate Help?
    </a>
""", unsafe_allow_html=True)

# Disclaimer
st.markdown("""
    <div class="disclaimer">
        This chatbot is not a substitute for professional mental health care. If you're in crisis, please seek immediate help from a mental health professional or emergency services.
    </div>
""", unsafe_allow_html=True)

# Close chat-container div
st.markdown('</div>', unsafe_allow_html=True)
