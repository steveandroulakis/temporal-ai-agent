from typing import List

from models.tool_definitions import AgentGoal
from shared.mcp_config import get_google_sheets_mcp_server_definition

# Generic starter prompt reused across agent goals
starter_prompt_generic = "Welcome me, give me a description of what you can do, then ask me for the details you need to do your job."

# ---------------------------------------------------------------------------
# Google Sheets agent goal
# ---------------------------------------------------------------------------

goal_google_sheets_management = AgentGoal(
    id="goal_google_sheets_management",
    category_tag="sheets",
    agent_name="Google Sheets Assistant",
    agent_friendly_description=(
        "Create, read, and update Google Spreadsheets through the MCP Google‑Sheets server. "
        "You can list spreadsheets, create new ones, read and write cell values, add rows or columns, "
        "and share sheets, all without leaving chat. Since you can see your spreadsheet alongside this chat, "
        "I'll focus on making changes rather than describing what's already visible to you."
    ),
    # If you have any custom convenience tools wrapped in tool_registry you can add them here.
    # All native Google‑Sheets operations are surfaced automatically via the MCP server tools.
    tools=[],
    mcp_server_definition=get_google_sheets_mcp_server_definition(
        included_tools=[
            "list_spreadsheets",
            "create_spreadsheet",
            "list_sheets",
            "get_sheet_data",
            "update_cells",
            "add_rows",
            "create_sheet",
            "batch_update_cells",
            "share_spreadsheet",
        ]
    ),
    description=(
        "Help the user with any Google Sheets task in a free-flowing, conversational manner. "
        "This is an ONGOING conversation - NEVER set next='done' unless the user explicitly asks to end the chat. "
        "After completing ANY task, always ask what they'd like to do next to keep the conversation flowing. "
        "The user has their spreadsheet open alongside this chat and can see changes in real-time. "
        "Focus on taking actions rather than describing what's visible. Available tools: list_spreadsheets, "
        "create_spreadsheet, list_sheets, get_sheet_data, update_cells, add_rows, create_sheet, "
        "batch_update_cells, share_spreadsheet. Be concise and action-oriented - users can see the results "
        "immediately. Remember spreadsheet_id and sheet names between tool calls for seamless multi-step workflows. "
        "CRITICAL: This goal has no defined end - keep helping until the user says they're done."
    ),
    starter_prompt=starter_prompt_generic,
    example_conversation_history="\n ".join(
        [
            "user: I want to work with my business data in Google Sheets.",
            "agent: Welcome! I'm your Google Sheets assistant and can help with any spreadsheet task. I can create new sheets, analyze existing data, update records, share documents, and much more. What would you like to do first?",
            "user: Show me what spreadsheets I have access to.",
            "user_confirmed_tool_run: <user clicks confirm on list_spreadsheets tool>",
            'tool_result: {"spreadsheets": [{"id": "abc123", "name": "Sales Data 2024"}, {"id": "def456", "name": "Budget Planning"}]}',
            "agent: I found 2 spreadsheets: 'Sales Data 2024' and 'Budget Planning'. Which one would you like to work with?",
            "user: Let's work with Sales Data 2024.",
            "agent: Great! Since you have the spreadsheet open, you can see your data. What would you like me to do with it?",
            "user: Add a new sale: today's date, Widget C, $950 revenue, 19 units.",
            "user_confirmed_tool_run: <user clicks confirm on add_rows tool with spreadsheet_id='abc123', data=[['2024-01-15', 'Widget C', '950', '19']]>",
            'tool_result: {"status": "success", "updatedRows": 1}',
            "agent: Perfect! I've added the new Widget C sale to your spreadsheet. What would you like to do next? I can help with calculations, create charts, share the sheet, or handle any other spreadsheet tasks.",
        ]
    ),
)

# Export the goal list so the agent loader can discover it
sheets_goals: List[AgentGoal] = [
    goal_google_sheets_management,
]
