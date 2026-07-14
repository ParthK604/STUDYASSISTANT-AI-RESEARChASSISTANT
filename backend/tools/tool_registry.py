from typing import Dict, List

from langchain_core.tools import BaseTool

from backend.tools.calculator_tool import calculator_tool
from backend.tools.rag_search import rag_tool
from backend.tools.web_search import tavily_tool


class ToolRegistry:

    def __init__(self):

        self._tools_list: List[BaseTool] = [
            rag_tool,
            tavily_tool,
            calculator_tool,
        ]

        self._tools_dict: Dict[str, BaseTool] = {
            tool.name: tool
            for tool in self._tools_list
        }

    def get_all_tools(self) -> List[BaseTool]:
        return self._tools_list

    def get_tool_map(self) -> Dict[str, BaseTool]:
        return self._tools_dict

    def get_tool(self, name: str) -> BaseTool:

        if name not in self._tools_dict:
            raise KeyError(f"Tool '{name}' not found.")

        return self._tools_dict[name]


registry = ToolRegistry()