from pydantic import BaseModel

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

INSTRUCTIONS = (
    "You find the best editorial contact at a publishing company. Given just the company's name, "
    "search the web to identify a likely decision maker we could reach out to. "
    "Prefer people responsible for content or editorial decisions. "
    "Return their full name and title. If unsure, make your best guess based on available information."
)


class ContactInfo(BaseModel):
    full_name: str
    title: str


contact_finder_agent = Agent(
    name="ContactFinderAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=ContactInfo,
)
