"""
ToolManager: Handles tool selection and execution based on user input.
"""

from typing import Optional
from search_util import google_search


class ToolManager:
    """Manages the selection and execution of tools based on user input."""

    def __init__(self):
        """Initialize the ToolManager with available tools."""
        self.tools = {
            "search": google_search,
            # Add more tools here as needed
        }

    def execute_tool(self, user_input: str) -> Optional[str]:
        """
        Execute the appropriate tool based on user input.

        Args:
            user_input (str): The user's input message.

        Returns:
            Optional[str]: The result of the tool execution, or None if no tool was used.
        """
        tool_name = self._select_tool(user_input)
        if tool_name:
            tool = self.tools.get(tool_name)
            if tool:
                return tool(user_input)
        return None

    def _select_tool(self, user_input: str) -> Optional[str]:
        """
        Select the appropriate tool based on user input.

        Args:
            user_input (str): The user's input message.

        Returns:
            Optional[str]: The name of the selected tool, or None if no tool was selected.
        """
        if any(
            keyword in user_input.lower() for keyword in ["search", "look up", "find"]
        ):
            return "search"
        # Add more tool selection logic here
        return None
