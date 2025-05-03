#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the correct path
env_path = os.path.join(os.path.dirname(__file__), 'model.env')
load_dotenv(env_path)

# Get API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)
