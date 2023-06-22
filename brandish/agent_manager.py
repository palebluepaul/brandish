"""
Module to manage agents.
This module will be responsible for instantiating and invoking agents using langchain and OpenAI API.
"""

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os
from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

def instantiate_agents():
    """
    Function to instantiate the agents.
    """
   

def invoke_agents(documents):
    """
    Function to invoke the agents.
    """
    chat = ChatOpenAI(temperature=0.7,model="gpt-4-0613")
    response = (chat.predict_messages([HumanMessage(content=documents[0].text),SystemMessage(content="You are a marketing guru.")]))

    return response