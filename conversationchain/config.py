#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Try to load from Streamlit secrets first
api_key = st.secrets.get("OPENAI_API_KEY")

# If not found in secrets, try loading from .env file
if not api_key:
    env_path = os.path.join(os.path.dirname(__file__), 'model.env')
    load_dotenv(env_path)
    api_key = os.getenv("OPENAI_API_KEY")

# If still not found, raise error
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables or Streamlit secrets")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)
