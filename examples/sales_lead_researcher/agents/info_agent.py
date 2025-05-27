from pydantic import BaseModel

from agents import Agent, WebSearchTool
from agents.model_settings import ModelSettings

INSTRUCTIONS = (
    "You gather sales lead information for our CRM. "
    "Given a person's name and company, search the web (LinkedIn and the company's website) "
    "and fill out the following fields as best you can. Use concise language."
)


class LeadInfo(BaseModel):
    # Basic contact data
    full_name: str
    title: str
    position: str
    email: str | None
    phone: str | None
    linkedin: str | None

    # Company data
    company: str
    company_type: str | None
    company_size: str | None
    headquarters: str | None
    website: str | None
    languages: str | None
    publication_formats: str | None

    # Publication/content data
    publication_types: str | None
    publication_frequency: str | None
    topics: str | None
    audience: str | None


info_agent = Agent(
    name="LeadInfoAgent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool()],
    model_settings=ModelSettings(tool_choice="required"),
    output_type=LeadInfo,
)
