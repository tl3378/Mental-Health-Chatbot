#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 14:03:10 2025

@author: gloria
"""

# emotion.py
import torch
from torch.nn.functional import sigmoid
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "joeddav/distilbert-base-uncased-go-emotions-student"
tokenizer = AutoTokenizer.from_pretrained(model_name)
emotion_model = AutoModelForSequenceClassification.from_pretrained(model_name)
id2label = emotion_model.config.id2label

anxiety_tags = {"nervousness", "confusion", "fear", "disappointment", "embarrassment"}
depression_tags = {"sadness", "grief", "despair", "remorse", "lonely"}

def detect_emotions(text, top_k=5):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        logits = emotion_model(**inputs).logits
    probs = sigmoid(logits)[0]
    top_ids = probs.topk(top_k).indices
    return [(id2label[i.item()], round(probs[i].item(), 4)) for i in top_ids]

def score_emotion_groups(emotions):
    scores = {"anxiety": 0.0, "depression": 0.0}
    for label, score in emotions:
        if label in anxiety_tags:
            scores["anxiety"] += score
        if label in depression_tags:
            scores["depression"] += score
    return scores
