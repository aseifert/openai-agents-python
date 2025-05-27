from pydantic import BaseModel

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

INSTRUCTIONS = (
    "You find editorial contacts at a publishing company. Given just the company's name, "
    "search the web to identify as many likely decision makers as you can. "
    "Prefer people responsible for content or editorial decisions. "
    "Return a list of their full names and titles, in order of relevance. "
    "If unsure, make your best guess based on available information."
)


class ContactInfo(BaseModel):
    full_name: str
    title: str


contact_finder_agent = Agent(
    name="ContactFinderAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=list[ContactInfo],
)
