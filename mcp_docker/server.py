from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass

from mcp.server.fastmcp import Context, FastMCP


class Database:
    @classmethod
    async def connect(cls):
        print("Database connected")
        return cls()

    async def disconnect(self):
        print("Database disconnected")

    def query(self) -> str:
        return "fake query result"

    def add(self, a: int, b: int) -> int:
        """Add two numbers together"""
        return a + b

# Define a type-safe context class
@dataclass
class AppContext:
    db: Database  # Replace with your actual resource type

# Create the lifespan context manager
@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    # Initialize resources on startup
    db = await Database.connect()
    try:
        # Make resources available during operation
        yield AppContext(db=db)
    finally:
        # Clean up resources on shutdown
        await db.disconnect()

# Create an MCP server
mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",  # only used for SSE transport
    port=8050,  # only used for SSE transport (set this to any port)
    lifespan=app_lifespan,
)

# Use the lifespan context in tools 
@mcp.tool() 
def query_db(ctx: Context) -> str: 
    """Tool that uses initialized resources""" 
    db = ctx.request_context.lifespan_context.db 
    return db.query()

# Add a simple calculator tool
@mcp.tool()
def add(ctx: Context, a: int, b: int) -> int:
    """Add two numbers using Database instance"""
    db = ctx.request_context.lifespan_context.db
    return db.add(a, b)

# Run the server
if __name__ == "__main__":
    print("Running server with SSE transport")
    mcp.run(transport="sse")
