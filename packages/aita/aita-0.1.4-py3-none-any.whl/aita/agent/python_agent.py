from typing import Dict, Optional

from aita.agent.graph import GraphAgent
from aita.tool.python_tool import PythonTool


class PythonAgent(GraphAgent):
    type: str = "python"
    description: str = "A Python agent that can use Python tools to run python scripts."

    def __init__(
        self,
        model: str,
        model_parameters: Optional[Dict] = None,
    ):
        super().__init__([PythonTool()], model, model_parameters)

    def add_script_context(self, script_context):
        for tool in self.tools:
            tool.update_script_context(script_context=script_context)
        return self
