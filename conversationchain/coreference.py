#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""

import spacy
from spacy.lang.en import English

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def resolve_coreferences(text):
    """
    Process coreference resolution in the text using spaCy
    
    Args:
        text (str): Input text to be processed
        
    Returns:
        str: Processed text with resolved coreferences
    """
    try:
        # Process the text with spaCy
        doc = nlp(text)
        
        # Get resolved text
        resolved_text = text
        
        # Replace pronouns with their antecedents
        for token in doc:
            if token.pos_ == "PRON" and token.dep_ in ["nsubj", "dobj", "pobj"]:
                # Find the antecedent
                for ancestor in token.ancestors:
                    if ancestor.pos_ in ["NOUN", "PROPN"]:
                        resolved_text = resolved_text.replace(token.text, ancestor.text)
                        break
        
        return resolved_text
    except Exception as e:
        print(f"Coreference resolution error: {str(e)}")
        return text  # Return original text if processing fails 