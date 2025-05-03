#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""

import os
import logging
from dotenv import load_dotenv
from openai import OpenAI
import streamlit as st

# Set up logging
logger = logging.getLogger(__name__)

try:
    # Try to load from Streamlit secrets first
    api_key = st.secrets.get("OPENAI_API_KEY")
    logger.info("Trying to get API key from Streamlit secrets...")
    
    # If not found in secrets, try loading from .env file
    if not api_key:
        logger.info("API key not found in Streamlit secrets, trying .env file...")
        env_path = os.path.join(os.path.dirname(__file__), 'model.env')
        load_dotenv(env_path)
        api_key = os.getenv("OPENAI_API_KEY")
    
    # If still not found, raise error
    if not api_key:
        error_msg = "OPENAI_API_KEY not found in environment variables or Streamlit secrets"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("API key found successfully")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
except Exception as e:
    logger.error(f"Error in config.py: {str(e)}")
    raise
