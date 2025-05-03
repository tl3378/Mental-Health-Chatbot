#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 17:16:51 2025

@author: gloria
"""

def detect_mbti_tendency(text):
    introvert_keywords = ["overwhelmed by people", "prefer being alone", "need time to recharge", "crowded places drain me"]
    extravert_keywords = ["love being around people", "energized by socializing", "enjoy meeting new people"]

    thinker_keywords = ["logical", "analyze", "objective", "rational decision", "fact-based"]
    feeler_keywords = ["emotional", "feelings", "care deeply", "hurt easily", "sensitive"]

    text_lower = text.lower()
    introvert_score = sum(1 for kw in introvert_keywords if kw in text_lower)
    extravert_score = sum(1 for kw in extravert_keywords if kw in text_lower)
    thinker_score = sum(1 for kw in thinker_keywords if kw in text_lower)
    feeler_score = sum(1 for kw in feeler_keywords if kw in text_lower)

    personality_profile = {}

    # Decide I/E
    if introvert_score >= 2:
        personality_profile["ie"] = "introvert"
    elif extravert_score >= 2:
        personality_profile["ie"] = "extravert"
    else:
        personality_profile["ie"] = "neutral"

    # Decide T/F
    if thinker_score >= 2:
        personality_profile["tf"] = "thinker"
    elif feeler_score >= 2:
        personality_profile["tf"] = "feeler"
    else:
        personality_profile["tf"] = "neutral"

    return personality_profile
