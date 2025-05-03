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

# Set up logging
logger = logging.getLogger(__name__)

try:
    # Load environment variables
    env_path = os.path.join(os.path.dirname(__file__), 'model.env')
    load_dotenv(env_path)
    
    # Get API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        error_msg = "OPENAI_API_KEY not found in environment variables"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    logger.info("API key found successfully")
    
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
except Exception as e:
    logger.error(f"Error in config.py: {str(e)}")
    raise
