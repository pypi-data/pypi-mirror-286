from typing import Optional, Union

import base64
import logging
import pickle

import reflex as rx
from langchain_core.messages import AIMessage, ToolMessage
from pandas import DataFrame
from sqlmodel import delete, select

from aita.agent.base import AitaAgent
from aita.agent.factory import AgentFactory
from aita.agent.graph import GraphAgent, ToolMode
from aita_lab.states.base import BaseState
from aita_lab.states.datasource import DataSourceState
from aita_lab.states.prompt_template import PromptTemplate, PromptTemplateState
from aita_lab.states.tool import Tool, ToolArg, ToolOutput
from aita_lab.states.vector_store import VectorStoreState


class QA(rx.Base):
    """A question and answer pair."""

    question: Optional[str]
    answer: Optional[str]


class Chat(rx.Model, table=True):
    """Chat Model"""

    title: str
    user: str
    question: Optional[str]
    answer: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]


DEFAULT_CHATS = {
    "Intros": [],
}


class ChatState(BaseState):
    """The app state."""

    # chat states
    chats: dict[str, list[QA]] = DEFAULT_CHATS

    current_chat = "Intros"

    question: str

    new_chat_title: str = ""

    # basic model states
    current_chat_model: str

    current_datasource: str

    # RAG states
    current_embedding_model: Optional[str] = ""

    current_prompt_template: Optional[PromptTemplate] = None

    current_k_shot: int = 0

    current_vector_feature: str = ""

    # agent states
    current_chat_agent_type: str = ""

    _current_chat_agent: Optional[Union[AitaAgent, GraphAgent]] = None

    _current_embedding_agent: Optional[AitaAgent] = None

    _current_chat_agent_state_change: bool = False

    _current_embedding_agent_state_change: bool = False

    # tool states
    current_tools: dict[str, Tool] = {}

    current_tool_id: Optional[str] = None

    run_tool_output: Optional[ToolOutput] = None

    # Whether we are processing the question.
    processing: bool = False

    vector_feature_dialog_open: bool = False

    @rx.var
    def current_tools_as_list(self) -> list[Tool]:
        if self.current_tools:
            return list(self.current_tools.values())
        return []

    @rx.var
    def current_tool_name(self) -> str:
        if self.current_tools and self.current_tool_id:
            return self.current_tools[self.current_tool_id].name
        return ""

    @rx.var
    def current_tool_args(self) -> list[ToolArg]:
        if self.current_tools and self.current_tool_id:
            return list(self.current_tools[self.current_tool_id].args.values())
        return []

    def close_vector_feature_dialog(self):
        self.vector_feature_dialog_open = False

    def set_current_chat_model(self, chat_model: str):
        if self.current_chat_model != chat_model:
            self.current_chat_model = chat_model
            self._current_chat_agent_state_change = True

    def set_current_datasource(self, datasource: str):
        if self.current_datasource != datasource:
            self.current_datasource = datasource
            self._current_chat_agent_state_change = True

    def set_current_chat_agent_type(self, chat_agent_type: str):
        if self.current_chat_agent_type != chat_agent_type:
            self.current_chat_agent_type = chat_agent_type
            self._current_chat_agent_state_change = True

    def set_current_prompt_template(self, prompt_template_name: str):
        self.current_prompt_template = PromptTemplateState.get_prompt_template(prompt_template_name)
        if self.current_prompt_template and self.current_prompt_template.k_shot > 0:
            self.vector_feature_dialog_open = True

    def _create_chat_agent(self, **kwargs):
        if not self._current_chat_agent or self._current_chat_agent_state_change:
            logging.info(
                f"Creating {self.current_chat_agent_type} agent with model {self.current_chat_model}"
            )

            self._current_chat_agent = AgentFactory.create_agent(
                agent_type=self.current_chat_agent_type,
                model=self.current_chat_model,
                **kwargs,
            )
            if self.current_datasource:
                datasource = DataSourceState.connect(self.current_datasource)
                self._current_chat_agent.add_datasource(datasource)

            logging.info(
                f"Created {self.current_chat_agent_type} agent with model {self.current_chat_model}"
            )
            self._current_chat_agent_state_change = False

    def set_current_embedding_model(self, embedding_model: str):
        if self.current_embedding_model != embedding_model:
            self.current_embedding_model = embedding_model
            self._current_embedding_agent_state_change = True

    def _create_embedding_agent(self):
        if not self._current_embedding_agent or self._current_embedding_agent_state_change:
            logging.info(f"Creating embedding agent with model {self.current_embedding_model}")
            self._current_embedding_agent = AgentFactory.create_agent(
                agent_type="embedding", model=self.current_embedding_model
            )
            self._current_embedding_agent_state_change = False

    def should_create_embedding_agent(self):
        if self.current_prompt_template and self.current_prompt_template.k_shot > 0:
            return True

    def set_current_tool_by_id(self, tool_id: str):
        if tool_id:
            logging.info(f"Setting current tool by id to {tool_id}")
            self.current_tool_id = tool_id

    def set_current_tool_by_name(self, tool_name: str):
        if tool_name:
            logging.info(f"Setting current tool by name to {tool_name}")
            for tool_id, tool in self.current_tools.items():
                if tool.name == tool_name:
                    self.current_tool_id = tool_id
                    break

    def update_current_tool_arg(self, key: str, value: str):
        tool_arg = self.current_tools[self.current_tool_id].args[key]
        new_tool_arg = ToolArg(
            name=key, reqired=tool_arg.required, description=tool_arg.description, value=value
        )
        self.current_tools[self.current_tool_id].args[key] = new_tool_arg

    def delete_current_tool(self):
        if self.current_tool_id:
            logging.info(f"Deleting current tool {self.current_tool_id}")
            del self.current_tools[self.current_tool_id]
            self.current_tool_id = None

    def cancel_tool(self):
        logging.info(f"Canceling tool {self.current_tool_id}")
        self._current_chat_agent.cancel_tool(self.current_tool_id)

    def create_chat(self):
        """Create a new chat."""
        # Add the new chat to the list of chats.
        self.current_chat = self.new_chat_title
        self.chats[self.new_chat_title] = []
        with rx.session() as session:
            session.add(
                Chat(
                    title=self.new_chat_title,
                    user=self.user.name,
                    question=None,
                    answer=None,
                    description=None,
                    created_at=None,
                    updated_at=None,
                )
            )
            session.commit()

    def delete_chat(self):
        """Delete the current chat."""
        with rx.session() as session:
            session.exec(delete(Chat).where(Chat.title == self.current_chat))
            session.commit()
        del self.chats[self.current_chat]
        self.load_chats()
        self.current_chat = list(self.chats.keys())[0]

    def set_chat(self, chat_title: str):
        """Set the title of the current chat.

        Args:
            chat_title: The name of the chat.
        """
        self.current_chat = chat_title

    @rx.var
    def chat_titles(self) -> list[str]:
        """Get the list of chat titles.

        Returns:
            The list of chat names.
        """
        return list(self.chats.keys())

    def _commit_chat(self, title: str, question: str, answer: str):
        with rx.session() as session:
            session.add(
                Chat(
                    title=title,
                    user=self.user.name,
                    question=question,
                    answer=answer,
                    description=None,
                    created_at=None,
                    updated_at=None,
                )
            )
            session.commit()

    def _process_agent_response(self, events: list[dict]):
        for event in events:
            if hasattr(event, "content"):
                message = event
            else:
                message = event["messages"][-1]
            if isinstance(message, AIMessage):
                self.chats[self.current_chat][-1].answer += message.content
            if isinstance(message, ToolMessage):
                if message.artifact is not None:
                    encoded_artifact = message.artifact.encode("utf-8")
                    artifact = base64.b64decode(encoded_artifact)
                    result = pickle.loads(artifact)
                    if isinstance(result, DataFrame):
                        self.run_tool_output = ToolOutput(data=result, show=True)
            yield

    def _process_agent_state(self):
        chat_state = self._current_chat_agent.get_current_state()
        if chat_state and chat_state.next:
            # having an action to execute
            for tool_call in self._current_chat_agent.get_current_tool_calls():
                tool = Tool(
                    id=tool_call["id"],
                    name=tool_call["name"],
                    args={
                        key: ToolArg(name=key, value=str(value))  # TODO handle other types
                        for key, value in tool_call["args"].items()
                    },
                )
                self.current_tools[tool_call["id"]] = tool
                if not self.current_tool_id:
                    self.current_tool_id = tool_call["id"]

            # Add the tool call to the answer
            self.chats[self.current_chat][
                -1
            ].answer += f"In order to assist you further, I need to run a tool shown in the kernel. Please confirm to run the tool."

    async def run_tool(self):
        self.processing = True

        tool_args = {
            tool_arg.name: tool_arg.value
            for key, tool_arg in self.current_tools[self.current_tool_id].args.items()
        }
        logging.info("Updating tool args: " + str(tool_args.items()))
        self._current_chat_agent.update_tool(self.current_tool_id, tool_args)

        # Add a empty question to the list of questions.
        qa = QA(question="", answer="")
        self.chats[self.current_chat].append(qa)

        events = self._current_chat_agent.stream(tool_mode=ToolMode.ONCE, display=False)
        for event in self._process_agent_response(events):
            yield

        self._process_agent_state()

        # Toggle the processing flag.
        self.processing = False

        # commit the chat to the database
        self._commit_chat(
            self.current_chat,
            self.chats[self.current_chat][-1].question,
            self.chats[self.current_chat][-1].answer,
        )

    async def process_question(self, form_data: dict[str, str]):

        # Clear the input and start the processing.
        self.processing = True

        # Get the question from the form
        question = form_data["question"]

        # Check if the question is empty
        if question == "":
            return

        # Add the question to the list of questions.
        qa = QA(question=question, answer="")
        self.chats[self.current_chat].append(qa)

        yield

        logging.info(f"Processing question: {question}")

        # init the chat agent
        self._create_chat_agent()

        # init the embedding agent
        if self.should_create_embedding_agent():
            self._create_embedding_agent()

            # embed the question
            embedded_question = self._current_embedding_agent.embed(question)

            # retrieve similar features
            top_k_features = VectorStoreState._retrieve_vector_features(
                self.current_vector_feature, embedded_question, self.current_k_shot
            )

            # TODO: add similar features to the prompt template
            self._current_chat_agent.add_prompt_context(top_k_features)

        async for value in self._invoke_agent(question):
            yield

        # Toggle the processing flag.
        self.processing = False

        # commit the chat to the database
        self._commit_chat(
            self.current_chat,
            self.chats[self.current_chat][-1].question,
            self.chats[self.current_chat][-1].answer,
        )

    async def _invoke_agent(self, question: Optional[str] = ""):
        """Get the response from the API.

        Args:
            question: The question to ask the API.
        """

        # Get the response and add it to the answer.
        events = self._current_chat_agent.stream(question, display=False)
        for event in self._process_agent_response(events):
            yield

        self._process_agent_state()

    def load_chats(self):
        """Load the chats from the database."""
        with rx.session() as session:
            chats = session.exec(select(Chat).where(Chat.user == self.user.name)).all()
            for chat in chats:
                self.chats[chat.title] = [QA(question=chat.question, answer=chat.answer)]
            if not self.chats:
                self.chats = DEFAULT_CHATS

    def on_load(self):
        self.load_chats()
