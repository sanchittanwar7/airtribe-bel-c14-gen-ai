from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnablePassthrough
import os
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

# --- Using ChatMessageHistory (Modern LangChain 0.3+ approach) ---
# ChatMessageHistory stores messages as a list of BaseMessage objects.
# This replaces the deprecated ConversationBufferMemory.
from langchain_core.messages import HumanMessage, AIMessage

# Create message history store
message_history = ChatMessageHistory()

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Use conversation history for context."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

# Chain with memory
chain = prompt | model

def chat(user_input):
    # Get history as list of messages
    history = message_history.messages
    
    # Get response
    response = chain.invoke({"input": user_input, "history": history})
    
    # Save to memory
    message_history.add_user_message(user_input)
    message_history.add_ai_message(response.content)
    
    return response.content

# Test conversation
print(chat("My name is Alex and I'm learning Python."))
print(chat("What's a good project for a beginner?"))
print(chat("What's my name again?"))