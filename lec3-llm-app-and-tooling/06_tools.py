import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Step 1: Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City and state, e.g., 'Seattle, WA'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to evaluate, e.g., '2+2' or '15*23'"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# Step 2: Implement actual functions
def get_weather(location, unit="fahrenheit"):
    """Mock weather function."""
    import random
    temp = random.randint(60, 85) if unit == "fahrenheit" else random.randint(15, 30)
    return {
        "location": location,
        "temperature": temp,
        "unit": unit,
        "conditions": random.choice(["sunny", "cloudy", "rainy"])
    }

def calculate(expression):
    """Safe calculator function."""
    try:
        # Only allow basic math operations for security
        allowed_chars = set("0123456789+-*/(). ")
        if not all(c in allowed_chars for c in expression):
            return {"error": "Invalid expression"}
        result = eval(expression)
        return {"expression": expression, "result": result}
    except Exception as e:
        return {"error": str(e)}

# Step 3: Function dispatcher
available_functions = {
    "get_weather": get_weather,
    "calculate": calculate
}

# Step 4: Main interaction loop
def run_conversation(user_message):
    """Run a conversation with tool calling."""
    messages = [{"role": "user", "content": user_message}]
    
    print(f"User: {user_message}\n")
    
    # First API call - model may request tool calls
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"  # Let model decide when to use tools
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # Check if model wants to call tools
    if tool_calls:
        print("🔧 Model requested tool calls:\n")
        
        # Add assistant's response to messages
        messages.append(response_message)
        
        # Execute each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"  Calling: {function_name}")
            print(f"  Arguments: {function_args}")
            
            # Execute the function
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)
            
            print(f"  Result: {function_response}\n")
            
            # Add function result to messages
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response)
            })
        
        # Second API call - model generates final response with tool results
        print("🤖 Model generating final response...\n")
        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        
        final_message = second_response.choices[0].message.content
        print(f"Assistant: {final_message}")
        return final_message
    
    else:
        # No tool calls needed
        print(f"Assistant: {response_message.content}")
        return response_message.content

# Demo different queries
# print("=" * 70)
# print("DEMO 1: Weather Query")
# print("=" * 70)
# run_conversation("What's the weather like in Seattle?")

# print("\n" + "=" * 70)
print("DEMO 2: Math Query")
print("=" * 70)
run_conversation("What is 234 * 567?")

# print("\n" + "=" * 70)
# print("DEMO 3: No Tool Needed")
# print("=" * 70)
# run_conversation("What is the capital of France?")