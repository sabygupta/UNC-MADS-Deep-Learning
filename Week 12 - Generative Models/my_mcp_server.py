from mcp.server.fastmcp import FastMCP
import math

# Create the MCP server
mcp = FastMCP("My Calculator Server")

# Define a tool using the @mcp.tool() decorator
@mcp.tool()
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression safely.
    
    Args:
        expression: A mathematical expression like '2**10 + sqrt(144)'
    """
    allowed = {"__builtins__": {}}
    allowed.update({k: getattr(math, k) for k in dir(math) if not k.startswith("_")})
    try:
        result = eval(expression, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e}"

@mcp.tool()
def unit_convert(value: float, from_unit: str, to_unit: str) -> str:
    """Convert between common units.
    
    Args:
        value: The numeric value to convert
        from_unit: Source unit (e.g., 'km', 'miles', 'celsius', 'fahrenheit')
        to_unit: Target unit
    """
    conversions = {
        ("km", "miles"): lambda x: x * 0.621371,
        ("miles", "km"): lambda x: x * 1.60934,
        ("celsius", "fahrenheit"): lambda x: x * 9/5 + 32,
        ("fahrenheit", "celsius"): lambda x: (x - 32) * 5/9,
        ("kg", "lbs"): lambda x: x * 2.20462,
        ("lbs", "kg"): lambda x: x * 0.453592,
    }
    key = (from_unit.lower(), to_unit.lower())
    if key in conversions:
        result = conversions[key](value)
        return f"{value} {from_unit} = {result:.4f} {to_unit}"
    return f"Conversion from {from_unit} to {to_unit} is not supported."

# Define a resource
@mcp.resource("info://server/about")
def get_server_info() -> str:
    """Information about this MCP server."""
    return "This is a calculator MCP server that can evaluate math expressions and convert units."

# Run the server
if __name__ == "__main__":
    mcp.run()