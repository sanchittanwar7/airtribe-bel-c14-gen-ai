#!/usr/bin/env python3
"""
Simple MCP Server with basic tools
"""
import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent
from mcp.server.stdio import stdio_server

# Create server instance
app = Server("my-first-mcp-server")

# Store our tools
@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="add_numbers",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="get_weather",
            description="Get mock weather data for a city",
            inputSchema={
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city"
                    }
                },
                "required": ["city"]
            }
        )
    ]

# Handle tool calls
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool execution"""
    
    if name == "add_numbers":
        try:
            a = arguments.get("a")
            b = arguments.get("b")
            
            if a is None or b is None:
                raise ValueError("Both 'a' and 'b' are required")
            
            result = a + b
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "result": result,
                        "operation": f"{a} + {b} = {result}"
                    }, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "error": str(e)
                    }, indent=2)
                )
            ]
    
    elif name == "get_weather":
        try:
            city = arguments.get("city")
            
            if not city:
                raise ValueError("City name is required")
            
            # Mock weather data
            weather_data = {
                "city": city,
                "temperature": 72,
                "conditions": "Sunny",
                "humidity": 45,
                "wind_speed": 10,
                "unit": "Fahrenheit"
            }
            
            return [
                TextContent(
                    type="text",
                    text=json.dumps(weather_data, indent=2)
                )
            ]
        except Exception as e:
            return [
                TextContent(
                    type="text",
                    text=json.dumps({
                        "error": str(e)
                    }, indent=2)
                )
            ]
    
    else:
        return [
            TextContent(
                type="text",
                text=json.dumps({
                    "error": f"Unknown tool: {name}"
                }, indent=2)
            )
        ]

async def main():
    """Run the server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())