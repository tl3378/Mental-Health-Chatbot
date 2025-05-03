#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 22:11:29 2025

@author: gloria
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from .config import client
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_conversation_chain():
    try:
        # Load environment variables
        env_path = os.path.join(os.path.dirname(__file__), 'model.env')
        load_dotenv(env_path)
        
        # Get API key from the client
        api_key = client.api_key
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables")
        
        logger.info("Initializing ChatOpenAI...")
        # Initialize the language model
        llm = ChatOpenAI(
            model_name="gpt-4o",
            temperature=0.7,
            openai_api_key=api_key
        )
        
        logger.info("Creating memory...")
        # Create memory
        memory = ConversationBufferMemory()
        
        logger.info("Creating prompt template...")
        # Create prompt template
        template = """You are a supportive assistant who helps users talk about their feelings and mental health. 
        Respond warmly and empathetically, focusing on active listening and emotional support.
        
        Current conversation:
        {history}
        Human: {input}
        Assistant:"""
        
        prompt = PromptTemplate(
            input_variables=["history", "input"],
            template=template
        )
        
        logger.info("Creating conversation chain...")
        # Create conversation chain
        conversation_chain = ConversationChain(
            llm=llm,
            memory=memory,
            prompt=prompt,
            verbose=True
        )
        
        logger.info("Conversation chain setup completed successfully")
        return conversation_chain
    except Exception as e:
        logger.error(f"Error in setup_conversation_chain: {str(e)}", exc_info=True)
        raise

