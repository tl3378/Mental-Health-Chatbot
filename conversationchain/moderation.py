#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""

# moderation.py
from .config import client

def is_input_flagged(input_text):
    try:
        response = client.moderations.create(input=input_text)
        result = response.results[0]
        flagged_labels = [label for label, is_flagged in result.categories.__dict__.items() if is_flagged]
        return result.flagged, flagged_labels
    except Exception as e:
        return "error", str(e)

def classify_user_intent(text):
    support_keywords = [
        "my friend", "someone I care about", "help someone", "worried about", "how can I support"
    ]
    self_keywords = [
        "i feel", "i want", "i'm tired", "i don't want", "i can't", "i hate myself"
    ]
    text_lower = text.lower()
    if any(phrase in text_lower for phrase in support_keywords):
        return "support_others"
    elif any(phrase in text_lower for phrase in self_keywords):
        return "self_emotion"
    else:
        return "unknown"
