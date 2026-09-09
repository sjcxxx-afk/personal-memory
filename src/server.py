import asyncio
import sys
from pathlib import Path
from typing import List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp.server import Server
from mcp.types import (
    Tool, TextContent, 
    CallToolRequest, CallToolResult,
    ListToolsRequest, ListToolsResult
)
import mcp.server.stdio

from .tools.store_tool import StoreTool
from .tools.search_tool import SearchTool
from .utils.helpers import setup_logging


# Initialize logger
logger = setup_logging()

# Create MCP server
app = Server("personal-memory")

# Initialize tools
store_tool = StoreTool()
search_tool = SearchTool()


# Define available tools
TOOLS = [
    Tool(
        name="store_fact",
        description="Store a factual memory in the personal knowledge base. Facts are stored with context including scene, source, and importance.",
        input_schema={
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "The factual content to store (e.g., '用户对花生过敏')"
                },
                "scene": {
                    "type": "string",
                    "description": "Scene tag for categorization (work, life, health, finance, etc.)",
                    "default": "general"
                },
                "source": {
                    "type": "string",
                    "description": "Source of the fact (chat_2026-09-07, note, document, etc.)",
                    "default": "chat"
                },
                "importance": {
                    "type": "string",
                    "description": "Importance level (high, medium, low)",
                    "default": "medium"
                }
            },
            "required": ["content"]
        }
    ),
    Tool(
        name="search_facts",
        description="Search for facts using semantic similarity. Returns the most relevant results based on the query.",
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (e.g., '过敏信息', '工作偏好', '饮食限制')"
                },
                "scene_filter": {
                    "type": "string",
                    "description": "Optional scene tag to filter results (work, life, health, etc.)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return",
                    "default": 5
                }
            },
            "required": ["query"]
        }
    ),
    Tool(
        name="list_facts",
        description="List all stored facts with optional filtering by scene tag.",
        input_schema={
            "type": "object",
            "properties": {
                "scene_filter": {
                    "type": "string",
                    "description": "Optional scene tag to filter by (work, life, health, etc.)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of facts to return",
                    "default": 10
                }
            }
        }
    ),
    Tool(
        name="get_fact_details",
        description="Get detailed information about a specific fact by its ID.",
        input_schema={
            "type": "object",
            "properties": {
                "fact_id": {
                    "type": "string",
                    "description": "The unique identifier of the fact"
                }
            },
            "required": ["fact_id"]
        }
    ),
    Tool(
        name="get_memory_stats",
        description="Get statistics about the memory service including counts by scene and temperature distribution.",
        input_schema={
            "type": "object",
            "properties": {}
        }
    )
]


# Define tools/list handler
async def handle_list_tools(ctx, params: ListToolsRequest) -> ListToolsResult:
    """Handle tools/list requests."""
    logger.info("Listing available tools")
    return ListToolsResult(tools=TOOLS)


# Define tools/call handler
async def handle_call_tool(ctx, params: CallToolRequest) -> CallToolResult:
    """Handle tools/call requests."""
    logger.info(f"=== TOOL CALL RECEIVED ===")
    logger.info(f"Params type: {type(params)}")
    logger.info(f"Params: {params}")
    
    tool_name = params.name
    arguments = params.arguments or {}
    
    logger.info(f"Tool name: {tool_name}")
    logger.info(f"Arguments: {arguments}")
    
    try:
        if tool_name == "store_fact":
            return await handle_store_fact(arguments)
        elif tool_name == "search_facts":
            return await handle_search_facts(arguments)
        elif tool_name == "list_facts":
            return await handle_list_facts(arguments)
        elif tool_name == "get_fact_details":
            return await handle_get_fact_details(arguments)
        elif tool_name == "get_memory_stats":
            return await handle_get_memory_stats(arguments)
        else:
            return CallToolResult(
                content=[TextContent(
                    type="text",
                    text=f"❌ Unknown tool: {tool_name}"
                )],
                isError=True
            )
    except Exception as e:
        logger.error(f"Error in tool call {tool_name}: {e}")
        return CallToolResult(
            content=[TextContent(
                type="text",
                text=f"❌ Error calling tool {tool_name}: {str(e)}"
            )],
            isError=True
        )


# Tool implementations
async def handle_store_fact(arguments: dict) -> CallToolResult:
    """Handle store_fact tool calls."""
    content = arguments.get("content", "")
    scene = arguments.get("scene", "general")
    source = arguments.get("source", "chat")
    importance = arguments.get("importance", "medium")
    
    logger.info(f"Storing fact: {content[:50]}...")
    
    # Call the store tool
    result = await store_tool.store_fact(content, scene, source, importance)
    
    return CallToolResult(
        content=result,
        isError=False
    )


async def handle_search_facts(arguments: dict) -> CallToolResult:
    """Handle search_facts tool calls."""
    query = arguments.get("query", "")
    scene_filter = arguments.get("scene_filter")
    limit = arguments.get("limit", 5)
    
    logger.info(f"Searching facts: {query}")
    
    # Call the search tool
    result = await search_tool.search_facts(query, scene_filter, limit)
    
    return CallToolResult(
        content=result,
        isError=False
    )


async def handle_list_facts(arguments: dict) -> CallToolResult:
    """Handle list_facts tool calls."""
    scene_filter = arguments.get("scene_filter")
    limit = arguments.get("limit", 10)
    
    logger.info(f"Listing facts (scene: {scene_filter}, limit: {limit})")
    
    # Call the list tool
    result = await store_tool.list_facts(scene_filter, limit)
    
    return CallToolResult(
        content=result,
        isError=False
    )


async def handle_get_fact_details(arguments: dict) -> CallToolResult:
    """Handle get_fact_details tool calls."""
    fact_id = arguments.get("fact_id", "")
    
    logger.info(f"Getting fact details: {fact_id}")
    
    # Call the details tool
    result = await search_tool.get_fact_details(fact_id)
    
    return CallToolResult(
        content=result,
        isError=False
    )


async def handle_get_memory_stats(arguments: dict) -> CallToolResult:
    """Handle get_memory_stats tool calls."""
    logger.info("Getting memory stats")
    
    # Get stats from stores
    fact_stats = store_tool.fact_store.get_all_facts(limit=1000)
    vector_stats = store_tool.vector_store.get_collection_stats()
    
    # Calculate statistics
    total_facts = len(fact_stats)
    scene_counts = {}
    temperature_counts = {"hot": 0, "warm": 0, "cold": 0}
    
    for fact in fact_stats:
        # Count by scene
        scene_counts[fact.scene] = scene_counts.get(fact.scene, 0) + 1
        
        # Count by temperature
        if fact.temperature in temperature_counts:
            temperature_counts[fact.temperature] += 1
    
    # Format statistics
    stats_lines = [
        "📊 Memory Service Statistics:",
        "",
        f"📈 Total Facts: {total_facts}",
        f"🔍 Vector DB Status: {vector_stats.get('status', 'unknown')}",
        f"📦 Vector DB Count: {vector_stats.get('count', 0)}",
        "",
        "🏷️ Facts by Scene:"
    ]
    
    for scene, count in sorted(scene_counts.items(), key=lambda x: x[1], reverse=True):
        stats_lines.append(f"   • {scene}: {count}")
    
    stats_lines.extend([
        "",
        "🌡️ Temperature Distribution:"
    ])
    
    for temp, count in temperature_counts.items():
        stats_lines.append(f"   • {temp}: {count}")
    
    return CallToolResult(
        content=[TextContent(
            type="text",
            text="\n".join(stats_lines)
        )],
        isError=False
    )


# Register handlers
def register_handlers():
    """Register all handlers with the MCP server."""
    try:
        # Register tools/list handler
        app.add_request_handler(
            method="tools/list",
            params_type=ListToolsRequest,
            handler=handle_list_tools
        )
        logger.info("Registered tools/list handler")
        
        # Register tools/call handler
        app.add_request_handler(
            method="tools/call",
            params_type=CallToolRequest,
            handler=handle_call_tool
        )
        logger.info("Registered tools/call handler")
        
    except Exception as e:
        logger.error(f"Error registering handlers: {e}")
        import traceback
        traceback.print_exc()


# Register handlers
register_handlers()


async def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Personal Memory MCP Server...")
    
    # Run the server
    try:
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            logger.info("MCP server started on stdio")
            
            await app.run(
                read_stream,
                write_stream,
                app.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Error running MCP server: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())