import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    },
    {
        "type": "function",
        "function": {
            "name": "get_flight_info",
            "description": "Get flight information between two cities",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "Origin city"
                    },
                    "destination": {
                        "type": "string",
                        "description": "Destination city"
                    },
                    "date": {
                        "type": "string",
                        "description": "Travel date in YYYY-MM-DD format"
                    }
                },
                "required": ["origin", "destination"]
            }
        }
    }
]

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

def get_flight_info(origin, destination, date=None):
    """Mock flight information."""
    import random
    return {
        "origin": origin,
        "destination": destination,
        "date": date or "2025-01-15",
        "price": random.randint(200, 800),
        "duration": f"{random.randint(2, 8)}h {random.randint(0, 59)}m",
        "airline": random.choice(["Delta", "United", "American"])
    }

# Update function dispatcher
available_functions = {
    "get_weather": get_weather,
    "calculate": calculate,
    "get_flight_info": get_flight_info
}

# Complex query requiring multiple tools
def run_complex_conversation(user_message):
    """Handle conversations that may need multiple tool calls."""
    messages = [{"role": "user", "content": user_message}]
    
    print(f"User: {user_message}\n")
    
    max_iterations = 5  # Prevent infinite loops
    iteration = 0
    
    while iteration < max_iterations:
        iteration += 1
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        # Check if we're done
        if not response_message.tool_calls:
            print(f"Assistant: {response_message.content}")
            return response_message.content
        
        # Process tool calls
        print(f"🔧 Iteration {iteration}: Processing {len(response_message.tool_calls)} tool call(s)\n")
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"  → {function_name}({function_args})")
            
            function_to_call = available_functions[function_name]
            function_response = function_to_call(**function_args)
            
            print(f"    ✓ Result: {function_response}\n")
            
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": json.dumps(function_response)
            })
    
    return "Max iterations reached"

# Demo complex query
print("=" * 70)
print("COMPLEX DEMO: Multiple Tools")
print("=" * 70)
run_complex_conversation(
    "I'm planning a trip from Seattle to Miami. What's the weather like in Miami, "
    "and can you find me a flight? Also calculate the total cost if I need to book 3 tickets."
)