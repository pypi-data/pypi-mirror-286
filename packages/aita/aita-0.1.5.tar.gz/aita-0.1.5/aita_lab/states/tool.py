from typing import Optional

import pandas as pd
import reflex as rx

from aita import tool
from aita_lab.states.utils import get_model_classes, get_model_fields, get_model_fields_as_dict


class ToolArg(rx.Model):
    name: str
    required: Optional[bool]
    description: Optional[str]
    value: Optional[str]


class Tool(rx.Model):
    id: Optional[str]
    name: str
    args: dict[str, ToolArg]
    description: Optional[str]


class ToolOutput(rx.Base):
    data: pd.DataFrame
    show: bool = False


class ToolState(rx.State):
    tools: list[Tool]

    @rx.var
    def tool_names(self) -> list[str]:
        return [t.name for t in self.tools]

    def load_tools(self):
        self.tools = []
        for t in get_model_classes(tool):
            name, cls = t
            description = get_model_fields(cls, "description")
            args_schema = get_model_fields(cls, "args_schema")
            args = get_model_fields_as_dict(args_schema)
            self.tools.append(
                Tool(
                    name=name,
                    description=description,
                    args={
                        arg["name"]: ToolArg(
                            name=arg["name"],
                            required=arg["required"],
                            description=arg["description"],
                        )
                        for arg in args.values()
                    },
                )
            )

    def on_load(self):
        self.load_tools()
