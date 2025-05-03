#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""

from langchain.memory import ConversationBufferMemory

# Initialize conversation memory
memory = ConversationBufferMemory(
    memory_key="history",
    return_messages=True,
    input_key="input",
    max_history_messages=10  # Limit to store the last 10 messages
)
