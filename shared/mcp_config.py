import os

from models.tool_definitions import MCPServerDefinition


def get_stripe_mcp_server_definition(included_tools: list[str]) -> MCPServerDefinition:
    """
    Returns a Stripe MCP server definition with customizable included tools.

    Args:
        included_tools: List of tool names to include from the Stripe MCP server

    Returns:
        MCPServerDefinition configured for Stripe
    """
    return MCPServerDefinition(
        name="stripe-mcp",
        command="npx",
        args=[
            "-y",
            "@stripe/mcp",
            "--tools=all",
            f"--api-key={os.getenv('STRIPE_API_KEY')}",
        ],
        env=None,
        included_tools=included_tools,
    )


def get_google_sheets_mcp_server_definition(
    included_tools: list[str],
) -> MCPServerDefinition:
    """
    Returns an MCPServerDefinition for the mcp-google-sheets server.

    It assumes you've already exported:
        SERVICE_ACCOUNT_PATH  – absolute path to your *.json* key
        DRIVE_FOLDER_ID       – the shared Drive folder ID
    Optionally:
        GOOGLE_APPLICATION_CREDENTIALS – set to the same path as SERVICE_ACCOUNT_PATH
                                         (handy belt-and-braces for ADC)

    Args:
        included_tools: List of tool names (e.g. ["list_spreadsheets", "get_sheet_data"])
                        that you want the client to expose. Use ["*"] or an empty list
                        to expose everything.

    Returns:
        A fully configured MCPServerDefinition instance.
    """
    service_account = os.getenv("SERVICE_ACCOUNT_PATH")
    drive_folder_id = os.getenv("DRIVE_FOLDER_ID")

    if not service_account or not drive_folder_id:
        # Fail early with a clear message instead of
        # letting Claude Desktop launch an unusable server
        raise RuntimeError(
            "Both SERVICE_ACCOUNT_PATH and DRIVE_FOLDER_ID "
            "must be set before starting the Google-Sheets MCP server."
        )

    # Build the env block Claude Desktop will inject into the subprocess
    env = {
        "SERVICE_ACCOUNT_PATH": service_account,
        "DRIVE_FOLDER_ID": drive_folder_id,
        # Propagate GOOGLE_APPLICATION_CREDENTIALS if the caller has set it,
        # otherwise fall back to the service-account path (optional but safe)
        "GOOGLE_APPLICATION_CREDENTIALS": os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS", service_account
        ),
    }

    return MCPServerDefinition(
        name="google-sheets-mcp",
        command="uvx",
        args=[
            # Always pull the freshest version
            "mcp-google-sheets@latest",
        ],
        env=env,
        included_tools=included_tools,
    )
