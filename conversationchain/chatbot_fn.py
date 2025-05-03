#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 23 21:50:20 2025

@author: gloria
"""

from .moderation import is_input_flagged, classify_user_intent
from .coreference import resolve_coreferences
from .config import client
import logging
import os
import sys

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Create file handler
file_handler = logging.FileHandler('logs/chatbot.log')
file_handler.setLevel(logging.INFO)

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def analyze_emotion_and_mbti_gpt4o(user_input):
    prompt = f"""
Analyze the following text and answer in JSON:
1. What is the user's main emotion? (e.g. sadness, anxiety, hope, anger, etc.)
2. What is the user's MBTI tendency? (e.g. introvert/extravert, thinker/feeler)
Text: "{user_input}"
Respond in the following JSON format:
{{"emotion": <emotion>, "mbti": {{"ie": <introvert/extravert/neutral>, "tf": <thinker/feeler/neutral>}}}}
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.0
        )
        import json
        import re
        # Extract JSON from response
        text = response.choices[0].message.content
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            result = json.loads(match.group(0))
            emotion = result.get("emotion", "neutral")
            mbti = result.get("mbti", {"ie": "neutral", "tf": "neutral"})
        else:
            emotion = "neutral"
            mbti = {"ie": "neutral", "tf": "neutral"}
        return emotion, mbti
    except Exception as e:
        logging.error(f"Error in GPT-4o emotion/MBTI analysis: {str(e)}")
        return "neutral", {"ie": "neutral", "tf": "neutral"}

def chatbot_fn(message, history, conversation_chain):
    try:
        logger.info("Starting chatbot_fn with message: %s", message)
        
        if not message or not isinstance(message, str):
            logger.error("Invalid message input")
            return "I'm sorry, I couldn't process your message. Please try again."
            
        if not conversation_chain:
            logger.error("No conversation chain available")
            return "I'm sorry, there was an error initializing the conversation. Please try again."
        
        # Coreference resolution
        try:
            resolved_message = resolve_coreferences(message)
            logger.info(f"Resolved message: {resolved_message}")
        except Exception as e:
            logger.error(f"Error in coreference resolution: {str(e)}")
            resolved_message = message  # fallback
        
        # Emotion and MBTI detection using GPT-4o
        emotion, mbti = analyze_emotion_and_mbti_gpt4o(resolved_message)
        logger.info(f"Emotion: {emotion}")
        logger.info(f"MBTI: {mbti}")
        
        # Style guide for assistant
        style_instruction = ""
        if emotion == "anxiety":
            style_instruction += "The user may be feeling anxious. Respond calmly and reassuringly. "
        elif emotion == "depression" or emotion == "sadness":
            style_instruction += "The user may be feeling hopeless. Respond gently and with encouragement. "
        elif emotion == "anger":
            style_instruction += "The user may be feeling angry. Respond with patience and understanding. "
        elif emotion == "hope":
            style_instruction += "The user may be feeling hopeful. Encourage and support their positive outlook. "
        else:
            style_instruction += "Provide general emotional support in a caring tone. "

        if mbti.get("ie") == "introvert":
            style_instruction += "Respect introversion: allow emotional space. "
        elif mbti.get("ie") == "extravert":
            style_instruction += "Encourage social engagement if appropriate. "

        if mbti.get("tf") == "thinker":
            style_instruction += "Support suggestions with logical reasons. "
        elif mbti.get("tf") == "feeler":
            style_instruction += "Focus more on emotional resonance. "

        # Merge instruction + user message
        conditioned_message = f"[Instruction for assistant: {style_instruction}]\nUser says: {resolved_message}"
        logger.info(f"Final instruction: {style_instruction}")
        
        # Check moderation
        try:
            flagged, reason = is_input_flagged(resolved_message)
            logger.info(f"Moderation check - Flagged: {flagged}, Reason: {reason}")
        except Exception as e:
            logger.error(f"Error in moderation check: {str(e)}")
            flagged, reason = False, None
        
        if flagged is True:
            try:
                user_intent = classify_user_intent(resolved_message)
                logger.info(f"User intent: {user_intent}")
            except Exception as e:
                logger.error(f"Error in intent classification: {str(e)}")
                user_intent = "unknown"
            
            if user_intent == "support_others":
                return """⚠️ I understand you're worried about someone else's mental health. Let me help you support them.

First, try to stay calm and listen to them without judgment. Express your concern in a caring way, and don't be afraid to ask directly if they're thinking about self-harm. 

It's important to encourage them to seek professional help. You can offer to help them find resources or make appointments. If they're in immediate crisis, please call emergency services or a crisis hotline right away.

Remember to take care of yourself too. Supporting someone with mental health challenges can be emotionally demanding. Set healthy boundaries and consider seeking support for yourself. You don't have to handle this alone - professional help is available for both of you."""
            elif user_intent == "self_emotion":
                return """⚠️ I hear that you're going through a difficult time. Let me help you find some support.

First, reach out to someone you trust - a friend, family member, or mental health professional. If you're in crisis, please call emergency services or a crisis hotline immediately.

In the meantime, try some simple self-care strategies. Take a few deep breaths, go for a short walk, or write down your thoughts and feelings. These small steps can help ground you in the present moment.

Most importantly, know that professional help is available. Consider scheduling an appointment with a therapist or counselor, or exploring online mental health resources. Your feelings are valid, and you don't have to face this alone."""
            else:
                return """⚠️ I'm concerned about your message. Your safety is the most important thing right now.

If you or someone else is in immediate danger, please call emergency services right away. Stay with the person if possible, and remove any potential means of self-harm.

Please contact a mental health professional immediately, or call a crisis hotline for immediate support. If needed, don't hesitate to visit an emergency room.

Reach out to trusted friends or family members. It's okay to ask for help - in fact, it's one of the bravest things you can do. Professional support is available, and you deserve to get the help you need.

Your safety is the top priority. Please seek professional help immediately."""
        elif flagged == "error":
            logger.error(f"Moderation error: {reason}")
            return f"⚠️ Moderation system error: {reason}"

        # Run conversation
        try:
            logger.info("Running conversation chain with message: %s", conditioned_message)
            response = conversation_chain.run(conditioned_message)
            logger.info("Got response from conversation chain: %s", response)
            return response
        except Exception as e:
            logger.error(f"Error in conversation chain: {str(e)}", exc_info=True)
            return "I'm sorry, I encountered an error while processing your message. Please try again."
    except Exception as e:
        logger.error(f"Error in chatbot_fn: {str(e)}", exc_info=True)
        return "I'm sorry, I encountered an unexpected error. Please try again."
